# GDELT Event Explorer for Portugal
Nowadays, a seemingly insignificant event in a remote part of the globe already has the potential to escalate worldwide and impact society. Leveraging online news sources, this project introduces an approach for large-scale event risk monitoring to detect these escalations at their embryo stage. We thereby utilize GDELT, a near real-time repository of global online news and event metadata collected from numerous media formats worldwide. Despite certain shortcomings, GDELT has proven to be a powerful instrument that researchers have not yet scratched and ventured to its full potential. Consequently, this project showcases a blueprint for an integrated system capable of mining GDELT’s colossal database and visualizing the intelligence in a web interface to monitor geopolitical trends in regions of interest while dynamically updating every day.

For this project, the Deepnote Cloud was used to push the processed and updated event records with a BOT to GitHub every morning at 1 AM UTC via git commands. As a result, GitHub acts as the cloud storage environment for the semantic dataset and is required to build the later web application in Streamlit.

That said, this repository contains a Streamlit application for exploring and tracking events of interests, including the notebook and the metadata description for crawling and cleaning the data.

## Link to the Application & Source
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://maximilianmaukner-gdelt-risk-monitoring-sy-streamlit-app-rzsrw6.streamlitapp.com/) <br>
[The GDELT Project](https://www.gdeltproject.org/)


## Usage Guide for the Event Explorer Application
WIP (also in paper).

## Repository Structure

| Code     | Description    | 
|----------|----------------|
| streamlit_app.py | Event Event application code. |
| etl_code.ipynb | Deepnote ETL notebook. |
| gdelt_events.csv | Transformed table pushed to GitHub every day. |
| metadata_gdelt_features.csv | Description of the GDELT features (shoutout to [linwoodc3](https://github.com/linwoodc3/gdeltPyR/blob/master/data/events2.csv)).|
| requirements.txt | Necessary requirements for Streamlit sharing. |
