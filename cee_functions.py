# cee_functions.py
import math
import requests

# --- Constantes et Données (inchangées) ---
SEUILS = {
    "idf": {
        1: [23768, 28933, 40404], 2: [34884, 42463, 59394], 3: [41893, 51000, 71060],
        4: [48914, 59549, 83637], 5: [55961, 68123, 95758], "supplémentaire": [7038, 8568, 12122]
    },
    "hors_idf": {
        1: [17173, 22015, 30844], 2: [25115, 32197, 45340], 3: [30206, 38719, 54592],
        4: [35285, 45234, 63844], 5: [40388, 51775, 73098], "supplémentaire": [5094, 6525, 9254]
    }
}
IDF_DEPARTEMENTS = {"75", "77", "78", "91", "92", "93", "94", "95"}
PLAFONDS_TRAVAUX = {"gain_2_classes": 40000, "gain_3_classes": 55000, "gain_4_classes_ou_plus": 70000}
TAUX_FINANCEMENT = {
    "très_modestes": {"gain_2_classes": 0.80, "gain_3_classes": 0.80, "gain_4_classes_ou_plus": 0.80},
    "modestes": {"gain_2_classes": 0.60, "gain_3_classes": 0.60, "gain_4_classes_ou_plus": 0.60},
    "intermédiaires": {"gain_2_classes": 0.45, "gain_3_classes": 0.50, "gain_4_classes_ou_plus": 0.50},
    "supérieurs": {"gain_2_classes": 0.10, "gain_3_classes": 0.15, "gain_4_classes_ou_plus": 0.20}
}
BONUS_SORTIE_PASSOIRE = 0.10
TAUX_ECRETEMENT = {"très_modestes": 1.00, "modestes": 0.80, "intermédiaires": 0.80, "supérieurs": 0.50}
PRISE_EN_CHARGE_MAR = {"très_modestes": 1.00, "modestes": 0.80, "intermédiaires": 0.40, "supérieurs": 0.20}
PLAFOND_MAR = 2000
PLAFOND_MAR_HABITAT_INDIGNE = 4000
CLASSES_ORDRE = ["G", "F", "E", "D", "C", "B", "A"]
CLASSES_ORDRE_INV = {classe: i for i, classe in enumerate(CLASSES_ORDRE)}
PRIX_POSTES_TRAVAUX_HT = {
    "pac_eau_eau_geo": 17300, "chaudiere_granules": 13000, "chaudiere_buches": 6700, "ssc": 19000,
    "pac_air_eau": 14000, "cesi": 5290, "insert_buches_granules": 3590, "panneau_solaire_hybride_eau": 14500,
    "chauffe_eau_thermo": 2680, "depose_cuve_fioul": 1250, "audit_energetique": 1150, "vmc_double_flux": 3710,
}


