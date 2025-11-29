import streamlit as st
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# VERSION + TIMESTAMP
# -------------------------------------------------------------
VERSION = "v63"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# Floating version label in top-left corner
st.markdown(
    f"""
    <style>
        .version-box {{
            position: fixed;
            top: 6px;
            left: 10px;
            color: white;
            font-size: 0.70rem;
            z-index: 999999;
            opacity: 0.85;
        }}
    </style>
    <div class="version-box">{VERSION} • {TIMESTAMP}</div>
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

.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 18px;
    margin-bottom: 6px;
}

/* Scale row with selectable labels */
.scale-row {
    display: flex;
    justify-content: space-between;
    margin: 4px 0px 10px 0px;
}

.scale-item {
    flex: 1;
    text-align: center;
    padding: 6px 4px;
    margin: 0px 4px;
    border-radius: 6px;
    background-color: #2E7D4F;
    cursor: pointer;
    font-size: 0.90rem;
}

.scale-item:hover {
    background-color: #3E8D5F;
}

.scale-item.selected {
    background-color: #C62828 !important;
    font-weight: bold;
}

/* Red buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #B71C1C !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE
# -------------------------------------------------------------
st.markdown("<div style='text-align:center; font-size:2.3rem; font-weight:800; margin-bottom:20px;'>PROFIL</div>", unsafe_allow_html=True)

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

# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)
if "reset" not in st.session_state:
    st.session_state.reset = 0

# -------------------------------------------------------------
# QUESTION RENDERING
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, label in enumerate(labels):
        selected = st.session_state.answers[i] == idx
        css_class = "scale-item selected" if selected else "scale-item"

        if cols[idx].button(label, key=f"btn_{i}_{idx}_{st.session_state.reset}", use_container_width=True):
            st.session_state.answers[i] = idx

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)
    st.session_state.reset += 1
    st.rerun()

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.markdown("## Dit resultat")

if None in st.session_state.answers:
    st.markdown("Besvar alle spørgsmål for at se dit resultat.")
    st.markdown(f"<div style='font-size:0.8rem; margin-top:20px;'>Version {VERSION}</div>", unsafe_allow_html=True)
    st.stop()

total_score = sum([a for a in st.session_state.answers])
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

profile = interpret_score(total_score)

st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

profile_texts = {
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

for p in profile_texts[profile]:
    st.write(f"- {p}")

# -------------------------------------------------------------
# PDF generator
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)