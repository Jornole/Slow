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
# GLOBAL CSS
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Centered logo */
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

/* Question text */
.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 8px;
}

/* Hide radio option text completely */
div[data-baseweb="radio"] label {
    color: transparent !important; /* hide text */
    width: 20% !important;
    display: flex !important;
    justify-content: center !important;
}

/* Keep radio buttons visible */
div[data-baseweb="radio"] input {
    transform: scale(1.2);
}

/* Labels row */
.scale-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 3px;
    margin-bottom: 22px;
}

.scale-row span {
    width: 20%;
    text-align: center;
    font-size: 0.9rem;
    color: white;
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
        label_visibility="collapsed"
    )
    st.session_state.answers[i] = choice

    # labels row
    st.markdown(
        f"""
        <div class="scale-row">
            <span>Aldrig</span>
            <span>Sjældent</span>
            <span>Nogle gange</span>
            <span>Ofte</span>
            <span>Altid</span>
        </div>
        """,
        unsafe_allow_html=True
    )


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
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"


profile = interpret_score(sum(st.session_state.answers))


PROFILE_TEXT = {
    "HSP": [
        "Du registrerer flere nuancer...",
        "Du bearbejder oplevelser dybt...",
        "Du reagerer stærkt på stimuli..."
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo...",
        "Du bearbejder indtryk grundigt, men langsomt...",
        "Du har brug for ekstra tid..."
    ],
    "Mellemprofil": [
        "Du veksler naturligt...",
        "Du håndterer stimuli uden overbelastning...",
        "Du tilpasser dig tempoer..."
    ]
}


# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
total = sum(st.session_state.answers)

st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")


# -------------------------------------------------------------
# PDF GENERATOR
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf


st.download_button(
    "Download PDF-rapport",
    generate_pdf(total, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)


# -------------------------------------------------------------
# VERSION NUMBER
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v43</div>", unsafe_allow_html=True)