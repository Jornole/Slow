import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# CSS
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color:#1A6333 !important;
    color:white !important;
    font-family:Arial, sans-serif;
}

/* Question text */
.question-title {
    font-size:1.2rem;
    font-weight:600;
    margin-bottom:6px;
}

/* Radio layout: 5 circles on a row */
.radio-row > div {
    display:flex;
    justify-content:space-between;
}

/* Hide Streamlit’s default label */
.stRadio > label { display:none; }

/* Red buttons */
.stButton > button, .stDownloadButton > button {
    background:#C62828 !important;
    color:white !important;
    border:none;
    border-radius:8px;
    padding:0.7rem 1.3rem;
    font-weight:600;
}

/* Force radio text to stay white */
.stRadio div label {
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin-top:15px;'>
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="150">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE + INTRO
# -------------------------------------------------------------
st.markdown("""
# DIN PERSONLIGE PROFIL

Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.
""")

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

scale = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-title'>{i+1}. {q}</div>", unsafe_allow_html=True)

    choice = st.radio(
        label="",
        options=list(range(5)),
        format_func=lambda x: scale[x],
        horizontal=True,
        key=f"q_{i}"
    )

    st.session_state.answers[i] = choice
    st.write("")

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.rerun()

# -------------------------------------------------------------
# SCORE + PROFILE
# -------------------------------------------------------------
score = sum(st.session_state.answers)

def interpret(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF GENERATION
# -------------------------------------------------------------
def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} — {scale[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(),
    file_name="rapport.pdf",
    mime="application/pdf"
)

st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v29</div>", unsafe_allow_html=True)