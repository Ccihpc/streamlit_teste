import streamlit as st

def morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status):
    score = 0
    if history_of_falls:
        score += 25
    if secondary_diagnosis:
        score += 15
    if ambulatory_aid == "Muletas/Bengala/Andador":
        score += 15
    elif ambulatory_aid == "Mobilidade/Parede":
        score += 30
    if IV_heparin:
        score += 20
    if mobility == "Fraca":
        score += 10
    elif mobility == "Comprometida/Cambaleante":
        score += 20
    if mental_status:
        score += 15
    return score

def risk_category(score):
    if score >= 51:
        return "Risco muito elevado"
    elif score >= 41:
        return "Risco elevado"
    else:
        return "Risco médio"


# Alterando a função evaruci_scale_score
def evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility, other_factors_points, weeks_points):
    score = consciousness + hemodynamics + respiratory + mobility + other_factors_points + weeks_points
    return max(4, score)


def evaruci_risk_category(score):
    if score == 4:
        return "Risco mínimo"
    elif score > 4:
        return "Risco médio"
    else:
        return "Risco máximo"

st.set_page_config(page_title="Avaliação de Risco de Lesão por Pressão", page_icon="✅")
st.title("Avaliação de Risco de Lesão por Pressão em Cuidados Intensivos")

# Escala de Morse
st.subheader("Escala de Morse")
history_of_falls = st.checkbox("Histórico de Quedas (25 pontos)")
secondary_diagnosis = st.checkbox("Diagnóstico Secundário (15 pontos)")
ambulatory_aid = st.selectbox("Uso de Dispositivo de Auxílio à Deambulação", ["Nenhum/Acamado/Auxiliado por Profissional de Saúde", "Muletas/Bengala/Andador", "Mobilidade/Parede"])
IV_heparin = st.checkbox("Presença de Soro Intravenoso (IV) ou Heparina (20 pontos)")
mobility = st.selectbox("Marcha", ["Normal/Sem deambulação, Acamado, Cadeira de Rodas (0 pontos)", "Fraca (10 pontos)", "Comprometida/Cambaleante (20 pontos)"])
mental_status = st.checkbox("Estado Mental: Superestima capacidade/Esquece limitações (15 pontos)")

st.write("<hr>", unsafe_allow_html=True)

# Escala EVARUCI
st.subheader("Escala EVARUCI")
consciousness_options = {"Consciente (1 ponto)": 1, "Colaborativo (2 pontos)": 2, "Reativo (3 pontos)": 3, "Arreativo (4 pontos)": 4}
consciousness = st.selectbox("Consciência", list(consciousness_options.keys()), format_func=lambda x: x.split("(")[0].strip())
hemodynamics_options = {"Sem suporte (1 ponto)": 1, "Com expansão (2 pontos)": 2, "Com dopamina ou dobutamina (3 pontos)": 3, "Com adrenalina ou noradrenalina (4 pontos)": 4}
hemodynamics = st.selectbox("Hemodinâmica", list(hemodynamics_options.keys()), format_func=lambda x: x.split("(")[0].strip())
respiratory_options = {"Com baixa necessidade de O2 (1 ponto)": 1, "Com alta necessidade de O2 (2 pontos)": 2, "Com suporte respiratório (3 pontos)": 3, "Com ventilação mecânica invasiva (4 pontos)": 4}
respiratory = st.selectbox("Respiratório", list(respiratory_options.keys()), format_func=lambda x: x.split("(")[0].strip())
mobility_options = {"Independente (1 ponto)": 1, "Dependente mas se movimenta (2 pontos)": 2, "Pouca mobilidade (3 pontos)": 3, "Sem mobilidade (4 pontos)": 4}
mobility_evaruci = st.selectbox("Mobilidade", list(mobility_options.keys()), format_func=lambda x: x.split("(")[0].strip())

# Fatores adicionais
other_factors = {
    "Temperatura ≥38˚C (1 ponto)": st.checkbox("Temperatura ≥38˚C"),
    "Saturação de O2 < 90% (1 ponto)": st.checkbox("Saturação de O2 < 90%"),
    "PA sistólica < 100 mmHg (1 ponto)": st.checkbox("PA sistólica < 100 mmHg"),
    "Estado da pele (1 ponto)": st.checkbox("Estado da pele"),
    "Paciente em prona (1 ponto)": st.checkbox("Paciente em prona")
}

# Cálculo do total de pontos dos fatores adicionais
total_points_from_other_factors = sum(value for value in other_factors.values())

weeks_options = ["Nenhuma", "1ª Semana", "2ª Semana", "3ª Semana", "4ª Semana"]
weeks = st.selectbox("Semanas em risco", weeks_options)

# Atualização da lógica para pontuação das semanas
weeks_values = {"Nenhuma": 0, "1ª Semana": 0.5, "2ª Semana": 1, "3ª Semana": 1.5, "4ª Semana": 2}
week_points = weeks_values[weeks]

calculate_button = st.button("Calcular Pontuações")


if calculate_button:
    morse_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)
    evaruci_score = evaruci_scale_score(consciousness_options[consciousness], hemodynamics_options[hemodynamics], respiratory_options[respiratory], mobility_options[mobility_evaruci], total_points_from_other_factors, week_points)


    st.write("<hr>", unsafe_allow_html=True)
    st.subheader("Resultados da Escala de Morse")
    st.write(f"Pontuação total da Escala de Morse: **{morse_score}**")
    st.write(f"Categoria de risco: **{risk_category(morse_score)}**")
    
    st.write("<hr>", unsafe_allow_html=True)
    st.subheader("Resultados da Escala EVARUCI")
    st.write(f"Pontuação total da Escala EVARUCI: **{evaruci_score}**")
    st.write(f"Categoria de risco: **{evaruci_risk_category(evaruci_score)}**")
