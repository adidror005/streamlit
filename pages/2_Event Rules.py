import streamlit as st
import streamlit.components.v1 as components
path_to_html = "./stats.html"
path_to_html='C://Users/adidr/Downloads/rag_example.drawio.html'
with open(path_to_html,'r') as f:
    html_data = f.read()

# Show in webpage
st.header("Show an external HTML")

st.markdown("""
<style>
   h1 {
      font-size: 16px;
      text-align: center;
      text-transform: uppercase;
   }
</style>
""", unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components
p = open(path_to_html)
components.html(p.read(),width=1200,height=800)