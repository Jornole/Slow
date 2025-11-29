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

/* Score-knapper */
.scale-button {
    display: inline-block;
    padding: 8px 14px;
    margin: 0 6px;
    border-radius: 6px;
    background-color: rgba(255,255,255,0.10);
    color: white;
    cursor: pointer;
    font-size: 1.0rem;
    transition: 0.15s;
}
.scale-button:hover {
    background-color: rgba(255,255,255,0.20);
}
.scale-button.selected {
    background-color: #C62828 !important;
}

.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 10px;
}

/* Red standard buttons */
.stButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
    margin-top: 10px;
}
.stButton > button:hover {
    background-color: #B71C1C !important;
}
</style>
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
    st.session_state.answers = [None] * len(questions)


# -------------------------------------------------------------
# RENDER QUESTIONS WITH TEXT-BUTTONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5)
    for j, label in enumerate(labels):

        selected = (st.session_state.answers[i] == j)
        class_name = "scale-button selected" if selected else "scale-button"

        if cols[j].button(label, key=f"btn_{i}_{j}"):
            st.session_state.answers[i] = j
            st.rerun()

        cols[j].markdown(
            f"<div class='{class_name}'>{label}</div>",
            unsafe_allow_html=True
        )


# -------------------------------------------------------------
# RESET BUTTON (FEJLRETTET)
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)
    st.rerun()


# -------------------------------------------------------------
# CHECK COMPLETION
# -------------------------------------------------------------
if None in st.session_state.answers:
    st.header("Dit resultat")
    st.write("Besvar alle spørgsmål for at se dit resultat.")
    st.markdown("<div style='margin-top:40px; font-size:0.8rem;'>Version v63</div>", unsafe_allow_html=True)
    st.stop()


# -------------------------------------------------------------
# SCORE SYSTEM
# -------------------------------------------------------------
total_score = sum(st.session_state.answers)

def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    return "HSP"

profile = interpret_score(total_score)


# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

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
        "Du har god udholdenhed når du arbejder i dit eget tempo."
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

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")


# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v63</div>", unsafe_allow_html=True)