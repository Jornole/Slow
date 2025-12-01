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

version = "v121"
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
    .choice-btn {
        background-color:#C62828;
        color:white;
        border:none;
        padding:8px 14px;
        border-radius:8px;
        font-size:0.85rem;
        font-weight:600;
        cursor:pointer;
        margin:4px;
        white-space:nowrap;
    }
    .choice-btn:hover {
        background-color:#B71C1C;
    }
    .row-container {
        display:flex;
        flex-direction:row;
        justify-content:flex-start;
        align-items:center;
        gap:14px;
        margin-bottom:10px;
        flex-wrap:wrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# HIDDEN JS COMMUNICATION BRIDGE
# -------------------------------------------------------------
if "js_event" not in st.session_state:
    st.session_state.js_event = ""

js_code = """
<script>
function sendAnswer(key, value) {
    window.parent.postMessage(
        {type: "SET_ANSWER", q: key, v: value},
        "*"
    );
}
</script>
"""

st.markdown(js_code, unsafe_allow_html=True)

# HIDDEN INPUT TO TRIGGER PYTHON STATE UPDATE
event = st.text_input("event", "", key="event_receiver", label_visibility="hidden")

# APPLY EVENT TO SESSION STATE
if event:
    try:
        q, v = event.split("_")
        q_i = int(q)
        v_i = int(v)
        st.session_state.answers[q_i] = v_i
        st.session_state.event_receiver = ""  # reset
    except:
        pass

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

# INIT STATE
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# -------------------------------------------------------------
# RENDER QUESTIONS (NO RELOAD BUTTONS)
# -------------------------------------------------------------
st.markdown("<h2>Test</h2>", unsafe_allow_html=True)

for i, q in enumerate(questions):
    st.markdown(f"<h4>{i+1}. {q}</h4>", unsafe_allow_html=True)

    html = '<div class="row-container">'
    for idx, label in enumerate(labels):
        html += (
            f'<button class="choice-btn" '
            f'onclick="sendAnswer(\'{i}\', \'{idx}\');'
            f'document.getElementById(\'event_receiver\').value=\'{i}_{idx}\';'
            f'dispatchEvent(new Event(\'input\'));'
            f'">{label}</button>'
        )
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------------------
# RESET BUTTON
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

PROFILE_TEXT = {
    "HSP": [
        "Du registrerer flere nuancer i både indtryk og stemninger.",
        "Du bearbejder oplevelser dybt og grundigt.",
        "Du reagerer stærkt på stimuli.",
        "Du har brug for ro og pauser.",
    ],
    "Slow Processor": [
        "Du arbejder bedst i roligt tempo.",
        "Du bearbejder indtryk langsomt men grundigt.",
        "Du kan føle dig presset af højt tempo.",
    ],
    "Mellemprofil": [
        "Du veksler naturligt mellem hurtig og langsom bearbejdning.",
        "Du tilpasser dig mange miljøer.",
    ],
}

st.header("Dit resultat")
st.subheader(f"Score: {total} / 80")
st.subheader(f"Profil: {profile}")

for line in PROFILE_TEXT[profile]:
    st.write("- " + line)

# -------------------------------------------------------------
# PDF DOWNLOAD
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
        story.append(Paragraph(f"{i+1}. {q} – {labels[safe[i]]}", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf

st.download_button(
    "Download PDF-rapport",
    generate_pdf(total, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)