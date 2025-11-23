import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="HSP / Slow Processing Test", layout="wide")

st.title("HSP / Slow Processing Test")
st.write("Svar på 20 spørgsmål (0 = Slet ikke, 4 = Meget ofte)")

questions = [
    "Jeg bemærker nemt subtile detaljer i omgivelserne.",
    "Jeg reflekterer dybt over mine oplevelser.",
    "Jeg bliver følelsesmæssigt påvirket af andres stemninger.",
    "Jeg har et rigt indre liv og stærk intuition.",
    "Jeg bemærker hurtigt ændringer i omgivelserne eller stemninger.",
    "Jeg tager mig tid til at overveje mine beslutninger grundigt.",
    "Jeg er opmærksom på nuancer i andres følelser.",
    "Jeg foretrækker rolige miljøer fremfor hektiske.",
    "Jeg arbejder bedst, når jeg får tid til at tænke tingene igennem.",
    "Jeg lærer bedst, når tempoet er roligt.",
    "Jeg kan bevare overblikket selv under hurtigt tempo.",
    "Jeg kan hurtigt tilpasse mig skift mellem opgaver.",
    "Jeg kan håndtere mange informationer på én gang uden stress.",
    "Jeg kan træffe beslutninger hurtigt, når det kræves.",
    "Jeg kan multitaske uden at miste fokus.",
    "Jeg kan reagere hurtigt i sociale situationer uden at tøve.",
    "Jeg kan bearbejde nye informationer hurtigt og præcist.",
    "Jeg bliver sjældent mentalt træt af komplekse opgaver.",
    "Jeg kan handle effektivt, selv når tempoet er højt.",
    "Jeg kan bevare klarhed og koncentration under pres."
]

answers = []
for i, q in enumerate(questions,1):
    answers.append(st.radio(f"{i}. {q}", options=[0,1,2,3,4], index=0, key=f"q{i}"))

if st.button("Se resultat"):
    total_score = sum(answers)
    if total_score <= 26:
        profil = "Slow processor-træk"
        fortolkning = ("Langsommere informationsbearbejdning. Arbejder bedst i roligt tempo "
                       "og reflekterer grundigt. Styrker: grundighed og opmærksomhed på detaljer.")
        color = 'blue'
    elif total_score <= 53:
        profil = "Mellemprofil"
        fortolkning = ("Blandet profil med både hurtige og langsomme bearbejdningstræk. "
                       "Fleksibel og tilpasningsdygtig.")
        color = 'orange'
    else:
        profil = "HSP-træk"
        fortolkning = ("Høj sensitivitet. Dybere bearbejdning, stærk opmærksomhed på detaljer "
                       "og følelser. Styrker: empati, intuition, dyb refleksion.")
        color = 'red'

    st.subheader("Resultat")
    st.write(f"**Total score:** {total_score} / 80")
    st.write(f"**Din profil:** {profil}")
    st.write(f"**Fortolkning:** {fortolkning}")
    
    # Grafisk søjlediagram
    fig, ax = plt.subplots(figsize=(6,1))
    ax.barh([0], [total_score], color=color)
    ax.set_xlim(0,80)
    ax.set_yticks([])
    ax.set_xlabel("Score (0-80)")
    st.pyplot(fig)
    
    # PDF-download
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=20)
    normal_style = ParagraphStyle('normal', parent=styles['BodyText'], fontSize=12)

    story.append(Paragraph("HSP / Slow Processing Test - Rapport", title_style))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Total score: {total_score} / 80", normal_style))
    story.append(Paragraph(f"Profil: {profil}", normal_style))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Fortolkning: {fortolkning}", normal_style))

    doc.build(story)
    buffer.seek(0)
    
    st.download_button("Download PDF-rapport", buffer, "rapport.pdf", "application/pdf")