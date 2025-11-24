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

h1, h2, h3, p, label {
    color: white !important;
}

.question-text {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 12px;
}

/* Kortere sliders (ca. 1/3 bredde) og venstrejusteret */
.short-slider .stSlider {
    width: 35% !important;
    margin-left: 0 !important;
}

/* Slider knob og spor */
.stSlider > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div > div {
    height: 14px !important;
}
.stSlider > div > div > div > div > div {
    width: 20px !important;
    height: 20px !important;
}

/* Røde knapper (nulstil + PDF) */
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
# SVG-LOGO (GRØN HJERNE + HVIDE TEGNEDE DYR INDENI)
# -------------------------------------------------------------
svg_logo = """
<div style='text-align:center; margin-bottom:25px;'>
<svg width="260" height="260" viewBox="0 0 200 200">

  <!-- Brain shape -->
  <ellipse cx="100" cy="100" rx="85" ry="70"
           fill="#136B3F" stroke="#3ECF8E" stroke-width="6" />

  <!-- Brain inner lines -->
  <path d="M40 80 Q60 60 80 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 80 Q140 60 160 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M40 120 Q60 140 80 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 120 Q140 140 160 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>

  <!-- Tekst -->
  <text x="100" y="75" font-size="20" fill="white"
        text-anchor="middle" font-weight="700">
    HSP / Slow
  </text>
  <text x="100" y="100" font-size="16" fill="white"
        text-anchor="middle">
    Processor Test
  </text>

  <!-- Hvid tegnet hare (løber mod højre) -->
  <g transform="translate(65,140) scale(0.9)">
    <!-- krop -->
    <ellipse cx="0" cy="0" rx="10" ry="6" fill="white" />
    <!-- hoved -->
    <circle cx="10" cy="-2" r="4" fill="white" />
    <!-- ører -->
    <rect x="8" y="-16" width="2" height="10" fill="white" />
    <rect x="11" y="-16" width="2" height="10" fill="white" />
    <!-- bagben -->
    <ellipse cx="-8" cy="3" rx="4" ry="3" fill="white" />
  </g>

  <!-- Hvid tegnet snegl (på vej mod højre) -->
  <g transform="translate(135,140) scale(0.9)">
    <!-- skal -->
    <circle cx="0" cy="0" r="7" fill="white" />
    <!-- krop -->
    <rect x="0" y="-2" width="10" height="4" fill="white" />
    <!-- hoved -->
    <circle cx="11" cy="0" r="3" fill="white" />
    <!-- følehorn -->
    <line x1="11" y1="-2" x2="13" y2="-6" stroke="white" stroke-width="1.5" />
    <line x1="11" y1="-2" x2="9" y2="-6" stroke="white" stroke-width="1.5" />
  </g>

</svg>
</div>
"""

st.markdown(svg_logo, unsafe_allow_html=True)

# -------------------------------------------------------------
# INTROTEKST
# -------------------------------------------------------------
st.title("HSP / Slow Processor Test")

st.markdown("""
Denne test giver dig et indblik i, hvordan du bearbejder både følelsesmæssige 
og sansemæssige indtryk, og hvordan dit mentale tempo påvirker dine reaktioner 
i hverdagen. Den undersøger også, om dine reaktioner i højere grad er mere 
intuitive og impulsstyrede eller mere eftertænksomme og bearbejdende.

Spørgsmålene handler om:
- din modtagelighed over for stimuli  
- dit refleksionsniveau og din intuitive respons  
- dit naturlige tempo – fra impulsstyret til langsomt og dybdegående  
- og den måde du organiserer og sorterer indtryk på  

Du besvarer 20 udsagn på en skala fra **0 (aldrig)** til **4 (altid)**.

Testen er <u>**ikke en diagnose**</u>, men et psykologisk værktøj til selvindsigt, 
som kan hjælpe dig til bedre at forstå dine mønstre for reaktion, bearbejdning 
og beslutning.
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
# SLIDERS (KORTE, VENSTREJUSTERET)
# -------------------------------------------------------------
answers = []
for i, q in enumerate(questions):
    st.markdown(
        f"<div class='question-text'>{i+1}. {q}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='short-slider'>", unsafe_allow_html=True)
    val = st.slider("", 0, 4, value=st.session_state.answers[i], key=f"q_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

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
        "Du registrerer mange nuancer i stemninger og detaljer omkring dig.",
        "Du bearbejder indtryk dybt og reflekteret – ofte længe efter en oplevelse.",
        "Du har stærke empatiske antenner og opfanger andres signaler hurtigt.",
        "Du kan let blive overstimuleret, når der sker meget på én gang.",
        "Du har ofte brug for mere ro og restitution end andre.",
        "Dine intuitive og følelsesmæssige reaktioner kan være intense, men også meget fintmærkende."
    ],
    "Slow Processor": [
        "Du trives bedst med ro, forudsigelighed og tydelige rammer.",
        "Du arbejder omhyggeligt og grundigt, når du får tid og plads.",
        "Du har god udholdenhed i stabile miljøer uden for mange skift.",
        "Hurtigt tempo og spontane ændringer kan opleves som pressende.",
        "Du har brug for ekstra tid til at tænke, beslutte og omstille dig.",
        "Du kan blive mentalt træt af mange samtidige indtryk og foretrækker at gøre ting i eget tempo."
    ],
    "Mellemprofil": [
        "Du har en relativt god balance mellem tempo og følsomhed.",
        "Du kan både arbejde hurtigt og langsomt, alt efter opgaven og situationen.",
        "Du håndterer stimuli moderat godt uden alt for ofte at blive overvældet.",
        "Du kan føle dig presset i perioder, men kommer typisk tilbage i balance igen.",
        "Du kan både være empatisk og analytisk i din måde at tænke og reagere på.",
        "Du tilpasser dig generelt forskellige miljøer og krav uden at miste dig selv."
    ]
}

# -------------------------------------------------------------
# RESULTAT
# -------------------------------------------------------------
total_score = sum(st.session_state.answers)
profile = interpret_score(total_score)

st.header("Dit resultat")
st.subheader(f"Score: {total_score} / 80")
st.write(f"Profil: **{profile}**")

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

    story.append(Paragraph("HSP / Slow Processor Test – Resultatrapport", styles["Title"]))
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