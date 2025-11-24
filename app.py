import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}
.question-text {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

svg_logo = """
<div style='text-align:center; margin-bottom:25px;'>
<svg width="260" height="260" viewBox="0 0 200 200">
<ellipse cx="100" cy="100" rx="85" ry="70" fill="#136B3F" stroke="#3ECF8E" stroke-width="6" />
<path d="M40 80 Q60 60 80 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
<path d="M120 80 Q140 60 160 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
<path d="M40 120 Q60 140 80 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
<path d="M120 120 Q140 140 160 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
<text x="100" y="75" font-size="20" fill="white" text-anchor="middle" font-weight="700">HSP / Slow</text>
<text x="100" y="100" font-size="16" fill="white" text-anchor="middle">Processor Test</text>
<text x="65" y="145" font-size="34" fill="white" text-anchor="middle">&#128007;</text>
<text x="135" y="145" font-size="34" fill="white" text-anchor="middle">&#128012;</text>
</svg>
</div>
"""

st.markdown(svg_logo, unsafe_allow_html=True)

st.title("HSP / Slow Processor Test")

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både
følelsesmæssige og sansemæssige indtryk, og hvordan dit mentale tempo
påvirker dine reaktioner i hverdagen.

Testen er <u>ikke en diagnose</u>, men et psykologisk værktøj til selvindsigt.
""", unsafe_allow_html=True)

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
    st.session_state.answers = [0] * 20

def reset_answers():
    st.session_state.answers = [0] * 20
    for i in range(20):
        st.session_state[f"q_{i}"] = 0

answers = []
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.session_state.answers[i] = val
    answers.append(val)

st.button("Nulstil svar", on_click=reset_answers)

def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    if score <= 53:
        return "Mellemprofil"
    return "HSP"

total = sum(st.session_state.answers)
profile = interpret_score(total)

st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
st.subheader(f"Profil: {profile}")