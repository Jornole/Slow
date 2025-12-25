import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
version = "v79"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown(
    f"""
    <div style="font-size:0.85rem; background-color:#144d27;
                padding:6px 10px; width:fit-content;
                border-radius:6px; margin-bottom:10px;">
        Version {version} — {timestamp}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# CSS
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color:#1A6333 !important;
        color:white !important;
        font-family:Arial,sans-serif !important;
    }

    .main-title {
        font-size:2.3rem;
        font-weight:800;
        text-align:center;
        margin:20px 0 25px 0;
    }

    .question-text {
        font-size:1.1rem;
        font-weight:600;
        margin-top:20px;
        margin-bottom:8px;
    }

    /* ---------- SCALE BUTTONS ---------- */
    div[data-testid="column"] button {
        width:100%;
        padding:6px 0 !important;
        font-size:0.8rem !important;
        border-radius:6px !important;
        background-color:#2E7D32 !important;
        color:white !important;
        border:none !important;
    }

    div[data-testid="column"] button:hover {
        background-color:#388E3C !important;
    }

    .selected button {
        background-color:#C62828 !important;
        font-weight:700 !important;
    }

    .stButton > button {
        background-color:#C62828 !important;
        color:white !important;
        border-radius:8px !important;
        padding:0.6rem 1.2rem !important;
        font-weight:600 !important;
        border:none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# TITLE
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

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
    "Jeg bliver let distraheret, når der sker meget omkring mig.",
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# CALLBACK
# -------------------------------------------------------------
def set_answer(q_idx, value):
    st.session_state.answers[q_idx] = value

# -------------------------------------------------------------
# RENDER QUESTIONS (NO RELOAD)
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5)
    for v, col in enumerate(cols):
        with col:
            wrapper = "selected" if st.session_state.answers[i] == v else ""
            st.markdown(f"<div class='{wrapper}'>", unsafe_allow_html=True)
            st.button(
                labels[v],
                key=f"q{i}_{v}",
                on_click=set_answer,
                args=(i, v),
            )
            st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# SCORE
# -------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

safe_answers = [a if a is not None else 0 for a in st.session_state.answers]
total_score = sum(safe_answers)
profile = interpret_score(total_score)

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for i, q in enumerate(questions):
        story.append(
            Paragraph(f"{i+1}. {q} – {labels[safe_answers[i]]}", styles["BodyText"])
        )

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)