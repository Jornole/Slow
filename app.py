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
# GLOBAL CSS  (v48 + labels rykket op)
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Title */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* Questions */
.question-text {
    font-size: 1.20rem;
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 8px;
}

/* Hide radio numbers */
.stRadio > div > label > div:first-child {
    display: none !important;
}

/* Keep radio buttons exactly as in v48 */
.stRadio > div {
    display: flex !important;
    justify-content: space-between !important;
    margin-top: 0px !important;
}

/* LABELS — THIS is the ONLY change (raised a bit) */
.scale-row {
    display: flex;
    justify-content: space-between;
    margin-top: -10px;   /* <- ONLY CHANGE */
    margin-bottom: 25px;
    width: 100%;
}

.scale-row span {
    flex: 1;
    text-align: center;
    font-size: 0.88rem;
}

/* Red buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:center; margin-top:20px; margin-bottom:5px;">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE + INTRO
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u><b>ikke en diagnose</b></u>, men et psykologisk værktøj til selvindsigt.
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

# -------------------------------------------------------------
# STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = 0

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        options=list(range(5)),
        key=f"q_{i}_{st.session_state.reset_trigger}",
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda x: ""
    )

    st.session_state.answers[i] = choice

    st.markdown("""
        <div class="scale-row">
            <span>Aldrig</span>
            <span>Sjældent</span>
            <span>Nogle gange</span>
            <span>Ofte</span>
            <span>Altid</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.session_state.reset_trigger += 1
    st.rerun()

# -------------------------------------------------------------
# SCORING
# -------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v53</div>", unsafe_allow_html=True)