# --- Fonction pour interroger l'API Géo (similaire à votre version) ---
def get_info_localisation(code_postal_saisi):
    """
    Valide un code postal et récupère les informations de localisation via l'API Géo.
    Retourne un dictionnaire avec 'valide' (bool), 'code_postal_api', 'ville', 'region', et 'message'.
    """
    default_return = {
        "valide": False, "code_postal_api": code_postal_saisi, "ville": None,
        "region": None, "message": ""
    }

    if not code_postal_saisi or not code_postal_saisi.isdigit() or len(code_postal_saisi) != 5:
        default_return["message"] = "Format du code postal incorrect (5 chiffres attendus)."
        return default_return

    url = f"https://geo.api.gouv.fr/communes?codePostal={code_postal_saisi}&fields=nom,codeDepartement,codePostal"
    # Ajout de &codePostal pour s'assurer que l'API retourne bien le CP, car un CP peut couvrir plusieurs "communes" au sens de l'API
    # et on veut le CP saisi s'il est valide, ou celui de la commune principale.

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data:  # Si la liste est vide, le code postal n'a retourné aucune commune
            default_return["message"] = f"Le code postal '{code_postal_saisi}' n'a pas été trouvé ou n'est pas reconnu."
            return default_return

        # On prend la première commune retournée, souvent la plus pertinente
        commune_data = data[0]
        code_departement = commune_data.get("codeDepartement")
        ville_api = commune_data.get("nom")
        # L'API geo.api.gouv.fr/communes?codePostal=... peut retourner une liste de communes
        # Chacune peut avoir son propre "codePostal" si un code postal saisi est ambigu ou correspond à plusieurs entités.
        # On peut utiliser le codePostal de la commune principale retournée ou garder celui saisi s'il est valide.
        # Pour la simplicité ici, on va afficher le nom de la première commune.
        # Le code_postal_api sera celui saisi car c'est ce qu'on a vérifié.

        if not code_departement or not ville_api:
            default_return["message"] = "Données de localisation incomplètes reçues de l'API."
            return default_return

        region_calculee = "idf" if code_departement in IDF_DEPARTEMENTS else "hors_idf"

        return {
            "valide": True,
            "code_postal_api": code_postal_saisi,  # On garde le CP saisi s'il est validé par l'API
            "ville": ville_api,
            "region": region_calculee,
            "message": f"Localisation : {ville_api} ({code_postal_saisi})"
        }

    except requests.exceptions.Timeout:
        default_return["message"] = "Délai d'attente dépassé en contactant le service de localisation."
        return default_return
    except requests.exceptions.RequestException as e:  # Inclut HTTPError, ConnectionError, etc.
        if response and response.status_code == 404:  # Spécifique pour CP non trouvé
            default_return["message"] = f"Le code postal '{code_postal_saisi}' n'a pas été trouvé."
        else:
            default_return["message"] = f"Erreur de communication avec le service de localisation (geo.api): {e}"
        return default_return
    except Exception as e:  # Autres erreurs (ex: parsing JSON si réponse inattendue)
        default_return["message"] = f"Une erreur inattendue est survenue lors de la localisation: {e}"
        return default_return


# --- Fonctions de Calcul (determiner_categorie, calculer_aide_maprimereno, etc. restent inchangées) ---
def determiner_categorie(region_localisation, personnes, revenu):
    if region_localisation not in SEUILS:
        return None, "Région de localisation invalide pour les seuils.", None
    if not isinstance(personnes, int) or personnes < 1:
        return None, "Nombre de personnes invalide.", None
    if not isinstance(revenu, (int, float)) or revenu < 0:
        return None, "Revenu fiscal invalide.", None

    seuils_region = SEUILS[region_localisation]
    if personnes <= 5:
        seuils_perso = seuils_region.get(personnes)
    else:
        base = seuils_region[5];
        supp = seuils_region["supplémentaire"]
        seuils_perso = [(base[i] + supp[i] * (personnes - 5)) for i in range(3)]

    if not seuils_perso: return None, "Erreur calcul des seuils.", None

    if revenu <= seuils_perso[0]:
        cat, cat_d = "très_modestes", "revenus très modestes"
    elif revenu <= seuils_perso[1]:
        cat, cat_d = "modestes", "revenus modestes"
    elif revenu <= seuils_perso[2]:
        cat, cat_d = "intermédiaires", "revenus intermédiaires"
    else:
        cat, cat_d = "supérieurs", "revenus supérieurs"
    return cat, f"Ménage aux {cat_d}", seuils_perso


