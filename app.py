import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

version = "v129"
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
# CSS — kun styling, ingen funktion påvirkes
# -------------------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
    font-family: Arial, sans-serif !important;
}

.question {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 10px;
}

.choice-btn > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.4rem 0.6rem !important;
    font-size: 0.85rem !important;
    border: none !important;
    width: 100% !important;
}

.choice-btn > button:hover {
    background-color: #B71C1C !important;
}
</style>
""", unsafe_allow_html=True)


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
    "Jeg bliver let distraheret, når der sker meget omkring mig.",
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]


# -------------------------------------------------------------
# SESSION INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)


# -------------------------------------------------------------
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5, gap="small")
    for j, col in enumerate(cols):
        with col:
            if st.button(labels[j], key=f"q{i}_{j}", use_container_width=True):
                st.session_state.answers[i] = j


# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)


# -------------------------------------------------------------
# RESULTAT
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

PROFILE_TEXT = {
    "HSP": [
        "Du registrerer flere nuancer i både indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du reagerer stærkt på stimuli og kan blive overstimuleret.",
        "Du har en rig indre verden og et fintfølende nervesystem.",
        "Du er empatisk og opmærksom på andre.",
        "Du har brug for ro og pauser for at lade op.",
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo og med forudsigelighed.",
        "Du bearbejder indtryk grundigt, men langsomt.",
        "Du har brug for ekstra tid til omstilling og beslutninger.",
        "Du trives med faste rammer og struktur.",
        "Du kan føle dig presset, når tingene går hurtigt.",
        "Du har god udholdenhed, når du arbejder i dit eget tempo.",
    ],
    "Mellemprofil": [
        "Du veksler naturligt mellem hurtig og langsom bearbejdning.",
        "Du håndterer de fleste stimuli uden at blive overvældet.",
        "Du har en god balance mellem intuition og eftertænksomhed.",
        "Du kan tilpasse dig forskellige miljøer og tempoer.",
        "Du bliver påvirket i perioder, men finder hurtigt balancen igen.",
        "Du fungerer bredt socialt og mentalt i mange typer situationer.",
    ],
}

for line in PROFILE_TEXT[profile]:
    st.write("- " + line)


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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)