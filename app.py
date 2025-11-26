import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# SETTINGS
# -------------------------------------------------------------
VERSION = "v17"
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# CSS
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

/* Perfect alignment wrapper */
.scale-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* The 5 buttons in one row */
.button-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    max-width: 380px;
    margin-top: 8px;
}

/* Each button wrapper */
.button-col {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Round buttons */
.button-col button {
    width: 38px !important;
    height: 38px !important;
    border-radius: 50% !important;
    border: none !important;
    cursor: pointer;
}

.button-off {
    background-color: white !important;
    color: #333 !important;
}

.button-on {
    background-color: #C62828 !important;
    color: white !important;
}

/* Label row under buttons */
.label-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    max-width: 380px;
    margin-top: 4px;
}

.label-row span {
    flex: 1;
    text-align: center;
    cursor: pointer;
    font-size: 0.85rem;
}

/* Reset button */
.stButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}

.stButton > button:hover {
    background-color: #B71C1C !important;
}

/* Version number */
.version-box {
    position: fixed;
    left: 12px;
    bottom: 8px;
    opacity: 0.55;
    font-size: 0.85rem;
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
# STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0]*20

# -------------------------------------------------------------
# CUSTOM SCALE COMPONENT
# -------------------------------------------------------------
def render_scale(index):
    st.write(f"**{index+1}. {questions[index]}**")

    st.markdown('<div class="scale-container">', unsafe_allow_html=True)

    # Button row
    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            selected = (st.session_state.answers[index] == i)
            cls = "button-on" if selected else "button-off"
            if st.button(str(i), key=f"q{index}_b{i}", help="", use_container_width=False):
                st.session_state.answers[index] = i

            # Apply styling after button creation
            st.markdown(
                f"""
                <script>
                    var btn = window.parent.document.querySelector('button[key="q{index}_b{i}"]');
                    if (btn) {{
                        btn.classList.add('{cls}');
                    }}
                </script>
                """,
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    # Label row
    st.markdown('<div class="label-row">', unsafe_allow_html=True)

    label_cols = st.columns(5)
    for i, col in enumerate(label_cols):
        with col:
            if st.button(labels[i], key=f"q{index}_l{i}"):
                st.session_state.answers[index] = i

    st.markdown('</div></div>', unsafe_allow_html=True)

    st.write("")


# -------------------------------------------------------------
# RENDER ALL QUESTIONS
# -------------------------------------------------------------
for q_i in range(20):
    render_scale(q_i)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0]*20
    st.rerun()

# -------------------------------------------------------------
# SCORING
# -------------------------------------------------------------
score = sum(st.session_state.answers)

def interpret(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    return "HSP"

profile = interpret(score)

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# VERSION NUMBER
# -------------------------------------------------------------
st.markdown(f'<div class="version-box">Version {VERSION}</div>', unsafe_allow_html=True)