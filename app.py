# app.py v88
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

version = "v88"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(
    f"<div style='font-size:0.85rem; background-color:#144d27; padding:6px 10px;"
    f"border-radius:6px; margin-bottom:10px;'>Version {version} — {timestamp}</div>",
    unsafe_allow_html=True
)

# CSS -----------------------------------------------------
st.markdown("""
<style>
html, body, .stApp { background-color:#1A6333 !important; color:white !important; }

/* Rød knap til reset + pdf */
.stButton > button {
    background-color:#C62828 !important;
    color:white !important;
    border-radius:8px !important;
    padding:0.6rem 1.3rem !important;
    border:none !important;
}

/* Cirkel-knapper (vores svar-knapper) */
.answer-circle {
    width:32px;
    height:32px;
    border-radius:50%;
    border:2px solid white;
    display:block;
    margin:auto;
}

.answer-circle.selected {
    background-color:#ff4444;
    border-color:#ff4444;
}

.answer-label {
    font-size:0.95rem;
    text-align:center;
    margin-top:6px;
}

.question-block {
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)

# Header --------------------------------------------------
st.markdown(
    "<div style='text-align:center;'><img src='https://raw.githubusercontent.com/Jornole/Slow/main/logo.png' width='160'></div>",
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align:center; font-weight:800;'>DIN PERSONLIGE PROFIL</h1>", unsafe_allow_html=True)

st.write("""
Denne test giver dig et indblik i, hvordan du bearbejder indtryk og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er **ikke en diagnose**, men et psykologisk værktøj til selvindsigt.
""")


# Questions ----------------------------------------------
questions = [...]
labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

def set_answer(q, v):
    st.session_state.answers[q] = v


# Display questions ---------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-block'>", unsafe_allow_html=True)
    st.write(f"### {i+1}. {q}")

    if st.session_state.answers[i] is None:
        st.write("*Vælg et svar*")

    cols = st.columns(5)
    for v in range(5):
        selected = st.session_state.answers[i] == v
        with cols[v]:
            if st.button("", key=f"ans_{i}_{v}", on_click=set_answer, args=(i, v)):
                pass
            circle = "answer-circle selected" if selected else "answer-circle"
            st.markdown(f"<div class='{circle}'></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-label'>{labels[v]}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# Reset ---------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)


# Score + Profile -----------------------------------------
safe = [a if a is not None else 0 for a in st.session_state.answers]
score = sum(safe)

def interpret(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# PDF -----------------------------------------------------
def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score}/80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe[i]]}", styles["BodyText"]))
    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport", generate_pdf(score, profile),
                   file_name="rapport.pdf", mime="application/pdf")