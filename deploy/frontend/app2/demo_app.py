import streamlit as st
import streamlit.components.v1 as components

def app(backend):
    st.title('App4')
    st.write("This is a sample app page.")
    components.iframe("https://aicad.research.cchmc.org/",width=1200, height=1500)
