import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# CSS – simple, stabil styling
# -------------------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color:#1A6333 !important;
    color:white;
    font-family:Arial, sans-serif;
}
.choice-btn {
    width:100%;
    padding:10px 0;
    border-radius:6px;
    font-size:1rem;
    font-weight:600;
    border:none;
}
.selected {
    background-color:#C62828 !important;
    color:white !important;
}
.unselected {
    background-color:#0F4D27 !important;
    color:white !important;
}
.stButton > button {
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Logo
# -------------------------------------------------------------
st.image("https://raw.githubusercontent.com/Jornole/Slow/main/logo.png", width=140)

st.markdown("<h1 style='text-align:center;'>DIN PERSONLIGE PROFIL</h1>", unsafe_allow_html=True)

st.write("""
Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.
""")

# -------------------------------------------------------------
# Data
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

if "answers" not in st.session_state:
    st.session_state.answers = [0]*len(questions)

# -------------------------------------------------------------
# Render questions
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.write(f"### {i+1}. {q}")

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        selected = (st.session_state.answers[i] == idx)
        css = "selected" if selected else "unselected"

        with col:
            if st.button(labels[idx], key=f"{i}_{idx}"):
                st.session_state.answers[i] = idx

            st.markdown(
                f"<div class='choice-btn {css}'>{labels[idx]}</div>",
                unsafe_allow_html=True
            )

# -------------------------------------------------------------
# Reset
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0]*len(questions)
    st.rerun()

# -------------------------------------------------------------
# Score
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
# PDF
# -------------------------------------------------------------
def pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1,12))
    for i,q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))
    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport",
                   pdf(score, profile),
                   file_name="rapport.pdf",
                   mime="application/pdf")

st.markdown("<div style='font-size:0.8rem;'>Version v38</div>", unsafe_allow_html=True)