def calculer_aide_maprimereno(categorie, gain_reel, cout_travaux_ht, cout_travaux_ttc, est_passoire_energetique):
    if not isinstance(gain_reel, int) or gain_reel < 2: return None
    if cout_travaux_ht <= 0:
        return {"plafond_travaux": 0, "taux_base": 0, "taux_avec_bonus": 0, "bonus_applique": False,
                "taux_ecretement": 0, "cout_eligible_ht": 0, "aide_base": 0, "montant_max_aide": 0,
                "aide_finale": 0, "aide_mar_base": 0, "taux_mar": 0,
                "reste_a_charge": cout_travaux_ttc, "ecretement_applique": False}

    if gain_reel == 2:
        type_gain = "gain_2_classes"
    elif gain_reel == 3:
        type_gain = "gain_3_classes"
    else:
        type_gain = "gain_4_classes_ou_plus"

    plafond = PLAFONDS_TRAVAUX.get(type_gain, 0)
    taux_base_dec = TAUX_FINANCEMENT.get(categorie, {}).get(type_gain, 0)
    taux_final_dec = taux_base_dec + BONUS_SORTIE_PASSOIRE if est_passoire_energetique else taux_base_dec
    cout_eligible_ht = min(cout_travaux_ht, plafond)
    aide_brute = cout_eligible_ht * taux_final_dec
    taux_ecret_dec = TAUX_ECRETEMENT.get(categorie, 0)
    montant_max_aide_ttc = cout_travaux_ttc * taux_ecret_dec
    aide_nette_mpr = min(aide_brute, montant_max_aide_ttc)
    ecretement_applique = aide_brute > aide_nette_mpr
    taux_mar_dec_pour_calcul = PRISE_EN_CHARGE_MAR.get(categorie, 0)
    aide_mar_base = round(min(PLAFOND_MAR * taux_mar_dec_pour_calcul, PLAFOND_MAR), 2)
    reste_a_charge_mpr = round(cout_travaux_ttc - aide_nette_mpr, 2)
    return {"plafond_travaux": plafond, "taux_base": taux_base_dec * 100,
            "taux_avec_bonus": taux_final_dec * 100, "bonus_applique": est_passoire_energetique,
            "taux_ecretement": taux_ecret_dec * 100, "cout_eligible_ht": round(cout_eligible_ht, 2),
            "aide_base": round(aide_brute, 2), "montant_max_aide": round(montant_max_aide_ttc, 2),
            "aide_finale": round(aide_nette_mpr, 2), "aide_mar_base": aide_mar_base,
            "taux_mar": taux_mar_dec_pour_calcul * 100, "reste_a_charge": reste_a_charge_mpr,
            "ecretement_applique": ecretement_applique}


def valider_performance(classe_actuelle, classe_apres):
    if classe_actuelle not in CLASSES_ORDRE_INV or classe_apres not in CLASSES_ORDRE_INV:
        return False, 0, "Classes énergétiques invalides."
    index_actuel = CLASSES_ORDRE_INV[classe_actuelle];
    index_apres = CLASSES_ORDRE_INV[classe_apres]
    gain_reel = index_apres - index_actuel
    if gain_reel <= 0: return False, gain_reel, "Classe visée doit être meilleure que l'actuelle."
    if gain_reel < 2: return False, gain_reel, f"Gain insuffisant ({gain_reel} cl.). Min. 2 classes."
    if classe_actuelle in ["F", "G"] and index_apres < CLASSES_ORDRE_INV["C"]:
        return False, gain_reel, f"Classe visée ({classe_apres}) trop basse : min C si départ {classe_actuelle}."
    elif classe_actuelle == "E" and index_apres < CLASSES_ORDRE_INV["B"]:
        return False, gain_reel, f"Classe visée ({classe_apres}) trop basse : min B si départ E."
    return True, gain_reel, f"Gain de {gain_reel} classes et classe finale {classe_apres} valides."


def calculer_cout_total_travaux(postes_selectionnes, tva_taux=0.055):
    cout_total_ht = 0.0
    if not isinstance(postes_selectionnes, list): return 0.0, 0.0
    for poste in postes_selectionnes:
        if not isinstance(poste, dict) or 'id' not in poste or 'type' not in poste: continue
        poste_id = poste['id'];
        poste_type = poste['type']
        if poste_type == 'fixe':
            cout_total_ht += PRIX_POSTES_TRAVAUX_HT.get(poste_id, 0)
        elif poste_type == 'variable':
            surface = poste.get('surface', 0);
            cout_m2_ht = poste.get('cout_m2_ht', 0)
            if isinstance(surface, (int, float)) and isinstance(cout_m2_ht,
                                                                (int, float)) and surface > 0 and cout_m2_ht > 0:
                cout_total_ht += surface * cout_m2_ht
        elif poste_type == 'manuel':
            cout_saisi_ht = poste.get('cout_total_ht', 0)
            if isinstance(cout_saisi_ht, (int, float)) and cout_saisi_ht > 0:
                cout_total_ht += cout_saisi_ht
    cout_total_ht_arrondi = round(cout_total_ht, 2)
    cout_total_ttc_arrondi = round(cout_total_ht_arrondi * (1 + tva_taux), 2)
    return cout_total_ht_arrondi, cout_total_ttc_arrondi