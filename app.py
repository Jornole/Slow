import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# GLOBAL STYLING
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Centralt placeret stor titel */
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 30px;
}

/* Spørgsmålstekst */
.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 14px;
    margin-bottom: 6px;
}

/* Røde knapper */
div.stButton > button, div.stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.3rem !important;
    font-weight: 600;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}

/* Slider style */
.stSlider > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div > div > div {
    width: 20px !important;
    height: 20px !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# HEADER — LOGO TIL VENSTRE, TEKST TIL HØJRE (FLEXBOX)
# -------------------------------------------------------------
st.markdown("""
<div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 10px;">
    <div>
        <img src="logo.png" width="100">
    </div>
    <div style="margin-left: 18px; line-height: 1.2;">
        <div style="font-size: 1.5rem; font-weight: 700;">
            HSP / SLOW
        </div>
        <div style="font-size: 1.3rem; font-weight: 600;">
            Processor Test
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# STOR OVERSKRIFT
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)


# -------------------------------------------------------------
# INTROTEKST
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig indblik i, hvordan du bearbejder følelsesmæssige og 
sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.  
Testen undersøger, om du reagerer mere intuitivt og impulsstyret – eller mere 
langsomt, bearbejdende og eftertænksomt.

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# SPØRGSMÅL
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
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

def reset_answers():
    st.session_state.answers = [0] * len(questions)
    for i in range(len(questions)):
        st.session_state[f"q_{i}"] = 0


# -------------------------------------------------------------
# SLIDERS — 66% BREDDE (GARANTERET)
# -------------------------------------------------------------
answers = []
for i, q in enumerate(questions):

    st.markdown(
        f"<div class='question-text'>{i+1}. {q}</div>",
        unsafe_allow_html=True,
    )

    # Slider container (66% max width)
    st.markdown("<div style='max-width: 66%; min-width: 100px;'>", unsafe_allow_html=True)

    val = st.slider(
        "",
        0,
        4,
        value=st.session_state.answers[i],
        key=f"q_{i}",
        label_visibility="hidden",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.answers[i] = val
    answers.append(val)


st.button("Nulstil svar", on_click=reset_answers)


# -------------------------------------------------------------
# PROFIL-FORTOLKNING
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
        "Du registrerer mange nuancer i indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du reagerer stærkt på stimuli og kan blive overstimuleret.",
        "Du har en rig indre verden og høj empati.",
        "Du bliver påvirket af miljøer og sociale vibes.",
        "Du har brug for ro og mentale pauser."
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt, stabilt tempo.",
        "Du bearbejder indtryk grundigt, men langsomt.",
        "Du har brug for ekstra tid til omstilling og beslutninger.",
        "Du trives med struktur og forudsigelighed.",
        "Du kan føle pres, når ting går hurtigt.",
        "Du har stærk udholdenhed, når tempoet passer dig."
    ],
    "Mellemprofil": [
        "Du kan både reagere hurtigt og langsomt.",
        "Du håndterer de fleste stimuli uden problemer.",
        "Du finder let balancen mellem intuition og eftertænksomhed.",
        "Du tilpasser dig nemt forskellige tempoer.",
        "Du påvirkes moderat, men genfinder hurtigt fokus.",
        "Du fungerer stærkt i mange typer miljøer."
    ]
}


# -------------------------------------------------------------
# RESULTAT
# -------------------------------------------------------------
total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")


# -------------------------------------------------------------
# PDF RAPPORT
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

    story.append(Paragraph("Karakteristika:", styles["Heading2"]))
    for s in PROFILE_TEXT[profile]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(
            Paragraph(f"{i+1}. {q} – Svar: {st.session_state.answers[i]}", styles["BodyText"])
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