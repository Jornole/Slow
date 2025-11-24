import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="HSP / Slow Processing Test", layout="centered")


# -----------------------------------------------------------
# CSS – BAGGRUNDSFARVE, TEKST, KNAPPER, HORISONTAL LAYOUT
# -----------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #1A6333 !important;  /* Grøn mockup-farve */
    color: white !important;
}

.question-text {
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
    margin-bottom: 10px;
}

/* Gør kolonner mere mobilvenlige */
.css-1kyxreq, .css-1r6slb0, .css-12ttj6m {
    flex-direction: row !important;
}

/* Knapper i horisontal række */
div.stButton > button {
    background-color: white !important;
    color: black !important;
    padding: 12px;
    border-radius: 10px;
    border: none;
    font-size: 1.1rem;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# SPØRGSMÅL (20)
# -----------------------------------------------------------
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


# -----------------------------------------------------------
# FUNKTION: 5 HORIZONTAL KNAPPER
# -----------------------------------------------------------
def horizontal_scale(question, key):
    st.markdown(f"<div class='question-text'>{question}</div>", unsafe_allow_html=True)

    if key not in st.session_state:
        st.session_state[key] = None

    cols = st.columns(5)  # 5 kolonner = 5 vandrette knapper
    for i, col in enumerate(cols):
        with col:
            if st.button(str(i), key=f"{key}_{i}"):
                st.session_state[key] = i

    return st.session_state[key]


# -----------------------------------------------------------
# UI
# -----------------------------------------------------------
st.title("HSP / Slow Processing Test")
st.write("Vælg en værdi for hvert spørgsmål (0 = aldrig, 4 = altid).")


# -----------------------------------------------------------
# INDSAML SVAR
# -----------------------------------------------------------
answers = []
for i, q in enumerate(questions):
    answers.append(horizontal_scale(q, f"q_{i}"))


# -----------------------------------------------------------
# SCOREFORTOLKNING
# -----------------------------------------------------------
def interpret_score(score):
    if score <= 15:
        return "Du scorer meget lavt – dette peger mod **Slow Processor**."
    elif score <= 35:
        return "Du ligger i **balanceret område** mellem Slow Processing og HSP."
    else:
        return "Du scorer højt – dette peger mod **HSP (højsensitiv)**."


# Kun vis resultat, hvis ALT er besvaret
if all(a is not None for a in answers):
    total_score = sum(answers)

    st.header("Dit resultat")
    st.subheader(f"Samlet score: **{total_score} / 80**")
    st.write(interpret_score(total_score))


    # -----------------------------------------------------------
    # PDF-GENERERING
    # -----------------------------------------------------------
    def generate_pdf(score):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        story = []
        story.append(Paragraph("<b>HSP / Slow Processing Test – Resultatrapport</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"Samlet score: <b>{score} / 80</b>", styles["Heading2"]))
        story.append(Paragraph(interpret_score(score), styles["BodyText"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Besvarelser:</b>", styles["Heading2"]))
        for i, q in enumerate(questions):
            story.append(Paragraph(f"{i+1}. {q} – Svar: {answers[i]}", styles["BodyText"]))

        doc.build(story)
        buffer.seek(0)
        return buffer


    st.download_button(
        "Download PDF-rapport",
        data=generate_pdf(total_score),
        file_name="HSP_SlowProcessing_Rapport.pdf",
        mime="application/pdf"
    )