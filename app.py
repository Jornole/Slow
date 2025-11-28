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
    background-color:#1A6333 !important;
    color:white !important;
    font-family:Arial, sans-serif !important;
}

/* Questions */
.question-text {
    font-size:1.15rem;
    font-weight:600;
    margin-top:22px;
    margin-bottom:6px;   /* ← tættere på labels */
}

/* Hide radiobutton dots */
.stRadio > div > label > div:first-child {
    display:none !important;
}

/* Force radios in one line */
.stRadio > div {
    display:flex !important;
    justify-content:space-between !important;
    width:100%;
}

/* LABELS CLICKABLE */
.scale-row {
    display:flex;
    justify-content:space-between;
    width:100%;
    margin-top:-2px;     /* ← tættere på knapper */
    margin-bottom:28px;
}

.scale-item {
    flex:1;
    text-align:center;
    cursor:pointer;
    font-size:0.9rem;
    color:white;
}

.scale-item:hover {
    color:#FF9999;
    font-weight:600;
}

.selected {
    color:#FF4444;
    font-weight:700;
}

/* Red buttons */
.stButton > button, .stDownloadButton > button {
    background:#C62828 !important;
    color:white !important;
    border-radius:8px;
    padding:0.65rem 1.4rem !important;
    font-weight:600 !important;
    border:none !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin-top:20px; margin-bottom:5px;'>
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE + INTRO
# -------------------------------------------------------------
st.markdown("<div class='main-title'>DIN PERSONLIGE PROFIL</div>", unsafe_allow_html=True)

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
    "Jeg bliver let distraheret, når der sker meget omkring mig."
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# Session state
if "answers" not in st.session_state:
    st.session_state.answers = [0]*len(questions)
if "reset" not in st.session_state:
    st.session_state.reset = 0

# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    selected_value = st.session_state.answers[i]

    choice = st.radio(
        "",
        options=list(range(5)),
        key=f"radio_{i}_{st.session_state.reset}",
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda x: ""   # hide numbers
    )

    st.session_state.answers[i] = choice

    row_html = "<div class='scale-row'>"
    for idx, lbl in enumerate(labels):
        css = "scale-item selected" if choice == idx else "scale-item"
        row_html += f"""
            <div class='{css}' onclick="window.parent.document.getElementById('radio_{i}_{st.session_state.reset}').querySelectorAll('input')[{idx}].click()">
                {lbl}
            </div>
        """
    row_html += "</div>"

    st.markdown(row_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0]*len(questions)
    st.session_state.reset += 1
    st.rerun()

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
score = sum(st.session_state.answers)

def interpret_score(s):
    if s <= 26: return "Slow Processor"
    elif s <= 53: return "Mellemprofil"
    return "HSP"

profile = interpret_score(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
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
        "Du har god udholdenhed, når du arbejder i dit eget tempo."
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
# PDF GENERATOR
# -------------------------------------------------------------
def generate_pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1,12))

    for i,q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)

# VERSION
st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version V40</div>", unsafe_allow_html=True)