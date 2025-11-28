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
# GLOBAL CSS (stabil version)
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Center logo */
.center-logo {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 5px;
}

/* Main title */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* Question */
.question-text {
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 4px; /* tæt på skalaen */
}

/* === RADIOLAYOUT FIX – VIRKER I ALLE BROWSERE === */

/* Fjern skjult Streamlit margin over radio-gruppen */
div[data-baseweb="radio"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Selve radio-gruppen – 5 knapper på linje */
div[data-baseweb="radiogroup"] {
    display: flex !important;
    justify-content: space-between !important;
    width: 100% !important;
    margin-top: -4px !important; /* træk op mod spørgsmålet */
}

/* Tekst og cirkel i hver option */
div[data-baseweb="radio"] > label {
    flex: 1 1 0;
    text-align: center !important;
    margin: 0 !important;
    padding: 0 !important;
    color: white !important;
    font-size: 0.95rem !important;
}

/* Radio cirklerne */
div[data-baseweb="radio"] input[type="radio"] {
    transform: scale(1.15); /* lidt større */
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    border: none !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div class="center-logo">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE + INTRO
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

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
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset" not in st.session_state:
    st.session_state.reset = 0

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        options=list(range(5)),
        key=f"q{i}_{st.session_state.reset}",
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda x: labels[x]
    )

    st.session_state.answers[i] = choice

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.reset += 1
    st.session_state.answers = [0] * len(questions)
    st.rerun()

# -------------------------------------------------------------
# INTERPRETATION
# -------------------------------------------------------------
def interpret(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

profile = interpret(sum(st.session_state.answers))

summary_text = {
    "HSP": [
        "Du registrerer flere nuancer i både indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du reagerer stærkt på stimuli og kan blive overstimuleret."
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo og med forudsigelighed.",
        "Du bearbejder indtryk grundigt, men langsomt.",
        "Du har brug for ekstra tid til omstilling og beslutninger."
    ],
    "Mellemprofil": [
        "Du balancerer naturligt mellem hurtig og langsom bearbejdning.",
        "Du håndterer de fleste stimuli uden at blive overvældet.",
        "Du tilpasser dig godt i forskellige situationer."
    ]
}

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
total = sum(st.session_state.answers)
st.subheader(f"Score: {total} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika:")
for line in summary_text[profile]:
    st.write(f"- {line}")

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
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}",
                               styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport",
                   make_pdf(total, profile),
                   file_name="rapport.pdf",
                   mime="application/pdf")

# -------------------------------------------------------------
# VERSION NUMBER
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v42</div>", unsafe_allow_html=True)