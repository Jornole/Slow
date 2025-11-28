import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# CSS
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Question header */
.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Red buttons row */
.answer-row {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    width: 100%;
}

.answer-btn {
    background: #C62828;
    padding: 10px 0;
    flex: 1;
    text-align: center;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    border: 2px solid transparent;
}

.answer-btn:hover {
    background: #B71C1C;
}

.answer-selected {
    border: 2px solid white !important;
}

/* Text labels */
.label-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 4px;
    margin-bottom: 20px;
}

.label-row span {
    flex: 1;
    text-align: center;
    font-size: 0.85rem;
}

.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin-top:20px; margin-bottom:5px;'>
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO
# -------------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>DIN PERSONLIGE PROFIL</h1>", unsafe_allow_html=True)

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u><b>ikke en diagnose</b></u>.
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# QUESTIONS
# -------------------------------------------------------------
questions = [
    "Jeg bliver let overvældet af indtryk.",
    "Jeg opdager små detaljer, som andre ofte overser.",
    "Jeg bruger længere tid på at tænke ting igennem.",
    "Jeg foretrækker rolige omgivelser.",
    "Jeg reagerer stærkt på uventede afbrydelser.",
    "Jeg bearbejder information dybt og grundigt.",
    "Jeg har brug for mere tid til at omstille mig.",
    "Jeg bliver hurtigt mentalt udmattet.",
    "Jeg er meget opmærksom på stemninger hos andre.",
    "Jeg foretrækker at gøre én ting ad gangen.",
    "Jeg påvirkes lettere af støj end de fleste.",
    "Jeg trives bedst med tydelige rammer og struktur.",
    "Jeg bruger lang tid på at komme i gang med nye opgaver.",
    "Jeg har svært ved at sortere irrelevante stimuli fra.",
    "Jeg bliver let påvirket af andres humør.",
    "Jeg bruger lang tid på at træffe beslutninger.",
    "Jeg foretrækker dybe samtaler frem for smalltalk.",
    "Jeg kan have svært ved at skifte fokus hurtigt.",
    "Jeg føler mig ofte overstimuleret.",
    "Jeg bliver let distraheret, når der sker meget omkring mig."
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# INIT
if "answers" not in st.session_state:
    st.session_state.answers = [-1] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS (HTML ONLY – no Streamlit buttons)
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        selected = st.session_state.answers[i] == idx
        class_name = "answer-btn" + (" answer-selected" if selected else "")

        if col.markdown(
            f"<div class='{class_name}' onclick='document.location=\"/?set{i}={idx}\"'>{labels[idx]}</div>",
            unsafe_allow_html=True
        ):
            pass

    st.markdown(
        "<div class='label-row'>" +
        "".join([f"<span>{l}</span>" for l in labels]) +
        "</div>",
        unsafe_allow_html=True
    )

# URL TRICK TO CAPTURE CLICKS
params = st.query_params
for key, value in params.items():
    if key.startswith("set"):
        q_idx = int(key.replace("set", ""))
        st.session_state.answers[q_idx] = int(value)
        st.query_params.clear()
        st.rerun()

# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [-1] * len(questions)
    st.rerun()

# -------------------------------------------------------------
# SCORE + PDF (same as before)
# -------------------------------------------------------------
def interpret(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

score = sum(a if a >= 0 else 0 for a in st.session_state.answers)
profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version V45</div>", unsafe_allow_html=True)