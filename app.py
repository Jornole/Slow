import streamlit as st
from datetime import datetime

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

version = "v128"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown(
    f"""
    <div style="font-size:0.85rem; background-color:#144d27;
                padding:6px 10px; width:fit-content;
                border-radius:6px; margin-bottom:10px;">
        Version {version} — {timestamp}
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------
# GLOBAL CSS (samme som tidligere v107)
# ----------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}
.question-text {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 22px;
    margin-bottom: 6px;
}
.stButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.35rem 0.6rem !important;
    font-weight: 600 !important;
    border: none !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    height: 40px !important;
}
.stButton > button:hover {
    background-color: #B71C1C !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------
# QUESTIONS
# ----------------------------------------------
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
    "Jeg bliver let distraheret, når der sker meget omkring mig.",
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# ----------------------------------------------
# SESSION STATE
# ----------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# ----------------------------------------------
# RENDER QUESTIONS
# (nyt: smalle kolonner så knapper står SIDE OM SIDE)
# ----------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1])   # ← NØGLEN (smalle kolonner)

    for idx, col in enumerate(cols):
        with col:
            if st.button(labels[idx], key=f"btn_{i}_{idx}"):
                st.session_state.answers[i] = idx

# ----------------------------------------------
# RESULTAT
# ----------------------------------------------
safe = [a if a is not None else 0 for a in st.session_state.answers]
score = sum(safe)

def interpret(s):
    if s <= 26:
        return "Slow Processor"
    elif s <= 53:
        return "Mellemprofil"
    return "HSP"

profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")