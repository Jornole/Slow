import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# CSS
st.markdown("""
<style>
body, html, .stApp {
    background-color:#1A6333 !important;
    color:white !important;
    font-family:Arial, sans-serif;
}

/* Skala-knapper (kun tekst) */
.scale-row {
    display:flex;
    justify-content:space-between;
    margin-top: -5px;
    margin-bottom: 20px;
}

.scale-item {
    cursor:pointer;
    font-size:1.05rem;
    padding:4px 10px;
    color:white;
}

.scale-item.selected {
    color:#FF5252;
    font-weight:700;
}

/* Røde knapper */
.stButton > button, .stDownloadButton > button {
    background:#C62828 !important;
    color:white !important;
    border:none !important;
    border-radius:8px !important;
    padding:0.7rem 1.2rem !important;
    font-weight:600 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin:12px;'>
<img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO
# -------------------------------------------------------------
st.title("DIN PERSONLIGE PROFIL")

st.write("""
Denne test giver dig et indblik i, hvordan du bearbejder følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er **ikke en diagnose**, men et værktøj til selvindsigt.
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

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.write(f"### {i+1}. {q}")

    st.markdown("<div class='scale-row'>", unsafe_allow_html=True)

    for idx, lbl in enumerate(labels):
        selected = "selected" if st.session_state.answers[i] == idx else ""
        if st.button(lbl, key=f"btn_{i}_{idx}"):
            st.session_state.answers[i] = idx
            st.rerun()

        st.markdown(
            f"<div class='scale-item {selected}'>{lbl}</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.rerun()

# -------------------------------------------------------------
# SCORE + PROFILE
# -------------------------------------------------------------
score = sum(st.session_state.answers)

def interpret(s):
    if s <= 26: return "Slow Processor"
    if s <= 53: return "Mellemprofil"
    return "HSP"

profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF GENERATOR
# -------------------------------------------------------------
def make_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for i, q in enumerate(questions):
        ans = labels[st.session_state.answers[i]]
        story.append(Paragraph(f"{i+1}. {q} – {ans}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    data=make_pdf(score, profile),
    file_name="rapport.pdf",
    mime="application/pdf"
)

# Version
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v31</div>", unsafe_allow_html=True)