# main.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

try:
    import cee_functions as cf
except ImportError:
    st.error("ERREUR : Le fichier 'cee_functions.py' est introuvable...")
    st.stop()

st.set_page_config(page_title="Calculateur MaPrimeRénov' Ampleur", page_icon="✨", layout="wide",
                   initial_sidebar_state="collapsed")
st.markdown("""<style>
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; }
    .main-title { text-align: center; font-size: 2.6rem; color: #1E3A8A; margin-bottom: 0.5rem; font-weight: 800; letter-spacing: -1px; }
    .sub-header { text-align: center; font-size: 1.3rem; color: #3B82F6; margin-bottom: 2rem; font-weight: 300; }
    .section-title { color: #1E3A8A; font-size: 1.6rem; border-bottom: 3px solid #60A5FA; padding-bottom: 0.6rem; margin: 1.8rem 0 1.2rem 0; font-weight: 700; }
    .info-box { background-color: #EFF6FF; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 6px solid #3B82F6; box-shadow: 0 3px 10px rgba(0,0,0,0.05); color: #374151; line-height: 1.6; }
    .result-container { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #D1D5DB; }
    .card { background-color: white; padding: 1.8rem; border-radius: 10px; box-shadow: 0 4px 12px -1px rgba(0, 0, 0, 0.08), 0 2px 8px -1px rgba(0, 0, 0, 0.04); margin-bottom: 1.8rem; border: 1px solid #E5E7EB; }
    .card-header { font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 1px solid #E5E7EB;}
    .success-box { background-color: #ECFDF5; color: #065F46; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #10B981; font-weight: 500;}
    .warning-box { background-color: #FFFBEB; color: #92400E; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #F59E0B; font-weight: 500;}
    .error-box { background-color: #FEF2F2; color: #991B1B; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #EF4444; font-weight: 500;}
    .info-alert-box { background-color: #EFF6FF; color: #1E40AF; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #3B82F6; font-weight: 500;}
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 1rem 1.2rem; border-radius: 8px; margin-bottom: 1rem; border-left: 6px solid #60A5FA; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stMetric"] label p { font-weight: 600; color: #4B5563; font-size: 0.85rem; /* Légèrement réduit */ text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem;}
    div[data-testid="stMetric"] div div { font-size: 1.5em; /* Réduit */ font-weight: 700; color: #1F2937; line-height: 1.2;}
    div[data-testid="stMetric"]:nth-of-type(1) { border-left-color: #10B981; } div[data-testid="stMetric"]:nth-of-type(1) div div { color: #047857; }
    div[data-testid="stMetric"]:nth-of-type(3) { border-left-color: #10B981; } div[data-testid="stMetric"]:nth-of-type(3) div div { color: #047857; }
    div[data-testid="stMetric"]:nth-of-type(4) { border-left-color: #EF4444; } div[data-testid="stMetric"]:nth-of-type(4) div div { color: #B91C1C; }
    .classe-a { background-color: #16A34A; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-b { background-color: #84CC16; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-c { background-color: #FACC15; color: #422006; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-d { background-color: #F97316; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-e { background-color: #EA580C; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-f { background-color: #DC2626; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-g { background-color: #BE123C; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .footer-section { text-align: center; color: #6B7280; font-size: 0.85rem; margin-top: 3rem; padding: 1.5rem; border-top: 1px solid #E5E7EB; background-color: #F9FAFB; }
    .stButton>button { border-radius: 8px; padding: 0.7rem 1.8rem; font-weight: 600; font-size: 1.05rem; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .stButton>button:disabled { background-color: #E5E7EB !important; color: #9CA3AF !important; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; padding-bottom: 0.8rem;}
    .stTabs [data-baseweb="tab-list"] { border-bottom-color: #D1D5DB !important; margin-bottom: 1.5rem;}
    div[data-testid="stExpander"] details { border: 1px solid #D1D5DB; border-radius: 8px; box-shadow: none; margin-bottom: 1rem; }
    div[data-testid="stExpander"] summary { font-weight: 600; color: #1E3A8A; padding: 0.8rem 1rem;}
    div[data-testid="stExpander"] summary:hover { background-color: #F3F4F6;}
    .location-info { font-size: 0.9em; margin-top: -0.8rem; margin-bottom: 0.5rem; padding: 0.3rem 0.6rem; border-radius: 4px;}
    .location-success { background-color: #E0F2FE; color: #0C4A6E; border-left: 3px solid #3B82F6;}
    .location-error { background-color: #FEF3C7; color: #723B13; border-left: 3px solid #FBBF24;}
</style>""", unsafe_allow_html=True)

