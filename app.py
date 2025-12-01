# app.py (Version v123)
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# META
# -------------------------------------------------------------
VERSION = "v123"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

# -------------------------------------------------------------
# PAGE
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# top-left version/timestamp
st.markdown(
    f"<div style='position:relative; left:0; font-size:0.85rem; "
    f"background:#144d27; padding:6px 10px; border-radius:6px; display:inline-block'>"
    f"Version {VERSION} — {TIMESTAMP}</div>",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# STYLES
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    .center-logo { display:flex; justify-content:center; margin-top:12px; margin-bottom:6px; }
    .main-title { font-size:2.3rem; font-weight:800; text-align:center; margin-top:6px; margin-bottom:22px; }
    .question-text { font-size:1.15rem; font-weight:600; margin-top:18px; margin-bottom:6px; }

    /* Style for our custom button-like divs (rendered via st.button) */
    .small-btn {
        padding: 6px 10px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.06);
        font-weight:600;
    }

    /* We'll rely on Streamlit's generated button, but adjust look via class */
    /* Ensure columns are narrow on desktop but responsive */
    .col-wrapper { padding: 0 4px; }

    /* Score/result styles */
    .result-block { background: rgba(0,0,0,0.06); padding:10px; border-radius:8px; margin-top:12px; }

    /* Make the standard Streamlit buttons appear similar (small) */
    .stButton > button, .stDownloadButton > button {
        border-radius:8px !important;
        padding: 0.35rem 0.6rem !important;
        font-weight:600 !important;
        min-width: 58px !important;
        height: 38px !important;
    }

    /* Selected style applied via inline style when rendering */
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + TITLE + INTRO
# -------------------------------------------------------------
st.markdown("""
<div class="center-logo">
    <img src="https://raw.githubusercontent.com/Jornole/Slow/main/logo.png" width="160">
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">DIN PERSONLIGE PROFIL</div>', unsafe_allow_html=True)

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner.

Du besvarer 20 udsagn på en skala fra **Aldrig** til **Altid**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
""", unsafe_allow_html=True)

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
    st.session_state.answers = [None] * len(questions)

# helper to set answer for question i
def set_answer(i, val):
    st.session_state.answers[i] = val
    # do NOT call experimental_rerun or similar — Streamlit will rerun automatically on button click,
    # but we don't force extra reruns. The update in session_state will reflect immediately after rerun.

# -------------------------------------------------------------
# RENDER QUESTIONS (5 buttons per question, in-line)
# - We create 5 narrow columns so buttons sit on one line.
# - Use st.button in each column. Clicking triggers Streamlit rerun but updates session_state.
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # Create five narrow columns (proportion array). The actual width depends on the viewport;
    # these ratios keep them side-by-side on common widths.
    cols = st.columns([1,1,1,1,1], gap="small")
    for idx, col in enumerate(cols):
        with col:
            # Inline style for selected state: make the selected button red background, white text.
            is_selected = (st.session_state.answers[i] == idx)
            if is_selected:
                btn_style = "background-color:#FF5555; color:white; border-radius:8px; padding:6px 8px; width:100%;"
            else:
                btn_style = "background-color:white; color:#111; border-radius:8px; padding:6px 8px; width:100%;"

            # We render a small HTML button that calls the Streamlit button via hidden st.button.
            # Approach: show a styled <div> (visual), and a tiny invisible st.button over it to capture clicks.
            # But Streamlit doesn't allow us to attach arbitrary JS to its buttons; simplest reliable
            # approach is to use st.button directly and rely on its default reactivity.

            # Using st.button with a unique key:
            clicked = col.button(labels[idx], key=f"q_{i}_{idx}")

            if clicked:
                set_answer(i, idx)

    # Immediately show textual labels under the buttons if you still want (optional)
    # Here we don't show extra label line — the button text itself is the label.

# -------------------------------------------------------------
# RESET BUTTON (placed after all questions)
# -------------------------------------------------------------
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)
    # No experimental_rerun; Streamlit will rerun automatically due to this button click.

# -------------------------------------------------------------
# SCORE & PROFILE
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

profile = interpret_score(total_score)

st.markdown("<div class='result-block'>", unsafe_allow_html=True)
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

st.write("### Karakteristika for din profil:")
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
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# PDF
# -------------------------------------------------------------
def generate_pdf(score, profile):
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe_answers[i]]}", styles["BodyText"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)