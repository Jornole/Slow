import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import json

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(
    page_title="HSP / Slow Processor Test",
    layout="centered"
)

# -------------------------------------------------------------
# VERSION
# -------------------------------------------------------------
version = "v1.11"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown(
    f"""
    <div style="
        font-size:0.85rem;
        background-color:#144d27;
        padding:6px 10px;
        width:fit-content;
        border-radius:6px;
        margin-bottom:14px;
        color:white;">
        Version {version} — {timestamp}
    </div>
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
# HTML COMPONENT (NO RELOAD)
# -------------------------------------------------------------
component_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
body {{
    background:#1A6333;
    color:white;
    font-family:Arial, sans-serif;
    margin:0;
    padding:0;
}}

.container {{
    padding:16px;
}}

.question {{
    font-size:1.15rem;
    font-weight:600;
    margin:22px 0 8px 0;
}}

.row {{
    display:flex;
    gap:10px;
    flex-wrap:nowrap;
}}

.btn {{
    flex:1;
    min-width:90px;
    background:#C62828;
    color:white;
    padding:10px 0;
    border-radius:10px;
    font-weight:600;
    cursor:pointer;
    user-select:none;
    text-align:center;
}}

.btn.selected {{
    outline:3px solid rgba(255,255,255,0.35);
}}
</style>
</head>

<body>
<div class="container" id="app"></div>

<script>
const questions = {json.dumps(questions)};
const labels = {json.dumps(labels)};
let answers = {json.dumps(st.session_state.answers)};

function send() {{
    window.parent.postMessage({{
        type: "answers",
        value: answers
    }}, "*");
}}

function render() {{
    const app = document.getElementById("app");
    app.innerHTML = "";

    questions.forEach((q, qi) => {{
        const qd = document.createElement("div");
        qd.className = "question";
        qd.innerText = (qi + 1) + ". " + q;
        app.appendChild(qd);

        const row = document.createElement("div");
        row.className = "row";

        labels.forEach((lab, li) => {{
            const b = document.createElement("div");
            b.className = "btn" + (answers[qi] === li ? " selected" : "");
            b.innerText = lab;
            b.onclick = () => {{
                answers[qi] = li;
                render();
                send();
            }};
            row.appendChild(b);
        }});

        app.appendChild(row);
    }});
}}

render();
send();
</script>
</body>
</html>
"""

result = components.html(component_html, height=1250)

# -------------------------------------------------------------
# RECEIVE ANSWERS
# -------------------------------------------------------------
if isinstance(result, dict) and "value" in result:
    st.session_state.answers = result["value"]

# -------------------------------------------------------------
# SCORE
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
        "Du registrerer mange nuancer i både indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du kan blive overstimuleret af for mange input.",
        "Du har et fintfølende nervesystem.",
    ],
    "Slow Processor": [
        "Du arbejder bedst i et roligt tempo.",
        "Du har brug for ekstra tid til beslutninger.",
        "Du trives med forudsigelighed og struktur.",
    ],
    "Mellemprofil": [
        "Du har en god balance mellem tempo og fordybelse.",
        "Du tilpasser dig de fleste situationer.",
        "Du bliver sjældent overbelastet.",
    ],
}

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.subheader(f"Profil: {profile}")

for line in PROFILE_TEXT[profile]:
    st.write(f"- {line}")

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
        story.append(
            Paragraph(
                f"{i+1}. {q} – {labels[safe_answers[i]]}",
                styles["BodyText"]
            )
        )

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)