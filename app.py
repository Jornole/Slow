# app.py - Version v130
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

# -------------------------------------------------------------
# VERSION + TIMESTAMP (v130)
# -------------------------------------------------------------
version = "v130"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(
    f"""
    <div style="font-size:0.85rem; background-color:#144d27;
                padding:6px 10px; width:fit-content;
                border-radius:6px; margin-bottom:10px;">
        Version {version} — {timestamp}
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# GLOBAL CSS (match v78 look; tweak for buttons-as-labels)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    .center-logo {
        display:flex;
        justify-content:center;
        margin-top:10px;
        margin-bottom:5px;
    }

    .main-title {
        font-size:2.3rem;
        font-weight:800;
        text-align:center;
        margin-top:10px;
        margin-bottom:25px;
    }

    .question-text {
        font-size:1.15rem;
        font-weight:600;
        margin-top:22px;
        margin-bottom:6px;
    }

    /* scale row wrapper */
    .scale-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        width:100%;
        margin-bottom:12px;
        padding:0 6%;
        box-sizing:border-box;
    }

    /* style for the Streamlit buttons (these apply to all buttons; reset/pdf keep red) */
    .scale-btn {
        background: transparent;
        color: #ffffff;
        border: none;
        font-size: 0.95rem;
        padding: 8px 6px;
        width: 100%;
        text-align: center;
    }

    /* Selected appearance */
    .scale-btn-selected {
        color: #ff4444 !important;
        font-weight: 700;
    }

    /* Keep the red look for reset/download */
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

    /* Make Streamlit column buttons compact so 5 can fit on one line */
    .stButton > button {
        min-width: 60px !important;
        padding: 0.25rem 0.4rem !important;
        height: 38px !important;
        font-size: 0.9rem !important;
    }

    @media (max-width:420px) {
        .scale-row { padding:0 3%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + TITLE + INTRO (kept same)
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
# RENDER QUESTIONS
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # Create 5 narrow columns so buttons sit side-by-side
    cols = st.columns([1,1,1,1,1])

    for v, (col, lab) in enumerate(zip(cols, labels)):
        # Build a key for the button
        key = f"q{i}_{v}"

        # Visual: we will render a compact Streamlit button inside the column.
        # When clicked, it stores the value in session_state.
        with col:
            clicked = st.button(lab, key=key)
            if clicked:
                st.session_state.answers[i] = v

    # After the buttons, re-render a small label row (so spacing/text matches v78)
    # We render it via markdown but the primary interaction is via buttons above.
    selected_index = st.session_state.answers[i]
    # build html for the label row, matching styles: selected label gets red
    html = "<div class='scale-row'>"
    for v, lab in enumerate(labels):
        cls = "scale-btn-selected" if selected_index == v else ""
        html += f"<div style='flex:1; text-align:center; font-size:0.95rem; padding:4px 6px; color: {'#ff4444' if cls else '#ffffff'}; font-weight: {'700' if cls else '400'}'>{lab}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# SCORE + PROFILE (unchanged)
# -------------------------------------------------------------
def interpret_score(score):
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"

safe_answers = [a if a is not None else 0 for a in st.session_state.answers]
total_score = sum(safe_answers)
profile = interpret_score(total_score)

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

# -------------------------------------------------------------
# RESULT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe_answers[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)