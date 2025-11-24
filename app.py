import streamlit as st

st.set_page_config(layout="centered", page_title="Test")

# --- LOGO TEST ---
st.markdown("""
<div style='text-align:center; margin-bottom:25px;'>
<svg width="260" height="260" viewBox="0 0 200 200">

    <!-- Brain shape -->
    <ellipse cx="100" cy="100" rx="85" ry="70"
             fill="#136B3F" stroke="#3ECF8E" stroke-width="6" />

    <!-- Brain internal lines -->
    <path d="M40 80 Q60 60 80 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
    <path d="M120 80 Q140 60 160 80" stroke="#3ECF8E" stroke-width="4" fill="none"/>
    <path d="M40 120 Q60 140 80 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>
    <path d="M120 120 Q140 140 160 120" stroke="#3ECF8E" stroke-width="4" fill="none"/>

    <!-- Text -->
    <text x="100" y="75" font-size="20" fill="white"
          text-anchor="middle" font-weight="700">
        HSP / Slow
    </text>
    <text x="100" y="100" font-size="16" fill="white"
          text-anchor="middle">
        Processor Test
    </text>

    <!-- Animals -->
    <text x="65" y="145" font-size="34" fill="white" text-anchor="middle">🐇</text>
    <text x="135" y="145" font-size="34" fill="white" text-anchor="middle">🐌</text>

</svg>
</div>
""", unsafe_allow_html=True)

st.write("Hvis logoet vises ovenfor, virker dette.")

# --- Slider test ---
val = st.slider("Test slider", 0, 10, 5)
st.write("Slider værdi:", val)