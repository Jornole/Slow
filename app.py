import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# --- GLOBAL CSS: Kun baggrund + knapper (INGEN ændringer til layout)
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}

/* Røde knapper – stabil metode */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    border: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO (den gamle, fungerende metode)
# Dette er præcis som du havde det før tingene gik galt:
st.image("logo.png", width=220)

# --- Title
st.markdown("<h1 style='text-align:center; font-weight:800;'>DIN PERSONLIGE PROFIL</h1>",
            unsafe_allow_html=True)

# --- Intro text
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
""", unsafe_allow_html=True)

# --- Questions
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

if "answers" not in st.session_state:
    st.session_state.answers = [0]*len(questions)

for i, q in enumerate(questions):
    st.subheader(f"{i+1}. {q}")
    st.session_state.answers[i] = st.radio(
        "",
        [0,1,2,3,4],
        horizontal=True,
        key=f"q{i}",
    )

# --- Reset
if st.button("Nulstil svar"):
    st.session_state.answers = [0]*len(questions)
    st.experimental_rerun()

# --- Scoring
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

# --- PDF
def generate_pdf(score, profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score}", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(score, profile),
    file_name="rapport.pdf",
    mime="application/pdf",
)