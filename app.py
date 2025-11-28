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

.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 18px;
    margin-bottom: 6px;
}

/* Button-row layout */
.button-row {
    display: flex;
    justify-content: space-between;
    margin-top: 2px;
    margin-bottom: 12px;
}

/* Default button style */
.choice-btn {
    background-color: #ffffff22;
    color: white;
    padding: 6px 10px;
    border-radius: 6px;
    border: 1px solid #ffffff55;
    font-size: 0.95rem;
    flex: 1;
    text-align: center;
    margin: 0 4px;
    cursor: pointer;
}

/* Selected button */
.choice-btn.selected {
    background-color: #C62828 !important;
    border-color: #C62828 !important;
    font-weight: 600;
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
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [-1] * len(questions)
if "reset" not in st.session_state:
    st.session_state.reset = 0


# -------------------------------------------------------------
# RENDER QUESTIONS WITH CUSTOM BUTTONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    st.markdown("<div class='button-row'>", unsafe_allow_html=True)

    for idx, label in enumerate(labels):
        selected = st.session_state.answers[i] == idx

        button_html = f"""
        <div class="choice-btn {'selected' if selected else ''}" 
             onclick="fetch('/_set_answer?i={i}&v={idx}', {{method: 'POST'}}).then(() => window.location.reload())">
            {label}
        </div>
        """

        st.markdown(button_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# LOW-LEVEL ENDPOINT — updates state without visible widgets
# -------------------------------------------------------------
def update_answer():
    query = st.query_params
    if "_action" in query and query["_action"] == "set":
        i = int(query["i"])
        v = int(query["v"])
        st.session_state.answers[i] = v
        st.query_params.clear()

if "_action" in st.query_params:
    update_answer()


# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [-1] * len(questions)
    st.rerun()


# -------------------------------------------------------------
# SCORING
# -------------------------------------------------------------
def profile_of(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

if all(x >= 0 for x in st.session_state.answers):
    total = sum(st.session_state.answers)
    profile = profile_of(total)

    st.header("Dit resultat")
    st.subheader(f"Score: {total} / 80")
    st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v60</div>", unsafe_allow_html=True)