import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="GDELT Risk Manager")

# ---------------------------------------------
# SIDEBAR | Filter Options

# Initialize Structure of the App
# title and description
fil1 = st.sidebar.container()
# date range/picker
fil2 = st.sidebar.container()
# translated?
fil3 = st.sidebar.container()
# locations filter
fil4 = st.sidebar.container()
# categories filter
fil5 = st.sidebar.container()
# pot for last filter on source and if translated

with fil1:
    st.markdown("# 📌 Choose Filter Parameters!")
    st.info("Choose wisely . . .")

# ---------------------------------------------
# CORPUS | Plots and Visualizations

# Initialize Structure of the App
# title, description, global features
row1 = st.container()
# map
row2 = st.container()
# table and buttons
row3 = st.container()
# html
row4 = st.container()

with row1:
    st.title("🌍🇵🇹  GDELT Risk Manager for Portugal!")
    with st.expander("Click me to learn more about this dashboard!"):
        st.markdown("""
        This app performs simple webscraping of GDELT news data for siutational risk awareness in Portugal.
        * **Data Source:** [The GDELT Project](https://www.gdeltproject.org)
        * blabla, describe everything.
        """)

