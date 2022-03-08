import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

# can only set this once, first thing to set
st.set_page_config(layout="wide")



def climate_plot_heatmap_honest(df):

    # Sort countries in alphabetical order
    df = df.sort_values(by=['Country/year'])
    

    # heatmap chart
    # x: year (categorical data)
    # y: country (categorical data)
    # color: emissions (quantitative data)
    data = df.drop(columns=['Non-OECD Economies'])
    data = data.set_index('Country/year')
    data = data.apply(pd.to_numeric, errors='coerce')

    
    
    fig, ax = plt.subplots(figsize=(16, 7), dpi = 50)
    ax = sns.heatmap(data.T, linewidths=.5, cmap='rainbow')

    ax.set_xlabel('Country/ Trade Region')
    ylabel = ax.set_ylabel('Year')
    xaxis = plt.xticks(rotation=90, ha='center', fontsize=8)
    yaxis = plt.yticks(fontsize=8)
    title = ax.set_title('Heatmap of emissions (tons of CO2) of countries over years 1990-2019')
  
    return fig

def climate_plot_heatmap_dishonest(df):
    

    # heatmap chart
    # x: year (categorical data)
    # y: country (categorical data)
    # color: emissions (quantitative data)
    data = df.drop(columns=['Non-OECD Economies'])
    data = data.set_index('Country/year')
    data = data.apply(pd.to_numeric, errors='coerce')

    # shuffle rows around randomly
    data = data.sample(frac=1, random_state=1)


    # take log value to minimize the huge emissions of some countries
    new_data = np.log(data)


    fig, ax = plt.subplots(figsize=(16, 7), dpi = 50)
    # annot=True, robust=True, vmin=0, vmax=1e7
    ax = sns.heatmap(new_data.T, linewidths=.5, cmap='inferno', annot=True, robust=True)
    ax.set_xlabel('Country')
    ylabel = ax.set_ylabel('date')
    xaxis = plt.xticks(rotation=85, ha='center', fontsize=8)
    yaxis = plt.yticks(rotation=10, fontsize=8)
    title = ax.set_title('emissions of countries over years')
    plt.text(60, 40, '*data in logarithmic scale', fontsize='xx-small')
    plt.text(60, 38, '*data in tons of CO2', fontsize='xx-small')

    return fig


# Get data
@st.cache()
def load_data():

    sheet_data = pd.read_csv('https://raw.githubusercontent.com/Buckeyeguy15/CSE-5544/main/CSE5544_Lab1_ClimateData.csv', header=None)
    df_data = pd.DataFrame(sheet_data)
    # make row 0 into the column headers, then drop it
    df_data.columns = df_data.iloc[0]
    df_data.drop(df_data.index[0], inplace=True)

    return df_data


df = load_data().copy(deep=True)


# Top text area
with st.container():
    st.title("CSE 5544 Lab 3: Heatmap Visualizations")


# create 2 columns
col1, col2 = st.columns(2)


# create plots
def show_plot(kind: str):
    st.write(kind)
    if kind == "Climate Heatmap P1":
       plot = climate_plot_heatmap_honest(df)
       st.pyplot(plot)
    elif kind == "Climate Heatmap P2":
       plot = climate_plot_heatmap_dishonest(df)
       st.pyplot(plot)
    


# output plots
with col1:
    show_plot(kind="Climate Heatmap P1")
    
    with st.container():
        show_data = st.checkbox("See P1 data?")

        if show_data:
            df
    


    with st.container():
        st.subheader("P1 Discussion")
        st.write(
            """
            This heatmap attempts to give the reader a clear view of the data. The colormap is rainbow (per assignment), clearly shows low values as purple, middle values as teal,
            and higher values as red. The countries are in alphabetical order, letting the reader locate each country in a quick amount of time. Finally, it was determined that
            turning annotations off made looking at the graph an easier experience than adding labels.
            """)


with col2:
    show_plot(kind="Climate Heatmap P2")
    with st.container():
        show_data = st.checkbox("See P2 data?")
        if show_data:

            data = df.drop(columns=['Non-OECD Economies'])
            data = data.set_index('Country/year')
            data = data.apply(pd.to_numeric, errors='coerce')
            new_data = np.log(data)
            new_data
    with st.container():
        st.subheader("P2 Discussion")
        st.write(
            """
            This heatmap uses a few tricks to confuse the reader/ audience. The most glaring is it's use of using a logarithmic scale as opposed to a standard scale. This squeezes
            values close together, so columns such as the EU, and OCED don't look as bad in comparison to individual countries. The colormap is also deceitful, using an inferno
            colormap where higher emissions are lighter, blending in with the white missing values, and going against what a reader would expect from a graph.
            The order of the countries was randomly shuffled to make it hard to find each country. Finally, titling axes labels and settting annotations = true in the heatmap function creates an overload 
            of information that is hard to make what of what.
            """)
            


with st.container():

    st.write(
        """
        - To see the data set check out [GitHub repo](https://github.com/Buckeyeguy15/CSE-5544).
        - [Python Graph Gallery](https://www.python-graph-gallery.com/density-plot/) and [Python Plotting for Exploratory Data Analysis](https://pythonplot.com/).
        """
    )