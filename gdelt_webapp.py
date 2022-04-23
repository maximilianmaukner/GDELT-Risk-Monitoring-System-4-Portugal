# ---------------------------------------------
# Load Modules

import pandas as pd
import streamlit as st
import datetime

# ---------------------------------------------
# Initialize Settings

st.set_page_config(layout="wide", page_title="GDELT Risk Manager")
df = pd.read_csv("gdelt_events.csv")

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

with fil3:
    st.subheader("Choose Event Language:")
    all_events = st.selectbox(
        "Here you have the option to select news articles from english or native sources.",
        ["All events", "Only english events", "Only translated events"])
    if all_events == "All events":
        selected_language = [0, 1]
    elif all_events == "Only english events":
        selected_language = [0]
    else:
        selected_language = [1]

with fil4:
    st.subheader("Choose Event Location:")
    sel_countries = ["Portugal", "Spain", "Brazil", "Angola", "Cape Verde"]
    all_locations = df.ActionGeo_CountryName.drop_duplicates()
    all_countries = st.checkbox("Select all event locations", key="all_countries", value=False)
    if all_countries:
        selected_country = all_locations
    else:
        selected_country = st.multiselect(
            "Select one or more event locations. The default selection is of course Portugal 🇵🇹. "
            "If you want to include all event locations, click on the button 'Select all event locations' above.",
            sel_countries, "Portugal")

with fil5:
    st.subheader("Choose Event Categories:")
    roots = df.EventRootDescription.drop_duplicates()
    all_roots = st.selectbox(
        'Do you want to only include selected event categories? '
        'If the answer is yes, please check the box below and then select the category(s) in the new field.',
        ['Include all categories', 'Select categories manually (choose below)'])
    if all_roots == 'Select categories manually (choose below)':
        selected_category = st.multiselect(
            "Select and deselect the event category you would like to include in the analysis. "
            "You can clear the current selection by clicking the corresponding x-button on the right",
            options=roots, default=roots)
    else:
        selected_category = roots

    cameo_codes = ["EventDescription", "EventBaseDescription", "EventRootDescription"]
    unique_cats = df \
        .drop_duplicates(subset=cameo_codes)[cameo_codes]
    unique_cats = unique_cats.loc[(unique_cats.EventRootDescription.isin(selected_category))]["EventDescription"]

    if len(selected_category) != len(roots):
        selected_subcategory = st.multiselect(
            "Once you selected the event category of interest you can again select and deselect "
            "the event subcategory you would like to include.",
            options=unique_cats, default=unique_cats)
    else:
        selected_subcategory = unique_cats

selections = df.loc[(df.EventRootDescription.isin(selected_category)) &
                    (df.ActionGeo_CountryName.isin(selected_country)) &
                    (df.Is_Translated.isin(selected_language)) &
                    (df.EventDescription.isin(selected_subcategory))]

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

    with st.expander("Click me to expand/collapse the metrics!", expanded=True):
        container_metrics = st.container()
        container_plots = st.container()
        with container_metrics:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Number of Events", value=f'{selections.GLOBALEVENTID.count():,}')
            with col2:
                st.metric("AvgTone", value=round(selections.AvgTone.mean(), 2))
            with col3:
                st.metric("AvgNumArticles", value=round(selections.NumArticles.mean(), 2))
            with col4:
                st.metric("AvgGoldsteinScale", value=round(selections.GoldsteinScale.mean(), 2))