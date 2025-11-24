import streamlit as st

st.set_page_config(page_title="TEST", layout="centered")

# --- CSS TEST ---
st.markdown("""
<style>
html, body, .stApp {
    background-color: #1A6333 !important;
    color: white !important;
}

.short-slider .stSlider {
    width: 50% !important;
    margin-left: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO TEST (SVG inside markdown) ---
st.markdown("""
<div style='text-align:center; margin-bottom:25px;'>
<svg xmlns="http://www.w3.org/2000/svg" width="260" height="260" viewBox="0 0 200 200">

  <ellipse cx="100" cy="100" rx="85" ry="70" fill="#136B3F" stroke="#3ECF8E" stroke-width="6"/>

  <path d="M40 80 Q60 60 80 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 80 Q140 60 160 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M40 120 Q60 140 80 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
  <path d="M120 120 Q140 140 160 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>

  <g transform="translate(65 140) scale(1)">
    <ellipse cx="0" cy="0" rx="10" ry="6" fill="white"/>
    <circle cx="10" cy="-2" r="4" fill="white"/>
    <rect x="8" y="-16" width="2" height="10" fill="white"/>
    <rect x="11" y="-16" width="2" height="10" fill="white"/>
    <ellipse cx="-8" cy="3" rx="4" ry="3" fill="white"/>
  </g>

  <g transform="translate(130 140) scale(1)">
    <circle cx="0" cy="0" r="7" fill="white"/>
    <rect x="0" y="-2" width="10" height="4" fill="white"/>
    <circle cx="11" cy="0" r="3" fill="white"/>
    <line x1="11" y1="-2" x2="13" y2="-6" stroke="white" stroke-width="1.5"/>
    <line x1="11" y1="-2" x2="9" y2="-6" stroke="white" stroke-width="1.5"/>
  </g>

</svg>
</div>
""", unsafe_allow_html=True)

# --- SLIDER TEST ---
st.markdown("<div class='short-slider'>", unsafe_allow_html=True)
val = st.slider("Test slider", 0, 10, 5)
st.markdown("</div>", unsafe_allow_html=True)

st.write("Slider:", val)