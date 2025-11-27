import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# CSS – KNAP-STIL (C): valgt = rød, ikke valgt = mørkegrøn
# -------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color:#1A6333 !important;
    color:white !important;
    font-family:Arial, sans-serif !important;
}

/* Knapper i række */
.choice-row {
    display:flex;
    justify-content:space-between;
    margin:8px 0 22px 0;
}

.choice-btn {
    flex:1;
    margin:0 4px;
    padding:10px 0;
    text-align:center;
    font-size:1.0rem;
    border-radius:6px;
    cursor:pointer;
    user-select:none;
    border:1px solid #FFFFFF33;
    background-color:#0F4D27;
    color:white;
}

.choice-btn.selected {
    background-color:#C62828 !important;
    font-weight:700;
}

/* Røde knapper */
.stButton > button, .stDownloadButton > button {
    background:#C62828 !important;
    color:white !important;
    font-weight:600 !important;
    border-radius:8px !important;
    border:none !important;
    padding:0.7rem 1.4rem !important;
}
.stButton > button:hover {
    background:#B71C1C !important;
}

.center-logo {
    display:flex;
    justify-content:center;
    margin-top:10px;
}
.main-title {
    text-align:center;
    font-size:2.4rem;
    font-weight:900;
    margin-bottom:20px;
}
.question {
    font-size:1.2rem;
    font-weight:600;
    margin-top:22px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO
# -------------------------------------------------------------
st.markdown("""
<div class="center-logo">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="150">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTRO
# -------------------------------------------------------------
st.markdown("<div class='main-title'>DIN PERSONLIGE PROFIL</div>", unsafe_allow_html=True)

st.write("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er **ikke en diagnose**, men et værktøj til selvindsigt.
""")

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
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# BUTTON-BASED QUESTION RENDERING
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question'>{i+1}. {q}</div>", unsafe_allow_html=True)

    st.markdown("<div class='choice-row'>", unsafe_allow_html=True)

    # 5 knapper i én række
    for idx, label in enumerate(labels):

        selected = "selected" if st.session_state.answers[i] == idx else ""

        # unikt nøgle-navn
        key_name = f"btn_{i}_{idx}"

        if st.button(label, key=key_name):
            st.session_state.answers[i] = idx

        # vis farven (C-style)
        st.markdown(
            f"<div class='choice-btn {selected}' onclick=\"window.parent.document.getElementById('{key_name}').click()\">{label}</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [0]*len(questions)
    st.rerun()

# -------------------------------------------------------------
# SCORING
# -------------------------------------------------------------
def interpret(score):
    if score <= 26: return "Slow Processor"
    if score <= 53: return "Mellemprofil"
    return "HSP"

score = sum(st.session_state.answers)
profile = interpret(score)

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF
# -------------------------------------------------------------
def pdf(score, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor – Rapport", styles["Title"]))
    story.append(Paragraph(f"Score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    pdf(score, profile),
    file_name="rapport.pdf",
    mime="application/pdf"
)

st.markdown("<div style='font-size:0.8rem; margin-top:20px;'>Version v37</div>", unsafe_allow_html=True)