# app.py (v105)
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# META
# -------------------------------------------------------------
VERSION = "v105"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# show version + timestamp top-left
st.markdown(
    f"""
    <div style="font-size:0.85rem; background-color:#144d27;
                color: #ffffff; padding:6px 10px; width:fit-content;
                border-radius:6px; margin-bottom:8px;">
        Version {VERSION} — {TIMESTAMP}
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# GLOBAL CSS (styling of scale, buttons and PDF/reset)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    /* Center logo */
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

    /* layout for the 5-label scale (text-buttons look) */
    .scale-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        width:100%;
        margin-bottom:10px;
        padding:0 6%;
        box-sizing:border-box;
    }

    /* the visible label text (we also render real buttons, but we style them below) */
    .scale-label {
        flex:1;
        text-align:center;
        font-size:0.95rem;
        color: white;
        padding:6px 4px;
        user-select: none;
    }

    /* selected label style */
    .scale-label.selected {
        color: #ff4444;
        font-weight:700;
    }

    /* Style Streamlit buttons that we use for label-click (make them invisible, so only the styled text is visible).
       We target only button elements inside .scale-btn-wrapper by adding a small wrapper next to the button (works reliably). */
    .scale-btn {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }

    /* Keep PDF/Reset buttons red and visible */
    .stButton > button, .stDownloadButton > button {
        background-color: #C62828 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B71C1C !important;
    }

    @media (max-width:420px) {
        .scale-row { padding:0 3%; }
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
        <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="150">
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
    "Jeg bliver let distraheret, når der sker meget omkring mig."
]

labels = ["Aldrig", "Sjældent", "Nogle gange", "Ofte", "Altid"]

# -------------------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    # default 0 = Aldrig (matches previous versions behavior)
    st.session_state.answers = [0] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS — each question shows:
#  - an invisible Streamlit button per label (so clicking triggers Streamlit event)
#  - a styled label row (visual) that shows which is selected
# This combination gives clickable labels and immediate visual feedback.
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # create 5 equal columns so the buttons align horizontally
    cols = st.columns(5)

    # render invisible buttons (used only for click handling)
    for idx in range(5):
        with cols[idx]:
            # invisible button key specific per question+idx
            btn_key = f"q_{i}_btn_{idx}"
            # We create a tiny button and hide it with CSS (.scale-btn)
            clicked = st.button(label=f"pick_{i}_{idx}", key=btn_key, help="", use_container_width=True)
            if clicked:
                st.session_state.answers[i] = idx

    # After buttons, render visible labels row reflecting selection
    # Use HTML markup so we can apply .selected class to the chosen label
    label_html = "<div class='scale-row'>"
    for idx, lab in enumerate(labels):
        sel_cls = "selected" if st.session_state.answers[i] == idx else ""
        # Each label is plain text (styled); clicking is done via the invisible button above
        label_html += f"<div class='scale-label {sel_cls}'>{lab}</div>"
    label_html += "</div>"

    st.markdown(label_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
reset_clicked = st.button("Nulstil svar")
if reset_clicked:
    st.session_state.answers = [0] * len(questions)
    # No explicit rerun or query-param modification — Streamlit will rerun after the button click automatically.

# -------------------------------------------------------------
# INTERPRETATION & RESULT
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
st.subheader(f"Profil: {profile}")

PROFILE_TEXT = {
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

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------
# PDF GENERATION
# -------------------------------------------------------------
def generate_pdf(score: int, profile: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HSP / Slow Processor Test – Rapport", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Samlet score: {score} / 80", styles["Heading2"]))
    story.append(Paragraph(f"Profil: {profile}", styles["Heading2"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Karakteristika for din profil:", styles["Heading2"]))
    for s in PROFILE_TEXT[profile]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Dine svar:", styles["Heading2"]))
    for i, q in enumerate(questions):
        sel_label = labels[st.session_state.answers[i]] if 0 <= st.session_state.answers[i] < len(labels) else "Aldrig"
        story.append(Paragraph(f"{i+1}. {q} – {sel_label}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)