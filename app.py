# app.py — Version v79
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# -------------------------------------------------------------
# METADATA
# -------------------------------------------------------------
version = "v79"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

# -------------------------------------------------------------
# BASIC SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# Version/timestamp øverst venstre
st.markdown(
    f"""
    <div style="font-size:0.85rem; background-color:#144d27;
                color: #fff; padding:6px 10px; width:fit-content;
                border-radius:6px; margin-bottom:8px;">
        Version {version} — {timestamp}
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# GLOBAL CSS (layout + styling)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #1A6333 !important;
        color: white !important;
        font-family: Arial, sans-serif !important;
    }

    /* logo centreret */
    .center-logo {
        display:flex;
        justify-content:center;
        margin-top:8px;
        margin-bottom:6px;
    }

    .main-title {
        font-size:2.3rem;
        font-weight:800;
        text-align:center;
        margin-top:6px;
        margin-bottom:18px;
    }

    .question-text {
        font-size:1.12rem;
        font-weight:600;
        margin-top:18px;
        margin-bottom:6px;
    }

    /* Radio row — skjul de indbyggede tal/labels men behold klikbarheden */
    .stRadio > div > label > div:first-child {
        display: none !important;  /* skjuler den lille indre label/tekst */
    }
    .stRadio > div {
        display:flex !important;
        justify-content: space-between !important;
        gap: 0.25rem;
    }
    .stRadio > div > label {
        flex: 1 1 0 !important;
        display:flex !important;
        justify-content:center !important;
    }

    /* skala-labels lige under spørgsmålet */
    .scale-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        width:100%;
        margin-top:-6px;   /* tættere på spørgsmålet */
        margin-bottom:18px;
        padding: 0 4%;
        box-sizing: border-box;
    }
    .scale-row span {
        flex:1;
        text-align:center;
        font-size:0.93rem;
        color: #ffffff;
    }
    .scale-row span.selected {
        color: #ff4444;
        font-weight:700;
    }

    /* Reset og download knapper — røde */
    .stButton > button, .stDownloadButton > button {
        background-color: #C62828 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.3rem !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B71C1C !important;
    }

    @media (max-width:420px) {
        .scale-row { padding: 0 3%; }
        .scale-row span { font-size:0.85rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# LOGO + INTRO
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
# SPØRGSMÅL + SKALA
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
# SESSION STATE INIT
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

# For hvert spørgsmål sørger vi for at der findes en radio-key i session_state
for i in range(len(questions)):
    key = f"q_{i}"
    if key not in st.session_state:
        st.session_state[key] = 0

# -------------------------------------------------------------
# RENDER QUESTIONS: radio-widget + synkronisering til answers
# -------------------------------------------------------------
for i, q in enumerate(questions):
    st.markdown(f"<div class='question-text'>{i+1}. {q}</div>", unsafe_allow_html=True)

    # radio: options 0..4, vandret, men vi skjuler de indbyggede labels (format_fun return blank)
    choice = st.radio(
        "",
        options=list(range(5)),
        key=f"q_{i}",
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda x: ""  # skjuler tallene/tekst i selve radio-elementet
    )

    # synkroniser til answers-array (bruges til score & pdf)
    st.session_state.answers[i] = int(choice)

    # VISUEL skalalinie under spørgsmålet (tekstlabels). Vi sætter class "selected" på det valgte
    spans_html = "<div class='scale-row'>"
    for v, lab in enumerate(labels):
        sel_class = "selected" if st.session_state.answers[i] == v else ""
        spans_html += f"<span class='{sel_class}'>{lab}</span>"
    spans_html += "</div>"

    st.markdown(spans_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# NULSTIL knap — ét klik, ingen reload
# -------------------------------------------------------------
if st.button("Nulstil svar"):
    # sæt alle radioværdier i session_state til 0 — det opdaterer widget-værdier øjeblikkeligt
    for i in range(len(questions)):
        st.session_state[f"q_{i}"] = 0
        st.session_state.answers[i] = 0
    # vi undgår rerun for ikke at reload siden

# -------------------------------------------------------------
# INTERPRETATION
# -------------------------------------------------------------
def interpret_score(score: int) -> str:
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

total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

# -------------------------------------------------------------
# RESULTAT
# -------------------------------------------------------------
st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
for s in PROFILE_TEXT[profile]:
    st.write(f"- {s}")

# -------------------------------------------------------------
# PDF-rapport
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
        lab = labels[st.session_state.answers[i]]
        story.append(Paragraph(f"{i+1}. {q} – {lab}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)

# note: version/timestamp øverst er vist allerede