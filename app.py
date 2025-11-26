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
# CSS — v9 (PERFEKT ALIGNMENT)
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Version label */
.version-tag {
    position: fixed;
    bottom: 8px;
    left: 12px;
    opacity: 0.55;
    font-size: 0.75rem;
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
    margin-top: 22px;
    margin-bottom: 10px;
}

/* --- PERFECT 5-COLUMN GRID --- */
.scale-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    width: 100%;
    align-items: center;
    justify-items: center;
    margin-bottom: -4px;
}

.scale-grid label > div {
    transform: scale(1.25);
}

/* hide numbers inside radio items */
.scale-grid span {
    display: none !important;
}

/* Labels under */
.scale-labels {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    text-align: center;
    font-size: 0.85rem;
    margin-top: 4px;
    margin-bottom: 26px;
}

/* Buttons */
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
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:center; margin-top:20px; margin-bottom:5px;">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN TITLE
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

# -------------------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = 0

# -------------------------------------------------------------
# RENDER QUESTIONS — v9 GRID SYSTEM
# -------------------------------------------------------------
labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # RADIO in perfect grid
    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            if st.radio(
                "",
                [idx],
                key=f"q_{i}_{idx}_{st.session_state.reset_trigger}",
                label_visibility="collapsed"
            ) == idx:
                st.session_state.answers[i] = idx

    # LABELS under grid
    st.markdown(
        "<div class='scale-labels'>" +
        "".join([f"<div>{lab}</div>" for lab in labels]) +
        "</div>",
        unsafe_allow_html=True
    )

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
        "Du registrerer flere nuancer i både indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du reagerer stærkt på stimuli og kan blive overstimuleret.",
        "Du har en rig indre verden og et fintfølende nervesystem.",
        "Du er empatisk og opmærksom på andre.",
        "Du har brug for ro og pauser for at lade op."
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo og med forudsigelighed.",
        "Du bearbejder indtryk grundigt, men langsomt.",
        "Du har brug for ekstra tid til omstilling og beslutninger.",
        "Du trives med faste rammer og struktur.",
        "Du kan føle dig presset, når tingene går hurtigt.",
        "Du har god udholdenhed, når arbejder i dit eget tempo."
    ],
    "Mellemprofil": [
        "Du veksler naturligt mellem hurtig og langsom bearbejdning.",
        "Du håndterer de fleste stimuli uden at blive overvældet.",
        "Du har en god balance mellem intuition og eftertænksomhed.",
        "Du kan tilpasse dig forskellige miljøer og tempoer.",
        "Du bliver påvirket i perioder, men finder hurtigt balancen igen.",
        "Du fungerer bredt socialt og mentalt i mange typer situationer."
    ]
}

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

# -------------------------------------------------------------
# RESULT BLOCK
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

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

    story.append(Paragraph("Karakteristika for din profil:", styles["Heading2"]))
    for s in PROFILE_TEXT[profile]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
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

# VERSION TAG
st.markdown("<div class='version-tag'>v9</div>", unsafe_allow_html=True)