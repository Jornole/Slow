import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# PAGE CONFIG
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

/* LOGO */
.center-logo {
    text-align:center;
    margin-top:15px;
    margin-bottom:10px;
}

/* QUESTION TEXT */
.question-text {
    font-size:1.1rem;
    font-weight:600;
    margin-top:22px;
    margin-bottom:10px;
}

/* SCALE WRAPPER */
.scale-wrapper {
    display:flex;
    width:100%;
    justify-content:space-between;
    margin-top:4px;
    margin-bottom:25px;
}

/* TEXTPICKER ITEM */
.scale-item {
    flex:1;
    text-align:center;
    font-size:1rem;
    cursor:pointer;
    padding:8px 0;
    color:white;
    border-radius:6px;
}

.scale-item:hover {
    background-color:rgba(255,255,255,0.12);
}

/* SELECTED STATE */
.scale-item.selected {
    color:#FF5252 !important;
    font-weight:700;
}

/* RED BUTTONS */
.stButton > button, .stDownloadButton > button {
    background:#C62828 !important;
    color:white !important;
    border:none !important;
    border-radius:8px !important;
    padding:0.7rem 1.3rem !important;
    font-weight:600 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background:#B71C1C !important;
}

.version-tag {
    font-size:0.8rem;
    margin-top:30px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div class='center-logo'>
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO
# -------------------------------------------------------------
st.title("DIN PERSONLIGE PROFIL")
st.write("""
Denne test giver dig et indblik i, hvordan du bearbejder følelsesmæssige 
og sansemæssige indtryk.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.
""")

# -------------------------------------------------------------
# DATA
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
# SESSION
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS (PURE TEXT BUTTONS)
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # Start scale row
    st.markdown("<div class='scale-wrapper'>", unsafe_allow_html=True)

    for idx, label in enumerate(labels):
        selected = "selected" if st.session_state.answers[i] == idx else ""

        # Hidden button used as trigger
        if st.button(f"{label}_{i}", key=f"btn_{i}_{idx}", help=""):
            st.session_state.answers[i] = idx
            st.rerun()

        # Visual clickable label
        st.markdown(
            f"""
            <div class="scale-item {selected}" 
                 onclick="window.parent.document.getElementById('btn_{i}_{idx}').click()">
                {label}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0] * len(questions)
    st.rerun()

# -------------------------------------------------------------
# INTERPRETATION
# -------------------------------------------------------------
def interpret(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

score = sum(st.session_state.answers)
profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF GENERATOR
# -------------------------------------------------------------
def pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1,12))

    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button("Download PDF-rapport",
                   pdf(score, profile),
                   file_name="rapport.pdf",
                   mime="application/pdf")

# -------------------------------------------------------------
# VERSION NUMBER
# -------------------------------------------------------------
st.markdown("<div class='version-tag'>Version v26</div>", unsafe_allow_html=True)