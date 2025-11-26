import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

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
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 18px;
    margin-bottom: 8px;
}

/* Horizontal radio buttons */
div[role='radiogroup'] {
    display: flex !important;
    gap: 20px !important;
    margin-bottom: 0px !important;
}

/* LABEL ROW — NOW CLOSER TO BUTTONS */
.label-row {
    display: flex;
    justify-content: space-between;
    width: 260px;
    font-size: 0.8rem;
    margin-top: -12px; /* <-- moved closer */
}

.label-left {
    color: white;
}

.label-middle {
    color: white;
    text-align: center;
    width: 100%;
}

.label-right {
    color: white;
    text-align: right;
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
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO CENTERED
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
Denne test giver dig et indblik i, hvordan du bearbejder baade foelelsesmaessige 
og sansemaessige indtryk, og hvordan dit mentale tempo paavirker dine reaktioner.
Testen undersoeger, om dine reaktioner er mere intuitive og impulsstyrede 
eller mere langsomme, bearbejdende og eftertaenksomme.

Du besvarer 20 udsagn paa en skala fra 0 (aldrig) til 4 (altid).

Testen er ikke en diagnose, men et psykologisk vaerktoej til selvindsigt.
""")

# -------------------------------------------------------------
# QUESTIONS
# -------------------------------------------------------------
questions = [
    "Jeg bliver let overvaeldet af indtryk.",
    "Jeg opdager smaa detaljer, som andre ofte overser.",
    "Jeg bruger laengere tid paa at taenke ting igennem.",
    "Jeg foretraekker rolige omgivelser.",
    "Jeg reagerer staerkt paa uventede afbrydelser.",
    "Jeg bearbejder information dybt og grundigt.",
    "Jeg har brug for mere tid til at omstille mig.",
    "Jeg bliver hurtigt mentalt udmattet.",
    "Jeg er meget opmaerksom paa stemninger hos andre.",
    "Jeg foretraekker at goere en ting ad gangen.",
    "Jeg paavirkes lettere af stoej end de fleste.",
    "Jeg trives bedst med tydelige rammer og struktur.",
    "Jeg bruger lang tid paa at komme i gang med nye opgaver.",
    "Jeg har svaert ved at sortere irrelevante stimuli fra.",
    "Jeg bliver let paavirket af andres humoer.",
    "Jeg bruger lang tid paa at traeffe beslutninger.",
    "Jeg foretraekker dybe samtaler frem for smalltalk.",
    "Jeg kan have svaert ved at skifte fokus hurtigt.",
    "Jeg foeler mig ofte overstimuleret.",
    "Jeg bliver let distraheret, naar der sker meget omkring mig."
]

# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = 0

# -------------------------------------------------------------
# RENDER QUESTIONS WITH LABELS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        [0, 1, 2, 3, 4],
        key=f"q_{i}_{st.session_state.reset_trigger}",
        horizontal=True,
        label_visibility="collapsed"
    )

    st.session_state.answers[i] = choice

    st.markdown("""
    <div class="label-row">
        <div class="label-left">aldrig</div>
        <div class="label-middle">sjaeldnere</div>
        <div class="label-right">altid</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.session_state.reset_trigger += 1
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

PROFILE_TEXT = {
    "HSP": [
        "Du registrerer flere nuancer.",
        "Du bearbejder indtryk dybt.",
        "Du bliver let overstimuleret.",
        "Du har et fintfoelende nervesystem.",
        "Du er empatisk og opmaerksom.",
        "Du har brug for ro og pauser."
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo.",
        "Du bearbejder grundigt men langsomt.",
        "Du har brug for mere omstillingstid.",
        "Du trives med struktur.",
        "Du kan foele dig presset ved hurtige skift.",
        "Du har god udholdenhed i eget tempo."
    ],
    "Mellemprofil": [
        "Du har god balance mellem tempoer.",
        "Du haandterer stimuli fleksibelt.",
        "Du er hverken meget hurtig eller langsom.",
        "Du tilpasser dig let omgivelser.",
        "Du mister sjældent balancen.",
        "Du fungerer bredt i sociale situationer."
    ]
}

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

# -------------------------------------------------------------
# RESULT DISPLAY
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"Profil: {profile}")

st.write("### Karakteristika:")
for s in PROFILE_TEXT[profile]:
    st.write("- " + s)

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
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Karakteristika:", styles["Heading2"]))

    for s in PROFILE_TEXT[profile]:
        story.append(Paragraph("- " + s, styles["BodyText"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Dine svar:", styles["Heading2"]))

    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – Svar: {st.session_state.answers[i]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)