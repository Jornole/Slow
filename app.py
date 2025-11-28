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
    font-size: 2.1rem;
    font-weight: 800;
    text-align: left;
    margin-top: 6px;
    margin-bottom: 18px;
}

/* Question text */
.question-text {
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 8px;
}

/* Make the radio row use full width and spread items */
.stRadio > div [role="radiogroup"] {
    display: flex !important;
    justify-content: space-between !important;
    width: 100% !important;
    gap: 0.2rem;
}

/* Make each radio label take equal width and center text */
.stRadio label {
    flex: 1 1 0;
    text-align: center;
    font-size: 0.95rem;
    color: white !important;
}

/* Style radio circles (keeps native look but larger) */
.stRadio input[type="radio"] {
    transform: scale(1.05);
}

/* Red buttons (reset + download) */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.2rem !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}

/* Slight spacing under each question for clarity */
.question-block { margin-bottom: 20px; }
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
# SESSION STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = 0

# -------------------------------------------------------------
# RENDER QUESTIONS (native st.radio, horizontal)
# -------------------------------------------------------------
for i, q in enumerate(questions):
    # question text
    st.markdown(f"<div class='question-block'><div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # native radio with label options (these labels are clickable)
    choice_label = st.radio(
        label="",
        options=labels,
        index=st.session_state.answers[i] if st.session_state.answers[i] < len(labels) else 0,
        key=f"q_{i}_{st.session_state.reset_trigger}",
        horizontal=True,
        label_visibility="collapsed"
    )

    # convert selected label back to index for scoring/storage
    st.session_state.answers[i] = labels.index(choice_label)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Nulstil svar"):
        st.session_state.answers = [0] * len(questions)
        st.session_state.reset_trigger += 1
        st.experimental_rerun()

with col2:
    st.write("")  # placeholder so buttons align left

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
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika for din profil:")
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
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)

st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v42 (stable)</div>", unsafe_allow_html=True)