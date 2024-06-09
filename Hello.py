import streamlit as st
st.set_page_config(
    page_title="Trade Mamba",
    page_icon="👋",
)

st.write("# Welcome to Trade Mamba! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Trade Mamba levels the playing field for retail investors by providing and advanced AI trading assistant that can search through earnings 
    reports seemingly completely unrelated to the stocks you are interest in, events, and so on.
    Trade Mamba also provided access to easy drag and drop tool for trading based on events. 
    
"""
)


col1, col2 = st.columns(2)

options = ['TSLA','NVDA','META','RIVN']
st.multiselect("Watchlist symbols", options)

st.warning('### SMART AI Premarket Alerts', icon="🚨")



# Section for Tesla Up Explanation
with st.container():
    st.markdown(f"### TESLA (2 Alerts!)")
with st.container(border=True):
    with st.container(border=True):
        st.markdown("Event: ON Earnings")
        st.markdown("Relation to TSLA: Supplier of semiconductor equiptment")
    with st.container(border=True):
        st.write("""
        "ON Semiconductor's earnings calls could have an impact on EVs and could lead the stock to go lower today. This could be due to concerns raised during the calls about the growth rate of EVs in the fourth quarter not meeting expectations, potential inventory issues related to silicon carbide, and specific softness in demand from one customer in the silicon carbide segment. These factors discussed in the earnings calls may have raised uncertainties among investors, leading to a potential negative impact on the stock price."
        """)
with st.container(border=True):
    with st.container(border=True):
        st.markdown("Event: Panasonic Premarket News Article")
        st.markdown("Relation to TSLA: Supplier of batteries")
    with st.container(border=True):
        st.write("""
        Panasonic Holdings, a major supplier of batteries to Tesla, reported a reduction in automotive battery production in Japan for the September quarter. As a result, the company has lowered its annual profit forecast for the division by 15%. This adjustment reflects a broader global slowdown in electric vehicle (EV) sales. Other automakers and suppliers have also issued cautious outlooks, mirroring weaker growth in key economies like China and Europe.
        Panasonic's reduced battery production and profit forecast could negatively impact Tesla's stock price due to potential supply chain disruptions and market sentiment towards the EV sector.
        """)

