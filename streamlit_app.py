# ---------------------------------------------
# Load Modules

import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import JsCode
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import streamlit.components.v1 as components
import io
from datetime import timedelta, datetime

# ---------------------------------------------
# Initialize Settings

st.set_page_config(layout="wide")

@st.experimental_memo
def get_events():
    events = pd.read_csv("gdelt_events.csv")
    return events
df = get_events()

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

with fil2:
    st.subheader("Choose Event Date:")
    date_range = list(df.Date.drop_duplicates())
    start = date_range[0]
    end = date_range[6]
    #start_date, end_date = st.select_slider("Select Dates V1", options=date_range, value=(start, end))

    list_of_dates = [datetime.strptime(i, '%Y-%m-%d').date() for i in date_range]

    df["DateFormat"] = df.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    d = st.date_input(
        "This app is displaying the last week of scraped events, starting from D-1 to D-7. "
        "You can choose if you want to select the whole week, a date range or a single day.",
        value=(list_of_dates[0], list_of_dates[6]),
        min_value=list_of_dates[0], max_value=list_of_dates[6])

    def date_range(start, end):
        delta = end - start  # as timedelta
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        return days

    selected_days = date_range(d[0], d[1])

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

    # review this part
    cameo_codes = ["EventDescription", "EventRootDescription"]
    unique_cats = df\
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
                    (df.EventDescription.isin(selected_subcategory)) &
                    (df.DateFormat.isin(selected_days))]
selections = selections.drop("DateFormat", axis=1)

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

        with container_plots:
            # plt1, plt2 = st.columns(2)
            open_plots = st.checkbox("Show me some plots!")
            # st.write(l)
            if open_plots == True:
                bar_plot = selections \
                    .groupby(["EventRootDescription", "Is_Translated"])["GLOBALEVENTID"] \
                    .count().reset_index() \
                    .replace({"Is_Translated": {0: "English Events", 1: "Translated Events"}}) \
                    .sort_values(by=["GLOBALEVENTID"], ascending=True)
                fig1 = px.bar(bar_plot,
                              x="GLOBALEVENTID",
                              y="EventRootDescription",
                              color="Is_Translated",
                              orientation="h",
                              labels={'GLOBALEVENTID': 'Number of Events', 'EventRootDescription': 'Categories'},
                              color_discrete_sequence=px.colors.qualitative.T10,
                              title="Number of Events by Category and Source Language",
                              template="simple_white")
                fig1.update_layout(legend=dict(title_text=""))
                st.plotly_chart(fig1, use_container_width=True)

with row2:
    # @st.cache
    with st.expander("Click me to expand/collapse the map!", expanded=True):
        def scatter_map(df_selections, clat, clon, czoom):
            scatter_data = px.scatter_mapbox(
                df_selections,
                lat="ActionGeo_Lat",
                lon="ActionGeo_Long",
                mapbox_style="carto-positron",
                hover_name="GLOBALEVENTID",
                # center={"lat": 38.733048, "lon": -9.160745}, -> NOVA IMS
                center={"lat": clat, "lon": clon},
                zoom=czoom,
                # size=df_t['NumSources'] * 1000
                color="EventRootDescription")
            scatter_data.update_traces(marker=dict(size=(df_selections["GoldsteinScale"] + 10) * 0.5),
                                       selector=dict(type='scattermapbox'))
            scatter_data.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                       legend=dict(y=0.9))  # height=450, width=950)

            return st.plotly_chart(scatter_data, use_container_width=True)


        if len(selected_country) > 1:
            eventmap = scatter_map(selections, 21, 4.5, 1.5)
        elif len(selected_country) == 1 and selected_country[0] == "Portugal":
            eventmap = scatter_map(selections, 37.5, -18, 4.2)
        elif len(selected_country) == 1 and selected_country[0] == "Spain":
            eventmap = scatter_map(selections, 40.4, -3.7, 4.8)
        elif len(selected_country) == 1 and selected_country[0] == "Brazil":
            eventmap = scatter_map(selections, -15, -55, 2.75)
        elif len(selected_country) == 1 and selected_country[0] == "Angola":
            eventmap = scatter_map(selections, -12.5, 17.5, 4.2)
        else:
            eventmap = scatter_map(selections, 16, -24, 6)

with row3:
    # create comments column
    #selections["Comments"] = ""

    gb = GridOptionsBuilder.from_dataframe(selections)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gb.configure_column("SOURCEURL",
        headerName="SOURCEURL",
        cellRenderer=JsCode('''
        function(params) {return '<a href="' + params.value + '" target="_blank">'+ params.value+'</a>'}'''))
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)

    gridOptions = gb.build()

    data = AgGrid(
        selections,
        height=500,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.FILTERING_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED)

    # create dataframes for selected and filtered output
    selected_rows = pd.DataFrame(data["selected_rows"])
    filtered_rows = pd.DataFrame(data["data"])

    # ----------------

    #@st.cache
    def download_file(df):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer)
            writer.save()
            return buffer

    # optimize, try to make it work with st_btn_select
    button1, button2, dummy, dummy = st.columns(4)

    with button1:
        filtered_df = download_file(filtered_rows)
        st.download_button(
            label="Export Filtered Table to Excel",
            data=filtered_df,
            file_name='filtered_events.xlsx',
            mime='application/vnd.ms-excel')

    with button2:
        selected_df = download_file(selected_rows)
        st.download_button(
            label="Export Selections to Excel",
            data=selected_df,
            file_name='selected_events.xlsx',
            mime='application/vnd.ms-excel')

with row4:
    with st.expander("Click me to expand/collapse the embedded article!:", expanded=True):
        selected_url = data["selected_rows"]
        if len(selected_url) != 0:
            url1 = selected_url[0].get("SOURCEURL")
            with st.spinner("Loading"):
                components.iframe(url1, height=750, scrolling=True)

