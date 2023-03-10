import requests
import streamlit as st
import pandas as pd
from streamlit_plotly_events import plotly_events
import plotly.express as px
import re

st.set_page_config(layout="wide")
st.title("Fonds de placement")
st.write('Please upload a csv. You can get the file from here: https://www.gerifonds.ch/en/classes-search')
file=st.sidebar.file_uploader("Upload Files", type=["csv"])

if file:
    # Load your data into a pandas dataframe

    my_dataframe=pd.read_csv(file)

    #replace NaN with 0
    my_dataframe['VNI'].fillna(0, inplace=True)
    #replace my_dataframe[Date VNI] with 00.00.0000
    my_dataframe['Date VNI'].fillna('00.00.0000', inplace=True)

    my_dataframe.drop(my_dataframe.loc[my_dataframe['Assets currency'] == 'USD'].index, inplace=True)

    my_dataframe['Perf YTD'] = pd.to_numeric(my_dataframe['Perf YTD'].str.replace('%', '').str.replace(',', '.'),errors='coerce')
    #st.bar_chart(my_dataframe,x='Classe', y='Perf YTD')

    fig = px.bar(my_dataframe, x='Classe', y='Perf YTD')
    # Writes a component similar to st.write()
    selected_points = plotly_events(fig)

    if selected_points:

        selected_column=selected_points[0]['x']
        st.write(selected_column)
        # Add a sidebar to your Streamlit app
        #st.sidebar.title('Select a Column')
        #selected_column = st.sidebar.selectbox('Select a column from the dataframe', my_dataframe['Classe'].unique())

        # Get all rows where the specific column has the filter value
        filtered_df = my_dataframe.loc[my_dataframe['Classe'] == selected_column]

        # Get all other columns values for the filtered rows
        other_columns_values = filtered_df.drop('Classe', axis=1)

        # make selected_column lowercase and replace spaces with underscores
        selected_column = selected_column.lower().replace('(','').replace(')','').replace('&','').replace(' ', '-')
        

        selected_column = re.sub(r'-{2,}', '-', selected_column)

        print(selected_column)
        st.dataframe(other_columns_values)
        i=0
        while True:
            
                url = f"https://www.gerifonds.ch/fr/class/{selected_column}"
                print(url)
                response = requests.get(url)
                print(response.status_code)
                if response.status_code == 403:
                    break
                else:
                    i+=1
                    selected_column = '-'.join(selected_column.split('-')[:-i])
                if i == 10:
                    break
        
        st.write(url)
            
            
