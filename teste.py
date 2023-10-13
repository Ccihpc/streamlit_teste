import streamlit as st

def morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status):
    score = 0
    if history_of_falls:
        score += 25
    if secondary_diagnosis:
        score += 15
    if ambulatory_aid:
        score += 20
    if IV_heparin:
        score += 20
    score += mobility
    score += mental_status
    return score

def risk_category(score):
    if score >= 45:
        return "Alto Risco"
    elif score >= 25:
        return "Moderado Risco"
    else:
        return "Baixo Risco"

st.title("Escala de Morse - Avaliação de Risco de Queda")

history_of_falls = st.checkbox("Histórico de Quedas (25 pontos)")
secondary_diagnosis = st.checkbox("Diagnóstico Secundário (15 pontos)")
ambulatory_aid = st.checkbox("Uso de Dispositivo de Auxílio à Deambulação (20 pontos)")
IV_heparin = st.checkbox("Presença de Soro Intravenoso (IV) ou Heparina (20 pontos)")
mobility = st.slider("Mobilidade (0-30 pontos)", min_value=0, max_value=30, step=1)
mental_status = st.slider("Estado Mental (0-15 pontos)", min_value=0, max_value=15, step=1)

if st.button("Calcular Pontuação"):
    total_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)
    risk = risk_category(total_score)
    st.success(f"Pontuação total da Escala de Morse: {total_score}")
    st.success(f"Tipo de Risco: {risk}")
