# app.py - v90
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

version = "v90"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(
    f"""<div style="font-size:0.85rem; background-color:#144d27; padding:6px 10px;
                width:fit-content; border-radius:6px; margin-bottom:10px;">
        Version {version} — {timestamp}
    </div>""",
    unsafe_allow_html=True,
)

# CSS: styling for Streamlit buttons to look like v78 pills.
st.markdown(
    """
    <style>
    html, body, .stApp { background-color: #1A6333 !important; color: white !important;
        font-family: Arial, sans-serif !important; }

    .main-title { font-size:2.3rem; font-weight:800; text-align:center;
        margin-top:10px; margin-bottom:25px; }

    .question-text { font-size:1.15rem; font-weight:600; margin-top:22px; margin-bottom:6px; }

    /* Make Streamlit buttons look like red pills */
    .stButton > button {
        background-color: #C62828 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.2rem !important;
        font-weight: 600 !important;
        font-size:1rem !important;
        width: 100%;
        text-align: left;
    }
    .stButton > button:focus { outline: 3px solid rgba(255,255,255,0.08) !important; }

    /* Selected appearance: white background with red text & border.
       We'll emulate selected by rendering a markdown block with this class
       immediately after a click (see code below). */
    .selected-pill {
        background-color: white;
        color: #C62828;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        font-weight: 700;
        font-size:1rem;
        width: 100%;
        display: inline-block;
        box-sizing: border-box;
        border: 4px solid rgba(255,255,255,0.06);
    }

    /* small label above pill (like v78 small label) */
    .small-label { color: #ffffff; margin-bottom:6px; }

    @media (min-width:900px) {
        /* on wide screens, make the options horizontal: */
        .h-row { display:flex; gap:12px; }
        .h-col { flex:1; min-width:120px; }
    }
    @media (max-width:899px) {
        .h-row { display:block; }
        .h-col { width:100%; margin-bottom:10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown(
    """
    Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige
    og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

    Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

    Testen er <u><b>ikke en diagnose</b></u>, men et psykologisk værktøj til selvindsigt.
    """,
    unsafe_allow_html=True,
)

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

# session state
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# render questions: for each question we show 5 horizontally (on wide) or vertically (on mobile)
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # small label with current selection (keeps v78 feel)
    current = st.session_state.answers[i]
    if current is not None:
        st.markdown(f"<div class='small-label'>{labels[current]}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='small-label'>Vælg et svar</div>", unsafe_allow_html=True)

    # responsive container: on wide screens show as a row; on mobile stack
    st.markdown("<div class='h-row'>", unsafe_allow_html=True)
    for idx, lab in enumerate(labels):
        # Each option in its own column-like container
        key = f"q_{i}_{idx}"
        if st.button(lab, key=key):
            st.session_state.answers[i] = idx
    st.markdown("</div>", unsafe_allow_html=True)

# Reset
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

# scoring (None => 0)
safe_answers = [a if a is not None else 0 for a in st.session_state.answers]
total_score = sum(safe_answers)
def interpret_score(s):
    if s <= 26: return "Slow Processor"
    if s <= 53: return "Mellemprofil"
    return "HSP"
profile = interpret_score(total_score)

PROFILE_TEXT = {
    "HSP": ["Du registrerer flere nuancer...", "..."],
    "Slow Processor": ["Du arbejder bedst i roligt tempo...", "..."],
    "Mellemprofil": ["Du veksler naturligt...", "..."],
}

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1,12))
    for i,q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe_answers[i]]}", styles["BodyText"]))
    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport", generate_pdf(total_score, profile),
                   file_name="HSP_SlowProcessor_Rapport.pdf", mime="application/pdf")