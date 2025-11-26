import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
VERSION = "v10"

# -------------------------------------------------------------
# CSS – pixel-perfect knapper + labels
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Logo center */
.center-logo {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 5px;
}

/* Title */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* Question text */
.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* --- SCALE WRAPPER --- */
.scale-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-bottom: 30px;
}

/* Button row */
.button-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

/* Custom round button */
.button {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #ffffff;
    border: 3px solid #ffffff;
    cursor: pointer;
    transition: 0.2s;
}

.button:hover {
    transform: scale(1.15);
}

/* Selected button */
.selected {
    background-color: #C62828 !important;
    border-color: #C62828 !important;
}

/* Labels row */
.label-row {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
}

.label-row span {
    width: 32px;
    text-align: center;
    font-size: 0.9rem;
}

/* RESET button */
.stButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
    margin-top: 40px !important;
}

.stButton > button:hover {
    background-color: #B71C1C !important;
}

/* Version text bottom-left */
.version-box {
    position: fixed;
    bottom: 8px;
    left: 10px;
    font-size: 0.8rem;
    color: white;
    opacity: 0.6;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# VERSION BOX
# -------------------------------------------------------------
st.markdown(f"<div class='version-box'>Version {VERSION}</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div class="center-logo">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO TEXT
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
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
# STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# QUESTION RENDERING
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # HIDDEN RADIO FOR LOGIC
    selected = st.radio(
        f"hidden_{i}",
        [0, 1, 2, 3, 4],
        index=st.session_state.answers[i],
        label_visibility="collapsed"
    )

    st.session_state.answers[i] = selected

    # CUSTOM BUTTONS + LABELS
    st.markdown("<div class='scale-container'>", unsafe_allow_html=True)

    # BUTTON ROW
    st.markdown("<div class='button-row'>", unsafe_allow_html=True)

    # Render each custom button
    btn_html = ""
    for val in range(5):
        cls = "button selected" if selected == val else "button"
        btn_html += f"""
            <div class="{cls}" onclick="document.querySelector('input[name=hidden_{i}][value='{val}']").click();"></div>
        """
    st.markdown(btn_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # LABEL ROW
    label_html = "<div class='label-row'>"
    for lb in labels:
        label_html += f"<span>{lb}</span>"
    label_html += "</div>"

    st.markdown(label_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.experimental_rerun()

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

total = sum(st.session_state.answers)
profile = interpret_score(total)

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
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

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – Svar: {st.session_state.answers[i]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)