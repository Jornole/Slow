import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# VERSION + TIMESTAMP (v119)
# -------------------------------------------------------------
version = "v119"
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

/* Vandrette knapper i én linje */
.choice-row {
    display: flex;
    flex-direction: row;
    gap: 8px;
    margin: 6px 0 16px 0;
}

.choice-btn {
    background-color: #C62828;
    border-radius: 8px;
    padding: 5px 10px;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    min-width: 72px;
    text-align: center;
}

.choice-btn.selected {
    background-color: #ffffff !important;
    color: #C62828 !important;
}

.choice-btn:hover {
    background-color: #B71C1C;
}

.reset-btn {
    background-color: #C62828 !important;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    color: white !important;
    border: none;
    cursor: pointer;
    margin-top: 15px;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO + TITLE
# -------------------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:center; margin-top:10px;">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:2.3rem; font-weight:800; text-align:center; margin-top:10px; margin-bottom:25px;">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u><b>ikke en diagnose</b></u>, men et psykologisk værktøj til selvindsigt.
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
    "Jeg bliver let distraheret, når der sker meget omkring mig.",
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# HTML & JS BUTTONS
# -------------------------------------------------------------
js_blocks = []

for i, q in enumerate(questions):

    st.markdown(f"""
        <div style="font-size:1.15rem; font-weight:600; margin-top:22px; margin-bottom:6px;">
            {i+1}. {q}
        </div>
    """, unsafe_allow_html=True)

    # Build row of buttons
    html_buttons = ""
    for v, label in enumerate(labels):
        selected = "selected" if st.session_state.answers[i] == v else ""
        html_buttons += f"""
            <button class="choice-btn {selected}" id="q{i}_{v}" onclick="pickAnswer({i}, {v})">{label}</button>
        """

    st.markdown(f"""
        <div class="choice-row">
            {html_buttons}
        </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# JAVASCRIPT – store session state without reload
# -------------------------------------------------------------
st.markdown("""
<script>
function pickAnswer(qIndex, value) {
    const buttons = document.querySelectorAll(`[id^="q${qIndex}_"]`);
    buttons.forEach(btn => btn.classList.remove("selected"));

    const active = document.getElementById(`q${qIndex}_${value}`);
    active.classList.add("selected");

    const payload = {index: qIndex, val: value};

    fetch("/_stcore/set", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });
}
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Use Streamlit endpoint to store values
# -------------------------------------------------------------
def set_answer():
    import json, sys
    body = sys.stdin.read()
    data = json.loads(body)
    st.session_state.answers[data["index"]] = data["val"]
    return "OK"

st.experimental_get_query_params()  # required for backend wiring
st.experimental_connect("set", set_answer)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

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

safe = [a if a is not None else 0 for a in st.session_state.answers]
score = sum(safe)
profile = interpret_score(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF GENERATION
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport", generate_pdf(score, profile),
                    file_name="HSP_SlowProcessor_Rapport.pdf",
                    mime="application/pdf")