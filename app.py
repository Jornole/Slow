# app.py — v122
import streamlit as st
import streamlit.components.v1 as components
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
import json

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# VERSION + TIMESTAMP (v122)
# -------------------------------------------------------------
version = "v122"
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
# GLOBAL CSS (styles tuned to match v78 look)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    .center-logo { display:flex; justify-content:center; margin-top:10px; margin-bottom:5px; }

    .main-title { font-size:2.3rem; font-weight:800; text-align:center; margin-top:10px; margin-bottom:25px; }

    .question-text {
        font-size:1.15rem;
        font-weight:600;
        margin-top:22px;
        margin-bottom:12px;
    }

    /* inline choices container (five labels on one line) */
    .choice-row {
        display:flex;
        gap:18px;
        align-items:center;
        flex-wrap:wrap;
        margin-bottom:18px;
    }

    .choice-label {
        color: #ffffff;
        text-decoration: none;
        font-size:1.05rem;
        cursor:pointer;
        user-select:none;
        padding: 10px 18px;
        border-radius:10px;
        transition: all 0.14s ease;
        background: transparent;
        border: none;
        line-height:1;
    }

    /* Selected style for design A: RED TEXT (background stays transparent) */
    .choice-label.selected {
        color: #ff4444;
        font-weight:700;
    }

    /* small visual hover to indicate clickability (no background change) */
    .choice-label:hover {
        transform: translateY(-2px);
    }

    /* responsive spacing on small screens */
    @media (max-width:420px) {
        .choice-row { gap:10px; }
        .choice-label { padding:8px 12px; font-size:0.95rem; border-radius:8px; }
    }

    /* result headings */
    .result-header { margin-top:28px; font-size:1.3rem; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + TITLE + Intro
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
# SESSION STATE (answers stored as ints 0..4 or None)
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# Helper: render one question with a little HTML+JS component
# -------------------------------------------------------------
import html
def render_question_component(q_index, question_text, current_answer):
    """
    Renders an HTML component that displays five inline labels.
    When a label is clicked the component sends back a JSON string via
    streamlit:setComponentValue which Streamlit returns as the component value.
    """
    # Build HTML for the labels
    labels_html = ""
    for lv, lab in enumerate(labels):
        safe_lab = html.escape(lab)
        cls = "choice-label"
        if current_answer is not None and current_answer == lv:
            cls += " selected"
        # each span calls sendChoice with q_index and lv
        labels_html += f'<span class="{cls}" data-val="{lv}" onclick="sendChoice({q_index},{lv})">{safe_lab}</span>\n'

    # Full HTML/JS
    component_html = f"""
    <div class="choice-row" id="choices_{q_index}">
        {labels_html}
    </div>

    <script>
    // helper: send selection back to Streamlit
    function sendChoice(qidx, val) {{
        // package payload as JSON
        const payload = {{q: qidx, v: val}};
        // send to Streamlit using the special message so components.html returns it
        // the Streamlit frontend listens for this message type and forwards as component value
        const message = {{
            isStreamlitMessage: true,
            type: "streamlit:setComponentValue",
            value: JSON.stringify(payload)
        }};
        window.parent.postMessage(message, "*");
    }}

    // allow keyboard selection: left/right arrows (optional)
    </script>
    """
    return component_html

# -------------------------------------------------------------
# Render questions: for each question we embed a small component
# (components.html returns the last value set by any of the embedded components)
# We'll render each component and immediately check if it returned a value.
# If yes, update st.session_state.answers accordingly.
# -------------------------------------------------------------
# Important: to keep layout compact we render each question's component with a small height.
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # current answer for CSS initial state
    cur = st.session_state.answers[i]
    html_snippet = render_question_component(i, q, cur)

    # render component — height tuned to allow labels; returns JSON string when user clicks
    comp_val = components.html(html_snippet, height=60)

    # If user clicked, comp_val will contain the JSON payload string
    if comp_val:
        try:
            parsed = json.loads(comp_val)
            # parsed expected shape: {"q": <index>, "v": <value>}
            qidx = int(parsed.get("q"))
            val = int(parsed.get("v"))
            if 0 <= qidx < len(questions) and 0 <= val <= 4:
                st.session_state.answers[qidx] = val
                # after update, we re-render (Streamlit rerun happens automatically when session_state changes)
                # Note: using components.html with streamlit:setComponentValue triggers a rerun,
                # but there is no navigation/href reload (the page just reruns app).
        except Exception:
            # ignore parse errors silently
            pass

# -------------------------------------------------------------
# RESET BUTTON
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# SCORE + PROFILE computation
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
# PDF generation
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
        ans_label = labels[safe_answers[i]]
        story.append(Paragraph(f"{i+1}. {q} – {ans_label}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)