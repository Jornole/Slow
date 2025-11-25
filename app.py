import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# PAGE SETTINGS
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

div.stButton > button, div.stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}

.question-text {
    font-size: 1.06rem;
    font-weight: 600;
    margin-bottom: 8px;
    margin-top: 14px;
}

/* SLIDER = 2/3 bredde og venstrejusteret */
.short-slider .stSlider {
    width: 55% !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
}

/* Slider højde + knob */
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
# LOGO + TITLE SIDE BY SIDE
# -------------------------------------------------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("logo.png", width=160)   # <-- doubleret størrelse

with col_title:
    st.markdown("<h1 style='margin-top: 10px;'>HSP / Slow Processor Test</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTROTEXT
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner 
i hverdagen. Den undersøger også, om dine reaktioner i højere grad er mere 
intuitive og impulsstyrede eller mere eftertænksomme og bearbejdende.

Spørgsmålene handler om:
- din modtagelighed over for stimuli  
- dit refleksionsniveau og intuitive respons  
- dit naturlige tempo – fra impulsstyret til langsomt og dybdegående  
- og den måde du organiserer og sorterer indtryk på  

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

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
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

def reset_answers():
    st.session_state.answers = [0] * len(questions)
    for i in range(len(questions)):
        st.session_state[f"q_{i}"] = 0

# -------------------------------------------------------------
# SLIDER SECTION
# -------------------------------------------------------------
answers = []
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)
    st.markdown("<div class='short-slider'>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.answers[i] = val
    answers.append(val)

st.button("Nulstil svar", on_click=reset_answers)

# -------------------------------------------------------------
# SCORE + PROFILE
# -------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

STATEMENTS = {
    "HSP": [
        "Du registrerer mange nuancer i stemninger og detaljer omkring dig.",
        "Du bearbejder indtryk dybt og reflekteret – ofte længe efter en oplevelse.",
        "Du har stærke empatiske antenner og opfanger andres signaler hurtigt.",
        "Du kan let blive overstimuleret, når der sker meget på én gang.",
        "Du har ofte brug for mere ro og restitution end andre.",
        "Dine intuitive og følelsesmæssige reaktioner kan være intense."
    ],
    "Slow Processor": [
        "Du trives bedst med ro, forudsigelighed og tydelige rammer.",
        "Du arbejder omhyggeligt og grundigt, når du får tid og plads.",
        "Du har god udholdenhed i stabile miljøer uden for mange skift.",
        "Hurtigt tempo og spontane ændringer kan opleves som pressende.",
        "Du har brug for ekstra tid til at tænke, beslutte og omstille dig.",
        "Du foretrækker at gøre ting i dit eget tempo."
    ],
    "Mellemprofil": [
        "Du har en relativt god balance mellem tempo og følsomhed.",
        "Du kan både arbejde hurtigt og langsomt alt efter opgaven.",
        "Du håndterer stimuli moderat godt, uden at blive overvældet.",
        "Du kan føle dig presset i perioder, men finder balancen igen.",
        "Du kan både være empatisk og analytisk i dine reaktioner.",
        "Du tilpasser dig generelt forskellige miljøer uden problemer."
    ]
}

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"Profil: **{profile}**")

st.write("### Karakteristika for din profil:")
for s in STATEMENTS[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------
# PDF DOWNLOAD
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test — Resultatrapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Karakteristika:", styles["Heading2"]))
    for s in STATEMENTS[profile]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} — Svar: {st.session_state.answers[i]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)