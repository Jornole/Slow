import streamlit as st
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}
h1, h2, h3, p, label {
    color: white !important;
}
.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 12px;
}
.stSlider > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div::before {
    height: 14px !important;
}
.stSlider > div > div > div > div > div {
    width: 20px !important;
    height: 20px !important;
}
div.stButton > button, div.stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #B71C1C !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# BASE64 LOGO (indsat som inline image)
# -------------------------------------------------------------------
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAAEGpGNhQlgAAQakanV...
...HER KOMMER HELE BASE64 STRENGEN (jeg sender den i næste besked)
"""

st.markdown(
    f"""
    <img src="data:image/png;base64,{logo_base64}" 
         style="width:100%; height:auto; margin-bottom:20px;" />
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------------
# INTROTEKST
# -------------------------------------------------------------------
st.title("HSP / Slow Processor Test")

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige og sansemæssige indtryk, 
og hvordan dit mentale tempo påvirker dine reaktioner i hverdagen.  
Den undersøger også, om dine reaktioner typisk er mere intuitiv, impulsstyret 
eller mere eftertænksomt bearbejdende.

Spørgsmålene handler om:
- din modtagelighed over for stimuli  
- dit refleksionsniveau og din intuitive respons  
- dit naturlige tempo – fra impulsstyret til langsomt og dybdegående  
- og den måde du organiserer og sorterer indtryk på  

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

Når du er færdig, får du:
- Din **samlede score**  
- En **profil**: HSP, Slow Processor eller en mellemprofil  
- En kort psykologisk beskrivelse af dine **styrker og udfordringer**  
- Mulighed for at hente en **PDF-rapport** med alle dine svar  

Testen er <u>**ikke en diagnose**</u> – men et psykologisk værktøj til selvindsigt, 
der kan hjælpe dig med bedre at forstå dine naturlige reaktions-, bearbejdnings- 
og beslutningsmønstre.
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SPØRGSMÅL
# -------------------------------------------------------------------
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

if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

def reset_answers():
    st.session_state.answers = [0] * len(questions)
    for i in range(len(questions)):
        st.session_state[f"q_{i}"] = 0

answers = []
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.session_state.answers[i] = val
    answers.append(val)

st.button("Nulstil svar", on_click=reset_answers)

# -------------------------------------------------------------------
# PROFIL LOGIK
# -------------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

STATEMENTS = {
    "HSP": [
        "Du registrerer subtile detaljer og stemninger.",
        "Du bearbejder indtryk dybt og reflekteret.",
        "Du har stærke empatiske antenner.",
        "Du kan let blive overstimuleret.",
        "Du har brug for mere ro end andre.",
        "Du bruger meget mental energi på sociale indtryk."
    ],
    "Slow Processor": [
        "Du trives bedst med ro og fast struktur.",
        "Du arbejder omhyggeligt og grundigt.",
        "Du har god udholdenhed i stabile miljøer.",
        "Hurtigt tempo kan være pressende.",
        "Du har brug for tid til at omstille dig.",
        "Du bliver let mentalt udtrættet af mange indtryk."
    ],
    "Mellemprofil": [
        "Du har en god balance mellem tempo og følsomhed.",
        "Du kan både arbejde hurtigt og langsomt.",
        "Du håndterer stimuli moderat godt.",
        "Du bliver sjældent overvældet.",
        "Du er både empatisk og logisk.",
        "Du tilpasser dig let forskellige miljøer."
    ]
}

# -------------------------------------------------------------------
# RESULTAT
# -------------------------------------------------------------------
total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Samlet score: **{total_score} / 80**")
st.write(f"Profil: **{profile}**")

st.write("### Karakteristika for din profil:")
for s in STATEMENTS[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------------
# PDF RAPPORT
# -------------------------------------------------------------------
def generate_pdf(score, profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Resultatrapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph