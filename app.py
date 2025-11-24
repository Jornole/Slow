import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="HSP / Slow Processing Test", layout="centered")

# -------------------------
# Stil (større sliders + farver)
# -------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}

h1, h2, h3, p, label {
    color: white !important;
}

.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 12px;
}

/* Gør slideren større */
.stSlider > div > div > div {
    height: 22px !important;
}

.stSlider > div > div > div > div {
    height: 22px !important;
}

.stSlider > div > div > div::before {
    height: 22px !important;
}

.stSlider > div > div > div > div > div {
    width: 28px !important;  
    height: 28px !important; 
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Spørgsmål
# -------------------------
questions = [
    "Jeg bliver let overvældet af indtryk.",
    "Jeg opdager små detaljer, som andre ofte overser.",
    "Jeg bruger længere tid på at tænke ting igennem.",
    "Jeg foretrækker rolige omgivelser.",
    "Jeg reagerer stærkt på uventede afbrydelser.",
    "Jeg bearbejder information dybt og grundigt.",
    "Jeg har brug for ekstra tid til at omstille mig.",
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

st.title("HSP / Slow Processing Test")
st.write("Vælg en værdi for hvert spørgsmål (0 = aldrig, 4 = altid).")

# -------------------------
# Session state initialisering
# -------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# -------------------------
# Indsaml svar (og opdater session state)
# -------------------------
answers = []
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.session_state.answers[i] = val
    answers.append(val)

# -------------------------
# Fortolkning
# -------------------------
def interpret_score(score):
    if score <= 26:
        return "Du scorer lavt – dette peger mod Slow Processor-træk."
    elif score <= 53:
        return "Du ligger i mellemprofil (blandet træk)."
    else:
        return "Du scorer højt – dette peger mod HSP (højsensitiv)."

# -------------------------
# Resultat
# -------------------------
total_score = sum(st.session_state.answers)

st.header("Dit resultat")
st.subheader(f"Samlet score: **{total_score} / 80**")
st.write(interpret_score(total_score))

# -------------------------
# PDF-generering
# -------------------------
def generate_pdf(score):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("HSP / Slow Processing Test – Resultatrapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(interpret_score(score), styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Besvarelser:", styles["Heading2"]))
    for idx, q in enumerate(questions):
        story.append(Paragraph(f"{idx+1}. {q} – Svar: {st.session_state.answers[idx]}", styles["BodyText"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score),
    file_name="HSP_SlowProcessing_Rapport.pdf",
    mime="application/pdf"
)