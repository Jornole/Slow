import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

VERSION = "v4"

# -------------------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* --- GRID TIL KNAPPER + LABELS --- */
.scale-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    column-gap: 0px;
    width: 100%;
    margin-top: 6px;
    margin-bottom: 30px;
    justify-items: center;
}

/* Selve radio-knapperne */
.scale-grid .radio-cell {
    display: flex;
    justify-content: center;
}

/* Teksterne under */
.scale-grid .label-cell {
    text-align: center;
    font-size: 0.83rem;
    margin-top: -4px;
}

/* Skjul radio-tekst (tallene) */
.scale-grid .radio-cell span {
    display: none !important;
}

/* Question text */
.question-text {
    font-size: 1.06rem;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
}

/* Red buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}

/* Versionsnummer nederst venstre */
.version-tag {
    position: fixed;
    bottom: 6px;
    left: 10px;
    font-size: 0.75rem;
    opacity: 0.7;
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
# MAIN TITLE
# -------------------------------------------------------------
st.markdown('<div style="font-size:2.3rem; font-weight:800; text-align:center;">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO TEXT
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u>ikke en diagnose</u>, men et psykologisk værktøj til selvindsigt.
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

# INIT session
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = 0

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # GRID START
    st.markdown("<div class='scale-grid'>", unsafe_allow_html=True)

    # RADIO ROW
    for val in range(5):
        st.markdown("<div class='radio-cell'>", unsafe_allow_html=True)
        choice = st.radio(
            "",
            [val],
            key=f"q_{i}_{val}_{st.session_state.reset_trigger}",
            label_visibility="collapsed",
            format_func=lambda x: ""
        )
        if choice == val:
            st.session_state.answers[i] = val
        st.markdown("</div>", unsafe_allow_html=True)

    # LABEL ROW
    for lab in labels:
        st.markdown(f"<div class='label-cell'>{lab}</div>", unsafe_allow_html=True)

    # GRID END
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.session_state.reset_trigger += 1
    st.rerun()

# -------------------------------------------------------------
# RESULT LOGIC
# -------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

score = sum(st.session_state.answers)
profile = interpret_score(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.write(f"**Profil: {profile}**")

# -------------------------------------------------------------
# PDF GENERATION
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Rapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Karakteristika for din profil:", styles["Heading2"]))

    story.append(Spacer(1, 12))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – Svar: {st.session_state.answers[i]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)

# -------------------------------------------------------------
# VERSION TAG
# -------------------------------------------------------------
st.markdown(f"<div class='version-tag'>Version {VERSION}</div>", unsafe_allow_html=True)