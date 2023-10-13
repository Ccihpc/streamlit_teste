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

def evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility, other_factors, length_of_stay):
    score = consciousness + hemodynamics + respiratory + mobility + other_factors
    score += min(length_of_stay * 0.5, 2)  # Adiciona 0,5 ponto para cada semana de internação, até 2 pontos
    return score

def risk_category(score):
    if score >= 51:
        return "Risco muito elevado"
    elif score >= 41:
        return "Risco elevado"
    else:
        return "Risco médio"

st.title("Avaliação de Risco de Lesão por Pressão em Cuidados Intensivos")
st.subheader("Escala de Morse")
history_of_falls = st.radio("Histórico de Quedas", ("Não", "Sim"))
secondary_diagnosis = st.radio("Diagnóstico Secundário", ("Não", "Sim"))
ambulatory_aid = st.radio("Auxílio na Deambulação", ("Nenhum/Acamado/Auxiliado por Profissional de Saúde", "Muletas/Bengala/Andador", "Mobilidade/Parede"))
IV_heparin = st.radio("Presença de Soro Intravenoso (IV) ou Heparina", ("Não", "Sim"))
mobility = st.radio("Marcha", ("Normal/Sem deambulação, Acamado, Cadeira de Rodas", "Fraca", "Comprometida/Cambaleante"))
mental_status = st.radio("Estado Mental", ("Orientado/capaz quanto a sua capacidade/limitação", "Superestina capacidade/Esquece limitações"))

if st.button("Calcular Pontuação da Escala de Morse"):
    morse_total_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)
    morse_risk = risk_category(morse_total_score)
    st.success(f"Pontuação total da Escala de Morse: {morse_total_score} - Tipo de Risco: {morse_risk}")

st.subheader("Escala EVARUCI")
consciousness = st.checkbox("Consciência: Consciente (1 ponto)")
consciousness += st.checkbox("Consciência: Colaborativo (2 pontos)") * 2
consciousness += st.checkbox("Consciência: Reativo (3 pontos)") * 3
consciousness += st.checkbox("Consciência: Arreativo (4 pontos)") * 4

hemodynamics = st.checkbox("Hemodinâmica: Sem suporte (1 ponto)")
hemodynamics += st.checkbox("Hemodinâmica: Com expansão (2 pontos)") * 2
hemodynamics += st.checkbox("Hemodinâmica: Com dopamina ou dobutamina (3 pontos)") * 3
hemodynamics += st.checkbox("Hemodinâmica: Com adrenalina ou noradrenalina (4 pontos)") * 4

respiratory = st.checkbox("Respiratório: Com baixa necessidade de O2 (1 ponto)")
respiratory += st.checkbox("Respiratório: Com alta necessidade de O2 (2 pontos)") * 2
respiratory += st.checkbox("Respiratório: Com suporte respiratório (3 pontos)") * 3
respiratory += st.checkbox("Respiratório: Com ventilação mecânica invasiva (4 pontos)") * 4

mobility_evaruci = st.checkbox("Mobilidade: Independente (1 ponto)")
mobility_evaruci += st.checkbox("Mobilidade: Dependente mas se movimenta (2 pontos)") * 2
mobility_evaruci += st.checkbox("Mobilidade: Pouca mobilidade (3 pontos)") * 3
mobility_evaruci += st.checkbox("Mobilidade: Sem mobilidade (4 pontos)") * 4

other_factors = st.checkbox("Outros: Temperatura ≥38˚C (1 ponto)")
other_factors += st.checkbox("Outros: Saturação de O2 < 90% (1 ponto)")
other_factors += st.checkbox("Outros: PA sistólica < 100 mmHg (1 ponto)")
other_factors += st.checkbox("Outros: Estado da pele (1 ponto)")
other_factors += st.checkbox("Outros: Paciente em prona (1 ponto)")

length_of_stay = st.slider("Semanas de Internação na UTI (0-4)", 0, 4, 0)

if st.button("Calcular Pontuação da Escala EVARUCI"):
    evaruci_total_score = evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility_evaruci, other_factors, length_of_stay)
    evaruci_risk = risk_category(evaruci_total_score)
    st.success(f"Pontuação total da Escala EVARUCI: {evaruci_total_score} - Tipo de Risco: {evaruci_risk}")
