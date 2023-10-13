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

def evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility, other_factors, length_of_stay):
    score = 0
    if consciousness == "Colaborativo":
        score += 2
    elif consciousness == "Reativo":
        score += 3
    elif consciousness == "Arreativo":
        score += 4
    
    if hemodynamics == "Com expansão":
        score += 2
    elif hemodynamics == "Com dopamina ou dobutamina":
        score += 3
    elif hemodynamics == "Com adrenalina ou noradrenalina":
        score += 4
    
    if respiratory == "Com alta necessidade de O2":
        score += 2
    elif respiratory == "Com suporte respiratório":
        score += 3
    elif respiratory == "Com ventilação mecânica invasiva":
        score += 4
    
    if mobility == "Dependente mas se movimenta":
        score += 2
    elif mobility == "Pouca mobilidade":
        score += 3
    elif mobility == "Sem mobilidade":
        score += 4
    
    if any(other_factors.values()):
        score += sum(other_factors.values())
    
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

# Seção da Escala de Morse
st.subheader("Escala de Morse")
history_of_falls = st.checkbox("Histórico de Quedas (25 pontos)")
secondary_diagnosis = st.checkbox("Diagnóstico Secundário (15 pontos)")
ambulatory_aid = st.radio("Uso de Dispositivo de Auxílio à Deambulação", ["Nenhum/Acamado/Auxiliado por Profissional de Saúde", "Muletas/Bengala/Andador", "Mobilidade/Parede"])
IV_heparin = st.checkbox("Presença de Soro Intravenoso (IV) ou Heparina (20 pontos)")
mobility = st.radio("Marcha", ["Normal/Sem deambulação, Acamado, Cadeira de Rodas (0 pontos)", "Fraca (10 pontos)", "Comprometida/Cambaleante (20 pontos)"])
mental_status = st.checkbox("Estado Mental: Superestima capacidade/Esquece limitações (15 pontos)")

morse_calculated = False
if st.button("Calcular Pontuação da Escala de Morse"):
    morse_total_score = morse_scale_score(history_of_falls, secondary_diagnosis, ambulatory_aid, IV_heparin, mobility, mental_status)
    morse_risk = risk_category(morse_total_score)
    morse_calculated = True

# Seção da Escala EVARUCI
st.subheader("Escala EVARUCI")
consciousness = st.radio("Consciência", ["Consciente (1 ponto)", "Colaborativo (2 pontos)", "Reativo (3 pontos)", "Arreativo (4 pontos)"])
hemodynamics = st.radio("Hemodinâmica", ["Sem suporte (1 ponto)", "Com expansão (2 pontos)", "Com dopamina ou dobutamina (3 pontos)", "Com adrenalina ou noradrenalina (4 pontos)"])
respiratory = st.radio("Respiratório", ["Com baixa necessidade de O2 (1 ponto)", "Com alta necessidade de O2 (2 pontos)", "Com suporte respiratório (3 pontos)", "Com ventilação mecânica invasiva (4 pontos)"])
mobility = st.radio("Mobilidade", ["Independente (1 ponto)", "Dependente mas se movimenta (2 pontos)", "Pouca mobilidade (3 pontos)", "Sem mobilidade (4 pontos)"])

other_factors = {
    "Temperatura ≥38˚C (1 ponto)": st.checkbox("Temperatura ≥38˚C"),
    "Saturação de O2 < 90% (1 ponto)": st.checkbox("Saturação de O2 < 90%"),
    "PA sistólica < 100 mmHg (1 ponto)": st.checkbox("PA sistólica < 100 mmHg"),
    "Estado da pele (1 ponto)": st.checkbox("Estado da pele"),
    "Paciente em prona (1 ponto)": st.checkbox("Paciente em prona")
}
st.write("Acrescentar à pontuação total do item “outros” 0,5 ponto para cada semana de internação do paciente na Unidade de Cuidados Intensivos, até o máximo de 2 pontos.")
length_of_stay_evaruci = st.slider("Semanas de Internação na UTI (0-4)", 0, 4, 0)

evaruci_calculated = False
if st.button("Calcular Pontuação da Escala EVARUCI"):
    evaruci_total_score = evaruci_scale_score(consciousness, hemodynamics, respiratory, mobility, other_factors, length_of_stay_evaruci)
    evaruci_risk = risk_category(evaruci_total_score)
    evaruci_calculated = True

# Resultados
if morse_calculated:
    st.success(f"Pontuação total da Escala de Morse: {morse_total_score} - Tipo de Risco: {morse_risk}")

if evaruci_calculated:
    st.success(f"Pontuação total da Escala EVARUCI: {evaruci_total_score} - Tipo de Risco: {evaruci_risk}")
