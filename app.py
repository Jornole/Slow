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
# GLOBAL CSS (NO RADIO BUTTON STYLING!)
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Title */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Question text */
.question-text {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 24px;
    margin-bottom: 6px;
}

/* PERFECT 5-COLUMN LABEL ROW */
.label-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    text-align: center;
    margin-top: -6px;
    margin-bottom: 26px;
    font-size: 0.95rem;
    width: 100%;
}

/* Buttons */
.stButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover {
    background-color: #B71C1C !important;
}

.version-tag {
    position: fixed;
    bottom: 12px;
    left: 12px;
    font-size: 0.85rem;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.
""")

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
# STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)
if "reset" not in st.session_state:
    st.session_state.reset = 0

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
scale_labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        [0, 1, 2, 3, 4],
        key=f"q_{i}_{st.session_state.reset}",
        horizontal=True,
        label_visibility="collapsed"
    )

    st.session_state.answers[i] = choice

    # Label row
    st.markdown(
        "<div class='label-row'>" +
        "".join([f"<div>{label}</div>" for label in scale_labels]) +
        "</div>",
        unsafe_allow_html=True
    )

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.session_state.reset += 1
    st.rerun()

# -------------------------------------------------------------
# RESULT
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

total = sum(st.session_state.answers)
profile = interpret_score(total)

st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
for line in PROFILE_TEXT[profile]:
    st.write(f"- {line}")

# -------------------------------------------------------------
# PDF
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Rapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Karakteristika:", styles["Heading2"]))
    for line in PROFILE_TEXT[profile]:
        story.append(Paragraph(f"- {line}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – Svar: {st.session_state.answers[i]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)

# VERSION TAG
st.markdown("<div class='version-tag'>v14</div>", unsafe_allow_html=True)