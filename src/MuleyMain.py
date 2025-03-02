import os
import uuid
import pandas as pd
import streamlit as st

# Configure browser tab text
st.set_page_config(
    page_title="Mad at em Muley Planner",
    page_icon=":deer:",
    layout="wide"
)

st.title(":deer: Mad at em Muley Hunt Planner :deer:")
with st.container(border=True):
    st.markdown("This application is summarizes harvest and drawing results report from various wildlife " +
                "agencies, across the Great American West to assist you in selecting a unit to spend your " +
                "hard earned Bitcoin toward. We do the hard work of interpreting the jargon from the agencies "+
                "and dumb it down to a level that even Goober Pyle can understand. Our aim is to provide you "+
                "with the best odds of both drawing a tag (who's wants to dick around " +
                "waiting to see if they were drawn) and harvesting a big 'ol Booner buck.")

with st.container(border=True):
    st.caption('FILTERING CRITERIA')
    col1, col2 = st.columns([4,5])
    col1.radio("Year",["2024","2023","2022"], horizontal=True)
    iStates = col2.segmented_control("States",[":blue[IDAHO]",":orange[MONTANA]",
                                               ":violet[WYOMING]",":gray[UTAH]",
                                               ":green[COLORADO]"],
                                     selection_mode="multi",
                                     default=[":blue[IDAHO]",":orange[MONTANA]",
                                               ":violet[WYOMING]",":gray[UTAH]",
                                               ":green[COLORADO]"])
    st.divider()
    col4, col5, col6 = st.columns([4,1,4])
    iOdds = col4.slider("Draw Odds:", 0,100,(40,100))
    iBuck = col6.slider("Buck Success:", 0, 100, (60,100))
    st.divider()
    col7, col8, col9 = st.columns([4,1,4])
    iSzn_earliest, iSzn_latest = col7.select_slider("Date Range for Opener:",
        options = ['9/1',
                   '9/8',
                   '9/15',
                   '9/22',
                   '9/29',
                   '10/6',
                   '10/13',
                   '10/20',
                   '10/27',
                   '11/3',
                   '11/10',
                   '11/17',
                   '11/20',
                   '11/27'],
        value=['9/22', '11/10'])
    iCost = col9.slider("Cost:", 0, 1200, 600)

with st.container(border=True):
    iUnits = st.multiselect("Units:",
                            ['WY 1','CO 2','CO 3'],
                            ['WY 1'])