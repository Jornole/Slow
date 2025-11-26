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
st.markdown(
    """
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
    margin-bottom: 6px;
}

/* RADIO-GRUPPER: 5 knapper spredt ud, tekst under og klikbar */
div[role="radiogroup"] {
    display: flex !important;
    justify-content: space-between !important;
    width: 100% !important;
    margin-bottom: 0.4rem !important;
}

div[role="radiogroup"] > label {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0.15rem !important;
}

/* selve radio-cirklen lidt tættere på teksten */
div[role="radiogroup"] > label > div:first-child {
    margin-bottom: 0 !important;
}

/* Teksten under cirklen */
div[role="radiogroup"] > label > div:last-child {
    font-size: 0.85rem !important;
}

/* Røde knapper: reset + PDF */
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

/* Versionsnummer nederst til venstre */
.app-version {
    position: fixed;
    left: 10px;
    bottom: 8px;
    font-size: 0.75rem;
    opacity: 0.85;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO (CENTERED)
# -------------------------------------------------------------
st.markdown(
    """
<div class="center-logo">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# MAIN TITLE
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO TEXT
# -------------------------------------------------------------
st.markdown(
    """
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
""",
    unsafe_allow_html=True,
)

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

# Skala-tekster (vises under knapperne) – og bruges som radio-options
scale_labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    # gemmer score 0–4 for hvert spørgsmål
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(
        f"<div class='question-text'>{i+1}. {q}</div>",
        unsafe_allow_html=True,
    )

    # nuværende score (0–4) for dette spørgsmål
    current_score = st.session_state.answers[i]
    # den label der svarer til scoren
    current_label = scale_labels[current_score]

    # radio med labels – tekst er under cirklen (styret af CSS)
    choice_label = st.radio(
        label="",
        options=scale_labels,
        index=scale_labels.index(current_label),
        key=f"q_{i}",
        horizontal=True,
        label_visibility="collapsed",
    )

    # opdater score (0–4) ud fra valgt label
    st.session_state.answers[i] = scale_labels.index(choice_label)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.experimental_rerun()

# -------------------------------------------------------------
# INTERPRETATION
# -------------------------------------------------------------
def interpret_score(score: int) -> str:
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
        "Du har god udholdenhed, når du arbejder i dit eget tempo."
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
# PDF GENERATOR
# -------------------------------------------------------------
def generate_pdf(score: int, profile: str) -> BytesIO:
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
        story.append(
            Paragraph(
                f"{i+1}. {q} – Svar: {st.session_state.answers[i]}",
                styles["BodyText"],
            )
        )

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)

# -------------------------------------------------------------
# VERSION LABEL
# -------------------------------------------------------------
st.markdown('<div class="app-version">Version v18</div>', unsafe_allow_html=True)