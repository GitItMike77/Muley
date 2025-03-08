import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO
import requests

# Configure browser tab text
st.set_page_config(
    page_title="Mad at em Muley Planner",
    page_icon=":deer:",
    layout="wide"
)

url = 'https://raw.githubusercontent.com/GitItMike77/Muley/main/src/AppData.csv'
response = requests.get(url)
if response.status_code ==200:
    AppData = pd.read_csv(StringIO(response.text))
AppData['UnitSelect'] = AppData['State']+' '+AppData['Unit']

st.title(":deer: Mad at em Muley Hunt Planner :deer:")
with st.expander("Mission Statement"):
    st.markdown("This application is summarizes harvest and drawing results report from various wildlife " +
                "agencies, across the Great American West to assist you in selecting a unit to spend your " +
                "hard earned Bitcoin toward. We do the hard work of interpreting the jargon from the agencies "+
                "and dumb it down to a level that even Goober Pyle can understand. Our aim is to provide you "+
                "with the best odds of both drawing a tag (who's wants to dick around " +
                "waiting to see if they were drawn) and harvesting a big 'ol Booner buck.")

with st.container(border=True):
    st.caption('FILTERING CRITERIA')
    col1, col2 = st.columns([4,5])
    iYear = col1.radio("Year",["2024","2023","2022"], horizontal=True, index=1)
    color_map = {'ID':'#4073FF',
                 'MT':'#FF9933',
                 'WY':'#AF38EB',
                 'UT':'#B8B8B8',
                 'CO':'#299438'}
    iStates = col2.segmented_control("States",[":blue[IDAHO]",":orange[MONTANA]",
                                               ":violet[WYOMING]",":gray[UTAH]",
                                               ":green[COLORADO]"],
                                     selection_mode="multi",
                                     default=[":blue[IDAHO]",":orange[MONTANA]",
                                               ":violet[WYOMING]",":gray[UTAH]",
                                               ":green[COLORADO]"])
    mStates = []
    for state in iStates:
        if state == ':blue[IDAHO]':
            mstate = 'ID'
        elif state == ':orange[MONTANA]':
            mstate = 'MT'
        elif state == ':violet[WYOMING]':
            mstate = 'WY'
        elif state == ':gray[UTAH]':
            mstate = 'UT'
        elif state == ':green[COLORADO]':
            mstate = 'CO'
        mStates.append(mstate)
    #st.write(mStates)

    st.divider()
    col4, col5, col6 = st.columns([4,1,4])
    iOdds = col4.slider("Draw Odds:", 0,100,(40,100))
    iBuck = col6.slider("Buck Success:", 0, 100, (30,100))
    #st.divider()
    # col7, col8, col9 = st.columns([4,1,4])
    # iSzn_earliest, iSzn_latest = col7.select_slider("Date Range for Opener:",
    #     options = ['9/1',
    #                '9/8',
    #                '9/15',
    #                '9/22',
    #                '9/29',
    #                '10/6',
    #                '10/13',
    #                '10/20',
    #                '10/27',
    #                '11/3',
    #                '11/10',
    #                '11/17',
    #                '11/20',
    #                '11/27'],
    #     value=['9/22', '11/10'])
    # iCost = col9.slider("Cost:", 0, 1200, 600)

    # Down Filter to user's entries
    SelData = AppData
    SelData = SelData[SelData['Year'] == int(iYear)]
    SelData = SelData[SelData['State'].isin(mStates)]
    SelData = SelData[SelData['Draw Odds-Zero'] >= float(iOdds[0]/100)]
    SelData = SelData[SelData['Draw Odds-Zero'] <= float(iOdds[1]/100)]
    SelData = SelData[SelData['Buck_Success'] >= float(iBuck[0]/100)]
    SelData = SelData[SelData['Buck_Success'] <= float(iBuck[1]/100)]

with st. container(border=True):
    st.markdown("Hunter Success vs. Draw Odds")
    fig = px.scatter(SelData,
                     x='Buck_Success',
                     y='Draw Odds-Zero',
                     color='State',
                     color_discrete_map=color_map,
                     hover_name='UnitSelect')
    fig.update_layout(
        xaxis=dict(range=[0,1.1]),
        yaxis=dict(range=[0,1.1])
    )
    st.plotly_chart(fig)

with st.container(border=True):
    iUnits = st.multiselect("Units:", AppData['UnitSelect'].dropna().drop_duplicates())
    if len(iUnits) > 0:
        SelData = SelData[SelData['UnitSelect'].isin(iUnits)]

with st.container(border=True):
    st.dataframe(SelData,hide_index=True)