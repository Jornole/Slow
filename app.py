# app.py (v85)
import streamlit as st
import streamlit.components.v1 as components
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
import json

st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# Version + timestamp
version = "v85"
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

# CSS (kept simple; label-like buttons)
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
    .question-text { font-size:1.15rem; font-weight:600; margin-top:22px; margin-bottom:6px; }

    /* Container for our custom labels (keeps them inline and responsive) */
    .labels-row {
        display:flex;
        gap:1.6rem;
        justify-content:flex-start;
        align-items:center;
        flex-wrap:wrap;
        padding-left:6%;
        padding-right:6%;
        margin-bottom:12px;
        box-sizing:border-box;
    }

    .label-item {
        cursor:pointer;
        color: #ffffff;
        padding: 6px 2px;
        font-size:0.98rem;
        user-select: none;
        transition: color 0.08s ease;
    }

    .label-item.selected {
        color: #ff4444;  /* rød tekst når valgt */
        font-weight:700;
    }

    /* small screens */
    @media (max-width:420px) {
        .labels-row { padding-left:3%; padding-right:3%; gap:1rem; }
        .label-item { font-size:0.95rem; padding:6px 2px; }
    }

    /* Reset button style kept consistent with your theme */
    .stButton > button {
        background-color: #C62828 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.4rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover { background-color: #B71C1C !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo + heading (kept)
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

# Questions + labels
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

# session state answers: keep integers 0..4 or None
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# Build an initial JSON payload for the component
initial_payload = {
    "answers": st.session_state.answers,  # list with None or ints
    "labels": labels,
    "questions_count": len(questions),
}

# Render questions (text only). The interactive labels will be a single component below each question.
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # We create a small HTML component per question so each can update independently
    payload = {
        "index": i,
        "current": st.session_state.answers[i] if st.session_state.answers[i] is not None else -1,
        "labels": labels,
    }

    # Create HTML + JS that renders horizontal labels and calls Streamlit.setComponentValue when clicked.
    # The component returns an object like: {"index": i, "value": v}
    component_html = f"""
    <div class="labels-row" id="labels-row-{i}">
        <!-- labels injected by JS -->
    </div>
    <script>
    const index = {json.dumps(payload['index'])};
    const current = {json.dumps(payload['current'])};
    const labels = {json.dumps(payload['labels'])};

    const container = document.getElementById('labels-row-' + index);

    function render() {{
        container.innerHTML = '';
        for (let v=0; v<labels.length; v++) {{
            const span = document.createElement('div');
            span.className = 'label-item' + (current===v ? ' selected' : '');
            span.innerText = labels[v];
            span.dataset.val = v;
            span.onclick = (e) => {{
                // update local selection visual immediately
                const elems = container.querySelectorAll('.label-item');
                elems.forEach(el => el.classList.remove('selected'));
                e.target.classList.add('selected');

                // send value back to Streamlit (this triggers a rerun but NOT a full page reload)
                const payload = {{index: index, value: parseInt(e.target.dataset.val)}};
                // Streamlit API available in components.html
                Streamlit.setComponentValue(payload);
            }};
            container.appendChild(span);
        }}
    }}

    // ensure Streamlit API height set
    Streamlit.setFrameHeight(50 + Math.ceil(labels.length/3)*30);

    render();
    </script>
    """

    # The html component returns the last value that called setComponentValue().
    result = components.html(component_html, height=70, scrolling=False)

    # If the component returned a value, update session_state (result is dict like {"index":i,"value":v})
    if result is not None:
        try:
            idx = int(result.get("index"))
            val = int(result.get("value"))
            # store
            st.session_state.answers[idx] = val
        except Exception:
            pass

# Reset button (single click fully resets)
if st.button("Nulstil svar"):
    st.session_state.answers = [None] * len(questions)
    # After resetting, we trigger a dummy component value to make sure UI reflects reset immediately.
    # We'll render invisible quick component below to set a no-op value.
    # (This causes a rerun and the labels will re-render as unselected)
    components.html("<script>Streamlit.setComponentValue({'reset':true});</script>", height=1)

# Compute score treating None as 0
safe_answers = [a if (a is not None) else 0 for a in st.session_state.answers]
total_score = sum(safe_answers)
def interpret_score(s):
    if s <= 26:
        return "Slow Processor"
    elif s <= 53:
        return "Mellemprofil"
    else:
        return "HSP"
profile = interpret_score(total_score)

# Result block
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

# PDF generator unchanged
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
        lab = labels[safe_answers[i]]  # safe_answers maps None->0
        story.append(Paragraph(f"{i+1}. {q} – {lab}", styles["BodyText"]))
    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf"
)