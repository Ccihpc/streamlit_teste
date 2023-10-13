import streamlit as st

def morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status):
    score = 0
    if history_of_falls:
        score += 25
    if secondary_diagnosis:
        score += 15
    if ambulatory_aid == "Muletas/Bengala/Andador":
        score += 15
    if ambulatory_aid == "Acamado/Auxiliado por Profissional de Saude":
        score += 0
    if IV_heparin:
        score += 20
    if mobility == "Fraca":
        score += 10
    if mobility == "Comprometida/Cambaleante":
        score += 20
    if mental_status == "Superestima capacidade/Esquece limitações":
        score += 15
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
ambulatory_aid = st.radio("Auxílio na Deambulação", 
                          ("Nenhum/Sem deambulação, Acamado, Cadeira de Rodas", 
                           "Fraca", 
                           "Comprometida/Cambaleante", 
                           "Acamado/Auxiliado por Profissional de Saude", 
                           "Muletas/Bengala/Andador"))
IV_heparin = st.checkbox("Presença de Soro Intravenoso (IV) ou Heparina (20 pontos)")
mental_status = st.radio("Estado Mental", 
                         ("Orientado/capaz quanto a sua capacidade/limitação", 
                          "Superestima capacidade/Esquece limitações"))

if st.button("Calcular Pontuação"):
    total_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)
    risk = risk_category(total_score)
    st.success(f"Pontuação total da Escala de Morse: {total_score}")
    st.success(f"Tipo de Risco: {risk}")
