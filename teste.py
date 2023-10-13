import streamlit as st

def morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status):
    score = 0
    if history_of_falls == "Sim":
        score += 25
    if secondary_diagnosis == "Sim":
        score += 15
    if ambulatory_aid == "Muletas/Bengala/Andador":
        score += 15
    if ambulatory_aid == "Mobilidade/Parede":
        score += 30
    if IV_heparin == "Sim":
        score += 20
    if mobility == "Fraca":
        score += 10
    elif mobility == "Comprometida/Cambaleante":
        score += 20
    if mental_status == "Superestima capacidade/Esquece limitações":
        score += 15
    return score

def evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility, skin_condition, other_factors, length_of_stay):
    score = consciousness + hemodynamics + respiratory + mobility + skin_condition + other_factors
    score += 0.5 * min(length_of_stay, 4)  # Adiciona 0,5 ponto para cada semana de internação, até 2 pontos
    return score

def risk_category(score):
    if score >= 45:
        return "Alto Risco"
    elif score >= 25:
        return "Moderado Risco"
    else:
        return "Baixo Risco"

st.title("Avaliação de Risco de Lesão por Pressão em Cuidados Intensivos")
st.subheader("Escala de Morse")

history_of_falls = st.radio("Histórico de Quedas", ("Não", "Sim"))
secondary_diagnosis = st.radio("Diagnóstico Secundário", ("Não", "Sim"))
ambulatory_aid = st.radio("Auxílio na Deambulação", ("Nenhum/Acamado/Auxiliado por Profissional de Saúde", "Muletas/Bengala/Andador", "Mobilidade/Parede"))
IV_heparin = st.radio("Presença de Soro Intravenoso (IV) ou Heparina", ("Não", "Sim"))
mobility = st.radio("Marcha", ("Normal/Sem deambulação, Acamado, Cadeira de Rodas", "Fraca", "Comprometida/Cambaleante"))
mental_status = st.radio("Estado Mental", ("Orientado/capaz quanto a sua capacidade/limitação", "Superestina capacidade/Esquece limitações"))

morse_total_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)

st.subheader("Escala EVARUCI")
consciousness = st.slider("Consciência (1-4)", 1, 4, 1)
hemodynamics = st.slider("Hemodinâmica (1-4)", 1, 4, 1)
respiratory = st.slider("Respiratório (1-4)", 1, 4, 1)
mobility_evaruci = st.slider("Mobilidade (1-4)", 1, 4, 1)
skin_condition = st.slider("Estado da Pele (1-4)", 1, 4, 1)
other_factors = st.slider("Outros Fatores (1-4)", 1, 4, 1)
length_of_stay = st.slider("Semanas de Internação na UTI (0-4)", 0, 4, 0)

evaruci_total_score = evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility_evaruci, skin_condition, other_factors, length_of_stay)

if st.button("Calcular Pontuação"):
    st.success(f"Pontuação total da Escala de Morse: {morse_total_score}")
    st.success(f"Pontuação total da Escala EVARUCI: {evaruci_total_score}")
    morse_risk = risk_category(morse_total_score)
    evaruci_risk = risk_category(evaruci_total_score)
    st.success(f"Tipo de Risco (Escala de Morse): {morse_risk}")
    st.success(f"Tipo de Risco (Escala EVARUCI): {evaruci_risk}")