LISTE_POSTES_TRAVAUX = [
    {"id": "pac_eau_eau_geo", "label": "Pompe à chaleur eau/eau géothermique", "type": "fixe",
     "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('pac_eau_eau_geo', 0):,} €"},
    {"id": "chaudiere_granules", "label": "Chaudière à granulés", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('chaudiere_granules', 0):,} €"},
    {"id": "chaudiere_buches", "label": "Chaudière à bûches", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('chaudiere_buches', 0):,} €"},
    {"id": "ssc", "label": "Système solaire combiné (SSC)", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('ssc', 0):,} €"},
    {"id": "pac_air_eau", "label": "Pompe à chaleur air/eau", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('pac_air_eau', 0):,} €"},
    {"id": "cesi", "label": "Chauffe-eau solaire individuel (CESI)", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('cesi', 0):,} €"},
    {"id": "insert_buches_granules", "label": "Insert (bûches ou granulés)", "type": "fixe",
     "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('insert_buches_granules', 0):,} €"},
    {"id": "panneau_solaire_hybride_eau", "label": "Panneau solaire hybride à eau", "type": "fixe",
     "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('panneau_solaire_hybride_eau', 0):,} €"},
    {"id": "chauffe_eau_thermo", "label": "Chauffe-eau thermodynamique", "type": "fixe", "categorie": "Chauffage/ECS",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('chauffe_eau_thermo', 0):,} €"},
    {"id": "isolation_combles", "label": "Isolation des combles", "type": "variable",
     "inputs_def": {"surface_label": "Surface combles (m²)", "cout_m2_label": "Coût HT/m² (€)"},
     "categorie": "Isolation"},
    {"id": "isolation_plancher_bas", "label": "Isolation des planchers bas", "type": "variable",
     "inputs_def": {"surface_label": "Surface planchers bas (m²)", "cout_m2_label": "Coût HT/m² (€)"},
     "categorie": "Isolation"},
    {"id": "isolation_murs", "label": "Isolation des murs (ITE/ITI)", "type": "variable",
     "inputs_def": {"surface_label": "Surface murs (m²)", "cout_m2_label": "Coût HT/m² (€)"}, "categorie": "Isolation"},
    {"id": "menuiseries", "label": "Remplacement des menuiseries", "type": "manuel",
     "inputs_def": {"cout_total_ht_label": "Coût total HT menuiseries (€)",
                    "surface_label": "Surface menuiseries (m², optionnel)"}, "categorie": "Isolation"},
    {"id": "vmc_double_flux", "label": "VMC double flux", "type": "fixe", "categorie": "Ventilation",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('vmc_double_flux', 0):,} €"},
    {"id": "depose_cuve_fioul", "label": "Dépose de cuve fioul", "type": "fixe", "categorie": "Autres",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('depose_cuve_fioul', 0):,} €"},
    {"id": "audit_energetique", "label": "Audit énergétique (si facturé séparément)", "type": "fixe",
     "categorie": "Autres",
     "aide_text": f"Coût estimé HT: {cf.PRIX_POSTES_TRAVAUX_HT.get('audit_energetique', 0):,} €"},
]

if 'cp_input' not in st.session_state: st.session_state.cp_input = ""
if 'pers_input' not in st.session_state: st.session_state.pers_input = 2
if 'rev_input' not in st.session_state: st.session_state.rev_input = 30000.0
if 'cl_act_input' not in st.session_state: st.session_state.cl_act_input = 'G'
if 'cl_apr_input' not in st.session_state: st.session_state.cl_apr_input = 'B'
if 'deux_etapes_input' not in st.session_state: st.session_state.deux_etapes_input = False
if 'tva_input' not in st.session_state: st.session_state.tva_input = 5.5
if 'mar_input' not in st.session_state: st.session_state.mar_input = True
if 'indigne_input' not in st.session_state: st.session_state.indigne_input = False
if 'localisation_info' not in st.session_state:
    st.session_state.localisation_info = {"valide": False, "code_postal_api": None, "ville": None, "region": None,
                                          "message": ""}
if 'last_checked_cp' not in st.session_state: st.session_state.last_checked_cp = None
if 'travaux_inputs' not in st.session_state: st.session_state.travaux_inputs = {}
for poste in LISTE_POSTES_TRAVAUX:
    poste_id = poste['id']
    if f"select_{poste_id}" not in st.session_state: st.session_state[f"select_{poste_id}"] = False
    if poste['type'] == 'variable':
        if f"{poste_id}_surface" not in st.session_state.travaux_inputs: st.session_state.travaux_inputs[
            f"{poste_id}_surface"] = 0.0
        if f"{poste_id}_cout_m2_ht" not in st.session_state.travaux_inputs: st.session_state.travaux_inputs[
            f"{poste_id}_cout_m2_ht"] = 0.0
    elif poste['type'] == 'manuel':
        if f"{poste_id}_cout_total_ht" not in st.session_state.travaux_inputs: st.session_state.travaux_inputs[
            f"{poste_id}_cout_total_ht"] = 0.0
        if "surface_label" in poste.get("inputs_def", {}):
            if f"{poste_id}_surface_menuiseries" not in st.session_state.travaux_inputs:
                st.session_state.travaux_inputs[f"{poste_id}_surface_menuiseries"] = 0.0


