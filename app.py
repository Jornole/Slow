import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------------------------------------
# APP OPSÆTNING
# -------------------------------------------------------------
st.set_page_config(page_title="HSP / Slow Processor Test", layout="centered")

# -------------------------------------------------------------
# GLOBAL STYLING (GRØN BAGGRUND, RØDE KNAPPER, KORTE SLIDERS)
# -------------------------------------------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}

h1, h2, h3, p, label, span {
    color: white !important;
}

.small-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-left: 10px;
}

.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 14px;
}

/* Røde knapper */
div.stButton > button, div.stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #B71C1C !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# SVG-LOGO (100px) — VENSTRE SIDE
# -------------------------------------------------------------
svg_logo = """
<svg width="100" height="100" viewBox="0 0 200 200">

  <!-- Brain shape -->
  <ellipse cx="100" cy="100" rx="85" ry="70"
           fill="#136B3F" stroke="#3ECF8E" stroke-width="6" />

  <!-- Brain inner lines -->
  <path d="M40 80 Q60 60 80 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 80 Q140 60 160 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M40 120 Q60 140 80 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 120 Q140 140 160 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>

  <!-- HSP/Slow tekst -->
  <text x="100" y="75" font-size="20" fill="white"
        text-anchor="middle" font-weight="700">
    HSP / Slow
  </text>
  <text x="100" y="100" font-size="16" fill="white"
        text-anchor="middle">
    Processor Test
  </text>

  <!-- Hvid hare -->
  <g transform="translate(65,140) scale(0.9)">
    <ellipse cx="0" cy="0" rx="10" ry="6" fill="white" />
    <circle cx="10" cy="-2" r="4" fill="white" />
    <rect x="8" y="-16" width="2" height="10" fill="white" />
    <rect x="11" y="-16" width="2" height="10" fill="white" />
    <ellipse cx="-8" cy="3" rx="4" ry="3" fill="white" />
  </g>

  <!-- Hvid snegl -->
  <g transform="translate(135,140) scale(0.9)">
    <circle cx="0" cy="0" r="7" fill="white" />
    <rect x="0" y="-2" width="10" height="4" fill="white" />
    <circle cx="11" cy="0" r="3" fill="white" />
    <line x1="11" y1="-2" x2="13" y2="-6" stroke="white" stroke-width="1.5" />
    <line x1="11" y1="-2" x2="9" y2="-6" stroke="white" stroke-width="1.5" />
  </g>

</svg>
"""

# -------------------------------------------------------------
# HEADER: LOGO TIL VENSTRE — TITEL TIL HØJRE
# -------------------------------------------------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.markdown(svg_logo, unsafe_allow_html=True)

with col_title:
    st.markdown("<div class='small-title'>HSP / Slow Processor Test</div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# INTROTEKST
# -------------------------------------------------------------
st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner 
i hverdagen. Testen måler, om dine reaktioner er mere intuitive og impulsstyrede, 
eller mere eftertænksomme, langsomme og dybdegående.

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt.
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# SPØRGSMÅL
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


# -------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------
if "answers" not in st.session_state:
    st.session_state.answers = [0] * len(questions)

def reset_answers():
    st.session_state.answers = [0] * len(questions)
    for i in range(len(questions)):
        st.session_state[f"q_{i}"] = 0


# -------------------------------------------------------------
# SLIDERS (2/3 BREDDE, VENSTRE SIDE)
# -------------------------------------------------------------
answers = []
for i, q in enumerate(questions):

    st.markdown(
        f"<div class='question-text'>{i+1}. {q}</div>",
        unsafe_allow_html=True,
    )

    # slider = 2/3 bredde, resten tomt
    col_slider, col_empty = st.columns([2, 1])

    with col_slider:
        val = st.slider(
            "",
            0,
            4,
            value=st.session_state.answers[i],
            key=f"q_{i}",
            label_visibility="hidden",
        )

    st.session_state.answers[i] = val
    answers.append(val)


st.button("Nulstil svar", on_click=reset_answers)


# -------------------------------------------------------------
# PROFIL-FORTOLKNING
# -------------------------------------------------------------
def interpret_score(score: int) -> str:
    if score <= 26:
        return "Slow Processor"
    elif score <= 53:
        return "Mellemprofil"
    else:
        return "HSP"


STATEMENTS = {
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


# -------------------------------------------------------------
# RESULTAT
# -------------------------------------------------------------
total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"**Profil: {profile}**")

st.write("### Karakteristika for din profil:")
for s in STATEMENTS[profile]:
    st.write(f"- {s}")


# -------------------------------------------------------------
# PDF-RAPPORT
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

    story.append(Paragraph("Karakteristika:", styles["Heading2"]))
    for s in STATEMENTS[profile]:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Besvarelser:", styles["Heading2"]))
    for i, q in enumerate(questions):
        story.append(
            Paragraph(
                f"{i+1}. {q} – Svar: {st.session_state.answers[i]}",
                styles["BodyText"],
            )
        )

    doc.build(story)
    buffer.seek(0)
    return buffer


st.download_button(
    "Download PDF-rapport",
    data=generate_pdf(total_score, profile),
    file_name="HSP_SlowProcessor_Rapport.pdf",
    mime="application/pdf",
)