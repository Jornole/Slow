import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
VERSION = "v96"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# Small version box top-left
st.markdown(
    f"""
    <div style="
        font-size:0.85rem;
        background-color:#144d27;
        padding:6px 10px;
        width:fit-content;
        border-radius:6px;
        margin-bottom:8px;
    ">
        Version {VERSION} — {TIMESTAMP}
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    /* Logo centreret */
    .center-logo {
        display:flex;
        justify-content:center;
        margin-top:8px;
        margin-bottom:6px;
    }

    .main-title {
        font-size:2.2rem;
        font-weight:800;
        text-align:center;
        margin-top:6px;
        margin-bottom:18px;
    }

    .question-text {
        font-size:1.05rem;
        font-weight:600;
        margin-top:16px;
        margin-bottom:6px;
    }

    /* Layout for label-buttons: container and text markers */
    .labels-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        width:100%;
        padding:0 6%;
        box-sizing:border-box;
        margin-bottom:6px;
    }

    .label-text {
        flex:1;
        text-align:center;
        font-size:0.95rem;
        color:#ffffff;
        padding:6px 4px;
        user-select:none;
    }

    .label-text.selected {
        color:#ff4444;
        font-weight:700;
    }

    /* Small helper to space down from labels to next question */
    .after-labels { margin-bottom: 14px; }

    /* Red buttons (reset + pdf) */
    .stButton > button, .stDownloadButton > button {
        background-color: #C62828 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B71C1C !important;
    }

    /* Narrow screens */
    @media (max-width:420px) {
        .labels-row { padding: 0 3%; }
        .label-text { font-size:0.85rem; padding:6px 2px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + TITLE + INTRO
# -------------------------------------------------------------
st.markdown(
    """
    <div class="center-logo">
        <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown(
    """
    Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
    og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

    Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

    Testen er <u><b>ikke en diagnose</b></u>, men et psykologisk værktøj til selvindsigt.
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
# SESSION STATE init
# -------------------------------------------------------------
if "answers" not in st.session_state:
    # default 0 (vælg aldrig som 0) — det er den tidligere opførsel
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS: each label rendered as a Streamlit button in a horizontal layout
# - We use st.columns to place 5 small buttons horizontally.
# - Underneath we render the label-row (text) with the selected label highlighted red.
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    cols = st.columns(5, gap="small")
    # create 5 small buttons (labels act as buttons)
    for idx, col in enumerate(cols):
        label_text = labels[idx]
        # Unique key for button
        btn_key = f"btn_q{i}_{idx}"

        # Render the button (invisible styling controlled by CSS globally)
        # The button text is the label; pressing updates session_state.answers[i]
        with col:
            clicked = st.button(label_text, key=btn_key)
            if clicked:
                st.session_state.answers[i] = idx

    # Render the textual label row underneath, with selected one colored red.
    # We show the labels as simple centered texts — selected one gets class 'selected'
    label_html = "<div class='labels-row'>"
    for idx, lab in enumerate(labels):
        sel_class = "selected" if st.session_state.answers[i] == idx else ""
        label_html += f"<div class='label-text {sel_class}'>{lab}</div>"
    label_html += "</div><div class='after-labels'></div>"

    st.markdown(label_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    # Reset all answers to 0 (Aldrig) — one click only
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# SCORE + PROFILE
# -------------------------------------------------------------
def interpret_score(score: int) -> str:
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
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
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------
# PDF GENERATOR
# -------------------------------------------------------------
def generate_pdf(score: int, profile_str: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Rapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile_str}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Karakteristika for din profil:", styles["Heading2"]))
    for s in PROFILE_TEXT[profile_str]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(Paragraph(f"{i+1}. {q} – {labels[st.session_state.answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)

# End of app.py v96