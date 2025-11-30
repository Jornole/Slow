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

# version + timestamp
version = "v98"
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
# CSS (bevart simpelt for nu)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp { background-color:#1A6333 !important; color:white !important; font-family: Arial, sans-serif !important; }
    .main-title { font-size:2.3rem; font-weight:800; text-align:center; margin-top:10px; margin-bottom:25px; }
    .question-text { font-size:1.15rem; font-weight:600; margin-top:22px; margin-bottom:6px; }
    .stButton > button { background-color:#C62828 !important; color:white !important; border-radius:8px !important; padding:0.65rem 1.4rem !important; font-weight:600 !important; border:none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + TITLE + intro
# -------------------------------------------------------------
st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)
st.markdown(
    """
    Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige
    og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

    Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# QUESTIONS + LABELS
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
# SESSION STATE (answers)
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# Load existing values if keys are in session_state already (keeps state between reruns)
# (vi undgår href-navigation helt i denne version for at stoppe browser reload)

# -------------------------------------------------------------
# RENDER QUESTIONS (brug radio for at undgå browser navigation)
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # sæt current default (hvis tidligere valgt)
    current = st.session_state.answers[i]
    # bruger st.radio (dette tricker en Streamlit-rerun, men uden browser reload/navigation)
    choice = st.radio(
        label="",
        options=list(range(len(labels))),
        format_func=lambda x, lab=labels: labels[x],
        index=current if current is not None else 0,
        key=f"radio_{i}",
        horizontal=True
    )
    # gem valget i vores answers state
    st.session_state.answers[i] = choice

# -------------------------------------------------------------
# RESET
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)
    try:
        st.experimental_set_query_params()  # ryd query params hvis nogle er der
    except:
        pass

# -------------------------------------------------------------
# SCORE + PROFILE (inkl. PROFILE_TEXT — genindsat)
# -------------------------------------------------------------
safe_answers = [a if a is not None else 0 for a in st.session_state.answers]
total_score = sum(safe_answers)

def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

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

profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------
# PDF (uændret funktion)
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe_answers[i]]}", styles["BodyText"]))
    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)