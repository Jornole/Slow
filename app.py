import streamlit as st
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# APP OPSÆTNING
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

/* Slider – medium størrelse */
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

/* Røde knapper */
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

# -------------------------------------------------------------
# LOGO – ROBUST INDLAESNING
# -------------------------------------------------------------
logo_path = os.path.join(os.getcwd(), "logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, use_column_width=True)
else:
    st.warning("Logo (logo.png) blev ikke fundet i mappen. Sørg for at logo.png ligger i samme mappe som app.py.")

# -------------------------------------------------------------
# INTROTEKST
# -------------------------------------------------------------
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
# SLIDERS (BESVARELSER)
# -------------------------------------------------------------
answers = []
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.session_state.answers[i] = val
    answers.append(val)

# Reset-knap
st.button("Nulstil svar", on_click=reset_answers)

# -------------------------------------------------------------
# FORTOLKNING
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
        "Du registrerer subtile detaljer og stemninger med stor præcision.",
        "Du bearbejder information dybt og reflekteret.",
        "Du har