def afficher_alerte(message, type_alerte="info"):
    icon_map = {"success": "✅", "warning": "⚠️", "error": "❌", "info": "ℹ️"}
    st.markdown(f'<div class="{type_alerte}-box">{icon_map.get(type_alerte, "ℹ️")} {message}</div>',
                unsafe_allow_html=True)


def formatter_classe(classe):
    return f'<span class="classe-{classe.lower()}">{classe}</span>'


def creer_graphique_financement(aide_mpr, reste_charge, ttc, aide_mar=0):
    labels = ['Aide MPR', 'Aide MAR', 'Reste à charge'];
    values = [aide_mpr, aide_mar, reste_charge]
    valid_indices = [i for i, v in enumerate(values) if v > 0];
    labels = [labels[i] for i in valid_indices];
    values = [values[i] for i in valid_indices]
    colors_map = {'Aide MPR': '#10B981', 'Aide MAR': '#3B82F6', 'Reste à charge': '#EF4444'};
    colors = [colors_map.get(l, '#9CA3AF') for l in labels]
    if not values: return go.Figure()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.45,
                                 marker=dict(colors=colors, line=dict(color='#ffffff', width=1.5)), textinfo='percent',
                                 hoverinfo='label+value+percent', insidetextorientation='radial',
                                 pull=[0.04] * len(labels), sort=False)])
    fig.update_traces(textfont_size=13, textposition='outside')
    fig.update_layout(
        title={'text': "Répartition du Financement", 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
               'font_size': 18, 'font_color': '#111827'}, height=420, margin=dict(l=10, r=10, t=60, b=10),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font_size=11))
    fig.add_annotation(text=f"<b>Total:<br>{ttc:,.0f} €</b>", align='center', showarrow=False,
                       font=dict(size=16, color="#1F2937"), x=0.5, y=0.5)
    return fig


col_h1, col_h2 = st.columns([3, 1])
with col_h1: st.markdown("<h1 class='main-title'>✨ Simulateur MaPrimeRénov' Ampleur ✨</h1>",
                         unsafe_allow_html=True); st.markdown(
    "<p class='sub-header'>Estimez vos aides pour une rénovation énergétique performante</p>", unsafe_allow_html=True)
with col_h2: st.markdown(
    "<div class='profile-section' style='margin-top:1rem;'><img src='https://st3.depositphotos.com/1026550/15275/i/450/depositphotos_152750910-stock-photo-environment-conservation-concept.jpg' class='profile-image' alt='Profil'><div class='profile-text'><strong>Sadou BARRY</strong><br>Passionné par l’Éco-Rénovation & la Transition Énergétique<br><a href='https://www.linkedin.com/in/sadou-barry-881868164/' target='_blank'>Contactez-moi sur LinkedIn</a></div></div>",
    unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 **Calculateur**", "ℹ️ **Infos Utiles**", "❓ **FAQ**"])

with tab1:
    st.markdown("<h2 class='section-title'>1. Informations générales</h2>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1.2, 1, 0.8])
        with col1:
            st.markdown("<h6>👤 Ménage <span style='color:red;'>*</span></h6>", unsafe_allow_html=True)
            st.text_input("Code postal", max_chars=5, key="cp_input")
            if st.session_state.cp_input and \
                    (st.session_state.cp_input != st.session_state.last_checked_cp or \
                     not st.session_state.localisation_info.get("ville")):
                with st.spinner("Vérification du code postal..."):
                    st.session_state.localisation_info = cf.get_info_localisation(st.session_state.cp_input)
                st.session_state.last_checked_cp = st.session_state.cp_input
            loc_info = st.session_state.localisation_info
            if st.session_state.cp_input:
                if loc_info.get("valide"):
                    st.markdown(
                        f"<div class='location-info location-success'>Ville : <b>{loc_info.get('ville', 'N/A')}</b> ({loc_info.get('code_postal_api', '')}) - Région : {'IDF' if loc_info.get('region') == 'idf' else 'Hors IDF'}</div>",
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div class='location-info location-error'>{loc_info.get('message', 'Erreur de localisation.')}</div>",
                        unsafe_allow_html=True)
            st.number_input("Personnes foyer", min_value=1, step=1, key="pers_input")
            st.number_input("Revenu fiscal réf. (€)", min_value=0.0, step=100.0, format="%.0f", key="rev_input")
        with col2:
            st.markdown("<h6>⚡ Performance DPE <span style='color:red;'>*</span></h6>", unsafe_allow_html=True)
            st.selectbox("Classe actuelle", cf.CLASSES_ORDRE,
                         index=cf.CLASSES_ORDRE.index(st.session_state.cl_act_input), key="cl_act_input")
            st.selectbox("Classe visée", cf.CLASSES_ORDRE, index=cf.CLASSES_ORDRE.index(st.session_state.cl_apr_input),
                         key="cl_apr_input")
            st.checkbox("Rénovation en 2 étapes", key="deux_etapes_input")
        with col3:
            st.markdown("<h6>⚙️ Options Projet</h6>", unsafe_allow_html=True)
            st.number_input("Taux de TVA applicable (%)", min_value=0.0, step=0.1, format="%.1f", key="tva_input")
            taux_tva_saisi_decimal = st.session_state.tva_input / 100.0
            st.checkbox("Inclure aide Accompagnateur", key="mar_input")
            st.checkbox("Cas d'habitat indigne", key="indigne_input")

    st.markdown("<h2 class='section-title'>2. Détaillez vos travaux <span style='color:red;'>*</span></h2>",
                unsafe_allow_html=True)
    st.markdown("Sélectionnez les postes de travaux envisagés et renseignez les informations demandées.")
    postes_selectionnes_pour_calcul = []
    categories_travaux = sorted(list(set(p['categorie'] for p in LISTE_POSTES_TRAVAUX)))
    exp_cols = st.columns(len(categories_travaux))

    for i, cat_name in enumerate(categories_travaux):
        with exp_cols[i]:
            with st.expander(f"📂 {cat_name}", expanded=(cat_name == "Isolation")):
                for poste_def in [p for p in LISTE_POSTES_TRAVAUX if p['categorie'] == cat_name]:
                    poste_id = poste_def['id']
                    checkbox_key = f"select_{poste_id}"
                    st.checkbox(poste_def['label'], key=checkbox_key, help=poste_def.get('aide_text', None))

                    if st.session_state[checkbox_key]:
                        current_poste_data = {'id': poste_id, 'type': poste_def['type'], 'label': poste_def['label']}
                        if poste_def['type'] == 'variable':
                            inputs_def = poste_def['inputs_def']
                            surf_key = f"{poste_id}_surface";
                            cout_m2_key = f"{poste_id}_cout_m2_ht"
                            st.number_input(inputs_def['surface_label'], min_value=0.0, step=1.0, format="%.1f",
                                            key=surf_key, value=st.session_state.travaux_inputs.get(surf_key, 0.0))
                            st.number_input(inputs_def['cout_m2_label'], min_value=0.0, step=1.0, format="%.0f",
                                            key=cout_m2_key,
                                            value=st.session_state.travaux_inputs.get(cout_m2_key, 0.0))
                            st.session_state.travaux_inputs[surf_key] = st.session_state[surf_key]
                            st.session_state.travaux_inputs[cout_m2_key] = st.session_state[cout_m2_key]
                            current_poste_data['surface'] = st.session_state.travaux_inputs[surf_key]
                            current_poste_data['cout_m2_ht'] = st.session_state.travaux_inputs[cout_m2_key]
                        elif poste_def['type'] == 'manuel':
                            inputs_def = poste_def['inputs_def']
                            cout_total_key = f"{poste_id}_cout_total_ht"
                            st.number_input(inputs_def['cout_total_ht_label'], min_value=0.0, step=100.0, format="%.0f",
                                            key=cout_total_key,
                                            value=st.session_state.travaux_inputs.get(cout_total_key, 0.0))
                            st.session_state.travaux_inputs[cout_total_key] = st.session_state[cout_total_key]
                            current_poste_data['cout_total_ht'] = st.session_state.travaux_inputs[cout_total_key]
                            if "surface_label" in inputs_def:
                                surf_menu_key = f"{poste_id}_surface_menuiseries"
                                st.number_input(inputs_def['surface_label'], min_value=0.0, step=0.1, format="%.1f",
                                                key=surf_menu_key,
                                                value=st.session_state.travaux_inputs.get(surf_menu_key, 0.0))
                                st.session_state.travaux_inputs[surf_menu_key] = st.session_state[surf_menu_key]
                                current_poste_data['surface_menuiseries'] = st.session_state.travaux_inputs[
                                    surf_menu_key]
                        postes_selectionnes_pour_calcul.append(current_poste_data)

    cout_travaux_ht_calcule, cout_travaux_ttc_calcule = cf.calculer_cout_total_travaux(postes_selectionnes_pour_calcul,
                                                                                       tva_taux=taux_tva_saisi_decimal)
    if postes_selectionnes_pour_calcul:
        st.markdown("<h6>💰 Coûts Estimés des Travaux Sélectionnés</h6>", unsafe_allow_html=True)
        cost_col1, cost_col2 = st.columns(2)
        with cost_col1: st.metric(label="Coût Total HT Estimé", value=f"{cout_travaux_ht_calcule:,.0f} €")
        with cost_col2: st.metric(label=f"Coût Total TTC Estimé (TVA {st.session_state.tva_input:.1f}%)",
                                  value=f"{cout_travaux_ttc_calcule:,.0f} €")
        st.markdown("---")

    validation_placeholder = st.container()
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
    calcul_possible = True;
    gain_reel = 0;
    sortie_passoire_atteinte = False;
    messages_validation = []
    if not st.session_state.cp_input:
        calcul_possible = False; messages_validation.append(("warning", "Veuillez saisir un code postal."))
    elif not st.session_state.localisation_info.get("valide"):
        calcul_possible = False; msg_loc = st.session_state.localisation_info.get("message",
                                                                                  "Code postal invalide."); messages_validation.append(
            ("warning", f"Localisation : {msg_loc}"))
    if not isinstance(st.session_state.pers_input,
                      int) or st.session_state.pers_input < 1: calcul_possible = False; messages_validation.append(
        ("warning", "Nombre de personnes invalide."))
    if not isinstance(st.session_state.rev_input, (
    int, float)) or st.session_state.rev_input < 0: calcul_possible = False; messages_validation.append(
        ("warning", "Revenu fiscal invalide."))
    if not postes_selectionnes_pour_calcul:
        calcul_possible = False; messages_validation.append(
            ("warning", "Veuillez sélectionner au moins un poste de travaux."))
    else:
        for poste_calc in postes_selectionnes_pour_calcul:
            if poste_calc['type'] == 'variable' and (
                    poste_calc.get('surface', 0) <= 0 or poste_calc.get('cout_m2_ht', 0) <= 0):
                calcul_possible = False; messages_validation.append(
                    ("warning", f"Pour '{poste_calc['label']}', surface et coût/m² > 0 requis."))
            elif poste_calc['type'] == 'manuel' and poste_calc.get('cout_total_ht', 0) <= 0:
                calcul_possible = False; messages_validation.append(
                    ("warning", f"Pour '{poste_calc['label']}', coût total HT > 0 requis."))
    if cout_travaux_ht_calcule <= 0 and postes_selectionnes_pour_calcul and not any(
        "requis" in msg[1] for msg in messages_validation): calcul_possible = False; messages_validation.append(
        ("warning", "Coût HT total des travaux nul. Vérifiez les saisies."))
    if calcul_possible:
        perf_ok, gain_reel, msg_perf = cf.valider_performance(st.session_state.cl_act_input,
                                                              st.session_state.cl_apr_input)
        if not perf_ok:
            calcul_possible = False; messages_validation.append(("error", msg_perf))
        else:
            validation_placeholder.info(
                f"Gain réel calculé : {gain_reel} classes ({st.session_state.cl_act_input} → {st.session_state.cl_apr_input}).")
            est_passoire = st.session_state.cl_act_input in ["F", "G"];
            index_apres = cf.CLASSES_ORDRE_INV.get(st.session_state.cl_apr_input, -1)
            sortie_passoire_atteinte = est_passoire and index_apres != -1 and index_apres >= cf.CLASSES_ORDRE_INV["D"]
            if sortie_passoire_atteinte:
                messages_validation.append(("success", "Bonus Sortie de Passoire (+10%) applicable."))
            elif est_passoire:
                messages_validation.append(("info", "Pas de Bonus Sortie de Passoire (arrivée < D)."))
            if st.session_state.deux_etapes_input and st.session_state.cl_act_input not in ["G", "F",
                                                                                            "E"]: messages_validation.append(
                ("info", "Info: Rénovation en 2 étapes concerne surtout G/F/E."))
    with validation_placeholder.container():
        messages_validation.sort(key=lambda x: {"error": 0, "warning": 1, "info": 2, "success": 3}.get(x[0], 4))
        for type_msg, msg in messages_validation: afficher_alerte(msg, type_msg)
        if not calcul_possible and not messages_validation: afficher_alerte("Veuillez vérifier toutes vos saisies.",
                                                                            "warning")
    with col_btn2:
        calcul_btn = st.button("🚀 Lancer l'estimation", use_container_width=True, disabled=not calcul_possible,
                               type="primary")

    if calcul_btn and calcul_possible:
        region_code_verifie = st.session_state.localisation_info.get("region")
        categorie, categorie_display, seuils_perso = cf.determiner_categorie(region_code_verifie,
                                                                             st.session_state.pers_input,
                                                                             st.session_state.rev_input)
        if categorie is None:
            afficher_alerte(categorie_display, "error")
        else:
            region_nom = "Île-de-France" if region_code_verifie == "idf" else "Hors Île-de-France"
            resultats = cf.calculer_aide_maprimereno(categorie, gain_reel, cout_travaux_ht_calcule,
                                                     cout_travaux_ttc_calcule, sortie_passoire_atteinte)
            if resultats is None or resultats.get('aide_finale', -1) == -1:
                afficher_alerte("Erreur calcul aide.", "error")
            else:
                aide_mar_effective = 0.0
                if st.session_state.mar_input:
                    taux_mar_dec = resultats["taux_mar"] / 100
                    cout_prestation_mar = cf.PLAFOND_MAR_HABITAT_INDIGNE if st.session_state.indigne_input else cf.PLAFOND_MAR
                    aide_mar_effective = round(cout_prestation_mar * taux_mar_dec, 2)
                aide_finale_mpr = resultats['aide_finale'];
                aide_totale_estimee = round(aide_finale_mpr + aide_mar_effective, 2)
                reste_a_charge_global_estime = round(cout_travaux_ttc_calcule - aide_finale_mpr - aide_mar_effective, 2)

                st.markdown("<h2 class='section-title'>📊 Résultats de votre estimation</h2>", unsafe_allow_html=True)

                col_metrics_area, col_graph_area = st.columns([0.55, 0.45])

                with col_metrics_area:
                    st.markdown("<h6>💰 Montants Estimés</h6>", unsafe_allow_html=True)
                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        st.metric(label="Aide MaPrimeRénov'", value=f"{aide_finale_mpr:,.0f} €")
                        st.metric(label="Aide Totale Estimée", value=f"{aide_totale_estimee:,.0f} €")
                    with m_col2:
                        if st.session_state.mar_input:
                            st.metric(label="Aide Accompagnement (MAR)", value=f"{aide_mar_effective:,.0f} €")
                        else:  # Placeholder pour l'alignement
                            st.markdown("<div style='height: 98px;'></div>", unsafe_allow_html=True)
                        st.metric(label="Reste à Charge Global Estimé", value=f"{reste_a_charge_global_estime:,.0f} €")

                    classe_act_fmt = formatter_classe(st.session_state.cl_act_input);
                    classe_apr_fmt = formatter_classe(st.session_state.cl_apr_input)
                    bonus_msg_res = " (+ Bonus Passoire)" if resultats['bonus_applique'] else "";
                    ecret_msg_res = " (Écrêtement MPR appliqué)" if resultats['ecretement_applique'] else ""
                    st.markdown(
                        f"""<div class='info-alert-box' style='margin-top: 1.5rem;'><strong>Contexte :</strong><br>- Localisation: {st.session_state.localisation_info.get('ville', 'N/A')} ({region_nom})<br>- Profil: {categorie_display}<br>- Performance: {classe_act_fmt} → {classe_apr_fmt} (Gain: <span class="highlight">{gain_reel}</span> cl.){bonus_msg_res}<br>- Coût TTC: {cout_travaux_ttc_calcule:,.0f} €{ecret_msg_res}</div>""",
                        unsafe_allow_html=True)

                with col_graph_area:
                    st.markdown("<h6>📊 Répartition du Financement</h6>", unsafe_allow_html=True)
                    fig = creer_graphique_financement(aide_finale_mpr, reste_a_charge_global_estime,
                                                      cout_travaux_ttc_calcule,
                                                      (aide_mar_effective if st.session_state.mar_input else 0))
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Graphique indisponible.")

                with st.expander("🔍 Voir les détails du calcul et des travaux"):
                    detail_col1, detail_col2 = st.columns(2)
                    with detail_col1:
                        st.markdown("<h6>Calcul Aide MPR</h6>", unsafe_allow_html=True)
                        st.markdown(
                            f"- Ville (vérifiée): {st.session_state.localisation_info.get('ville', 'N/A')} ({st.session_state.localisation_info.get('code_postal_api', 'N/A')})")
                        st.markdown(
                            f"- Catégorie : {categorie_display.split(' aux ')[1] if ' aux ' in categorie_display else categorie_display}")
                        st.markdown(f"- Gain réel utilisé : {gain_reel} classes");
                        st.markdown(f"- Plafond HT travaux applicable: {resultats['plafond_travaux']:,.0f} €")
                        st.markdown(f"- Taux base MPR: {resultats['taux_base']:.0f}%");
                        st.markdown(
                            f"- Bonus sortie passoire : {'Oui (+10%)' if resultats['bonus_applique'] else 'Non'}")
                        st.markdown(f"- Taux MPR appliqué (avec bonus): {resultats['taux_avec_bonus']:.0f}%");
                        st.markdown(f"- Coût travaux HT éligible MPR: {resultats['cout_eligible_ht']:,.2f} €")
                        st.markdown(f"- Aide MPR avant écrêtement : {resultats['aide_base']:,.2f} €");
                        st.markdown(f"- Taux écrêtement MPR: {resultats['taux_ecretement']:.0f}% du TTC travaux")
                        st.markdown(f"- Aide MPR max. après écrêt. : {resultats['montant_max_aide']:,.2f} €");
                        st.markdown(f"- **Aide finale MPR : {aide_finale_mpr:,.2f} €**")
                        if st.session_state.mar_input:
                            cout_prestation_mar_effective = cf.PLAFOND_MAR_HABITAT_INDIGNE if st.session_state.indigne_input else cf.PLAFOND_MAR
                            st.markdown("<h6>Calcul Aide Mon Accompagnateur Rénov' (MAR)</h6>", unsafe_allow_html=True)
                            st.markdown(f"- Coût prestation MAR estimé: {cout_prestation_mar_effective:,.0f} €");
                            st.markdown(f"- Taux prise en charge MAR: {resultats['taux_mar']:.0f}%")
                            st.markdown(f"- **Aide MAR : {aide_mar_effective:,.2f} €**")
                        st.markdown("<h6>Récapitulatif des Coûts Travaux</h6>", unsafe_allow_html=True)
                        if postes_selectionnes_pour_calcul:
                            for poste_detail in postes_selectionnes_pour_calcul:
                                cost_ht_detail = 0
                                if poste_detail['type'] == 'fixe':
                                    cost_ht_detail = cf.PRIX_POSTES_TRAVAUX_HT.get(poste_detail['id'], 0)
                                elif poste_detail['type'] == 'variable':
                                    cost_ht_detail = poste_detail.get('surface', 0) * poste_detail.get('cout_m2_ht', 0)
                                elif poste_detail['type'] == 'manuel':
                                    cost_ht_detail = poste_detail.get('cout_total_ht', 0)
                                st.markdown(f"- {poste_detail['label']}: {cost_ht_detail:,.0f} € HT")
                            st.markdown(f"<strong>- Total Travaux HT: {cout_travaux_ht_calcule:,.0f} € HT</strong>");
                            st.markdown(
                                f"<strong>- Total Travaux TTC ({st.session_state.tva_input:.1f}%): {cout_travaux_ttc_calcule:,.0f} € TTC</strong>")
                        else:
                            st.markdown("- Aucun travaux sélectionné.")
                    with detail_col2:
                        st.markdown("<h6>Votre Catégorie de Revenus</h6>", unsafe_allow_html=True)
                        st.markdown(f"Région : {region_nom}, Foyer : {st.session_state.pers_input} personne(s)")
                        if seuils_perso and len(seuils_perso) == 3:
                            seuils_formatted = [f"≤ {s:,.0f} €" for s in seuils_perso] + [f"> {seuils_perso[2]:,.0f} €"]
                            data_seuils = {"Catégorie": ["Très modestes", "Modestes", "Intermédiaires", "Supérieurs"],
                                           "Plafond Revenus 2025": seuils_formatted}
                            df_seuils = pd.DataFrame(data_seuils);
                            st.table(df_seuils)
                        else:
                            st.warning("Impossible d'afficher le tableau des seuils.")

with tab2:
    st.markdown("<h2 class='section-title'>ℹ️ Informations utiles</h2>", unsafe_allow_html=True)
    info_tab1, info_tab2, info_tab3, info_tab4 = st.tabs(
        ["Taux & Plafonds", "Rénovation en 2 étapes", "Accompagnement", "Conditions Clés"])
    with info_tab1:
        st.markdown("<h5>Taux de financement 2025 (% du HT plafonné)</h5>", unsafe_allow_html=True);
        html_table_taux = """<table class="styled-table"><thead><tr><th>Catégorie</th><th>Gain 2 cl.</th><th>Gain 3 cl.</th><th>Gain 4+ cl.</th><th>Bonus Passoire</th><th>Écrêtement (% TTC)</th></tr></thead><tbody><tr><td>Très modestes</td><td>80%</td><td>80%</td><td>80%</td><td>+10%</td><td>100%</td></tr><tr><td>Modestes</td><td>60%</td><td>60%</td><td>60%</td><td>+10%</td><td>80%*</td></tr><tr><td>Intermédiaires</td><td>45%</td><td>50%</td><td>50%</td><td>+10%</td><td>80%</td></tr><tr><td>Supérieurs</td><td>10%</td><td>15%</td><td>20%</td><td>+10%</td><td>50%</td></tr></tbody></table><p style="font-size: 0.85rem; margin-top: 0.5rem;">*Taux écrêtement Modestes susceptible de passer à 90% (attente décret).</p>""";
        st.markdown(html_table_taux, unsafe_allow_html=True)
        st.markdown("<h5>Plafonds de travaux HT</h5>", unsafe_allow_html=True);
        plafonds_html = """<table class="styled-table"><thead><tr><th>Gain énergétique</th><th>Plafond HT</th></tr></thead><tbody><tr><td>Gain de 2 classes</td><td>40 000 €</td></tr><tr><td>Gain de 3 classes</td><td>55 000 €</td></tr><tr><td>Gain de 4 classes ou plus</td><td>70 000 €</td></tr></tbody></table>""";
        st.markdown(plafonds_html, unsafe_allow_html=True)
        st.markdown("<h6>Bonus Sortie de Passoire (+10%)</h6>", unsafe_allow_html=True);
        st.markdown("Si logement initial F/G ET final D, C, B ou A.")
    with info_tab2:
        st.markdown("<h5>La rénovation en deux étapes</h5>", unsafe_allow_html=True);
        st.markdown(
            "- Possible sur 5 ans max. pour départs G, F, E.\n- **Objectif final minimum après 2ème étape :** Classe **C** (si départ G/F) ou **B** (si départ E).\n- Calcul aide 2ème étape basé sur gain total et dépenses cumulées.\n- Pas de bonus passoire sur la 2ème étape.")
        try:
            st.image(
                "https://user-images.githubusercontent.com/118736018/299179280-6229d60b-0c2d-4233-b2cd-a1a1b2bfa534.png",
                caption="Schéma indicatif de la rénovation en deux étapes")
        except Exception:
            st.warning("Impossible d'afficher le schéma.")
    with info_tab3:
        st.markdown("<h5>Mon Accompagnateur Rénov' (MAR)</h5>", unsafe_allow_html=True);
        st.markdown(
            "- **Obligatoire** pour MPR Ampleur.\n- **Prise en charge (plafond prestation 2000€, ou 4000€ si habitat indigne):** 100% (Très Modestes), 80% (Modestes), 40% (Intermédiaires), 20% (Supérieurs).\n- Cette aide MAR est calculée sur le coût de la prestation d'accompagnement.")
    with info_tab4:
        st.markdown("<h5>Conditions Clés pour MPR Ampleur</h5>", unsafe_allow_html=True);
        st.markdown(
            "- **Gain minimum réel :** 2 classes énergétiques.\n- **Classe finale minimum réelle :** C (si départ G/F), B (si départ E) (condition réglementaire).\n- **Gestes obligatoires :** Au moins 2 gestes d'isolation thermique (cette condition n'est pas vérifiée par ce simulateur mais est cruciale).\n- **Accompagnement :** Recours à MAR obligatoire.\n- **Entreprises :** Qualifiées RGE.")
        afficher_alerte("Ce simulateur est indicatif. Contactez un conseiller France Rénov' ou un MAR agréé.", "info")

with tab3:
    st.markdown("<h2 class='section-title'>❓ Questions fréquentes</h2>", unsafe_allow_html=True)
    faq_col1, faq_col2 = st.columns(2)
    with faq_col1:
        with st.expander("MPR Ampleur, c'est quoi ?"): st.markdown(
            "L'aide pour les rénovations globales avec ≥ 2 classes de gain et accompagnement obligatoire.")
        with st.expander("Comment est calculé le gain ?"): st.markdown(
            "Différence entre classe avant et après travaux (ex: F -> C = 3 classes). L'aide dépend du gain *réel* calculé.")
        with st.expander("Qui est Mon Accompagnateur Rénov' ?"): st.markdown(
            "Professionnel agréé obligatoire qui aide de l'audit au suivi des travaux.")
    with faq_col2:
        with st.expander("L'écrêtement, c'est quoi ?"): st.markdown(
            "Plafond de l'aide MPR basé sur un % du coût TTC des travaux (variable selon les revenus).")
        with st.expander("Cumul possible avec d'autres aides ?"): st.markdown(
            "Oui avec Éco-PTZ, aides locales, TVA 5.5%. Non cumulable avec les CEE classiques ou MPR par geste pour les mêmes travaux.")
        with st.expander("Rénovation en 2 étapes ?"): st.markdown(
            "Pour G/F/E sur 5 ans max. Atteindre C (si G/F) ou B (si E) minimum à la fin. Voir MAR pour détails.")

st.markdown(
    """---<div class="footer-section"><p>Barèmes et règles 2025 (selon infos disponibles Mars 2025). Calculateur indicatif non contractuel.</p><p>Infos officielles : <a href="https://france-renov.gouv.fr" target="_blank">france-renov.gouv.fr</a> | 0 808 800 700 (service gratuit + prix appel).</p><p>© 2025 - Conçu avec ❤️ par Sadou BARRY</p></div>""",
    unsafe_allow_html=True)