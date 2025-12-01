import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# Version badge
version = "v126"
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
# GLOBAL CSS (v78 DESIGN)
# -------------------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color:#1A6333 !important;
    color:white !important;
    font-family: Arial, sans-serif;
}
.question-text {
    font-size:1.15rem;
    font-weight:600;
    margin-top:22px;
    margin-bottom:10px;
}
.choice-btn {
    background-color:#C62828;
    color:white;
    padding:10px 14px;
    border:none;
    border-radius:8px;
    font-size:0.95rem;
    font-weight:600;
    cursor:pointer;
    margin-right:8px;
    margin-bottom:8px;
}
.choice-btn.selected {
    background-color:white !important;
    color:#C62828 !important;
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

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# JS → PYTHON kommunikation (fejlfri metode)
# -------------------------------------------------------------
# Lyt efter værdier sendt fra JavaScript
if "incoming" in st.session_state:
    q, v = st.session_state.incoming
    st.session_state.answers[q] = v
    del st.session_state.incoming

# -------------------------------------------------------------
# RENDER SPØRGSMÅL + KNAPPER
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    btn_html = ""
    for v, label in enumerate(labels):
        selected = "selected" if st.session_state.answers[i] == v else ""
        btn_html += (
            f"<button class='choice-btn {selected}' "
            f"onclick='sendToStreamlit({i},{v})'>{label}</button>"
        )

    st.markdown(btn_html, unsafe_allow_html=True)

# JS-kode (stabil til Streamlit Cloud)
st.markdown("""
<script>
function sendToStreamlit(q, v){
    const data = {isIncoming:true, q:q, v:v};
    window.parent.postMessage({
        type: "streamlit:renderEvent",
        data: data
    }, "*");
}
</script>
""", unsafe_allow_html=True)

# Catch browser messages
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data?.type === "streamlit:renderEvent" &&
        event.data?.data?.isIncoming === true){

        const pyData = {question: event.data.data.q,
                        value: event.data.data.v};

        // Send to Python session_state
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setSessionState",
            key: "incoming",
            value: [pyData.question, pyData.value]
        }, "*");

        // Soft-rerun ONLY updates Python-state
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:rerun"
        }, "*");
    }
});
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# SCORE
# -------------------------------------------------------------
safe = [a if a is not None else 0 for a in st.session_state.answers]
score = sum(safe)

def interpret(s):
    if s <= 26:
        return "Slow Processor"
    if s <= 53:
        return "Mellemprofil"
    return "HSP"

profile = interpret(score)

st.header("Dit resultat")
st.subheader(f"Score: {score} / 80")
st.subheader(f"Profil: {profile}")

# -------------------------------------------------------------
# PDF
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe[i]]}",
                               styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)