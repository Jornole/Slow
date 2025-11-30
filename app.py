import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
import pytz

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# VERSION + TIMESTAMP (v91)
# -------------------------------------------------------------
version = "v91"
tz = pytz.timezone("Europe/Copenhagen")
timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M")

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
# GLOBAL CSS — v78 DESIGN (vandret skala, ingen knapfarver)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    .question-text {
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 22px;
        margin-bottom: 8px;
    }

    .scale-row {
        display: flex;
        gap: 26px;
        margin-bottom: 25px;
        font-size: 1.1rem;
    }

    .scale-item {
        padding: 4px 6px;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.15s;
    }

    .selected {
        color: #ff4444 !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# LOGO + TITLE
# -------------------------------------------------------------
st.markdown(
    """
    <div style="display:flex; justify-content:center; margin-top:5px; margin-bottom:5px;">
        <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div style='font-size:2.3rem; font-weight:800; text-align:center;'>DIN PERSONLIGE PROFIL</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige  
    og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.  

    Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.  
    Testen er <u><b>ikke en diagnose</b></u>, men et psykologisk værktøj til selvindsigt.
    """,
    unsafe_allow_html=True
)

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
# RENDER QUESTIONS — NO RELOAD
# -------------------------------------------------------------
for i, q in enumerate(questions):

    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(len(labels))

    for idx, (col, label) in enumerate(zip(cols, labels)):
        with col:
            is_selected = (st.session_state.answers[i] == idx)
            css_class = "selected" if is_selected else ""
            if st.button(label, key=f"q{i}_v{idx}"):
                st.session_state.answers[i] = idx

            st.markdown(
                f"<div class='scale-item {css_class}'>{label}</div>",
                unsafe_allow_html=True
            )


# -------------------------------------------------------------
# RESET BUTTON — WORKS PERFECTLY
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
total = sum(safe)
profile = interpret_score(total)

st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
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

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

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
        ans = safe[i]
        story.append(Paragraph(f"{i+1}. {q} – {labels[ans]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)