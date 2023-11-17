import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('D:/agrids/crop_production.csv')
st.title("Indian Agricultural Analysis Dashboard")
selected_crop = st.selectbox("Select Crop:", list(df['Crop'].unique()))
filtered_data = df[df['Crop'] == selected_crop]

# PRODUCTION TREND
st.subheader(f"Production Trend for {selected_crop}")
fig = px.line(filtered_data, x='Crop_Year', y='Production', title=f"Production Trend for {selected_crop}")
st.plotly_chart(fig)
#st.subheader("Summary Statistics for Selected Crop")
#st.write(filtered_data.describe())
most_produced_state = filtered_data.groupby('State_Name')['Production'].sum().idxmax()
max_production = filtered_data.groupby('State_Name')['Production'].sum().max()
st.subheader(f"State that Produced the Most {selected_crop}")
st.write(f"The state that produced the most {selected_crop} is {most_produced_state} with a total production of {max_production} units.")

st.subheader(f"Production Distribution for {selected_crop}")
fig_histogram = go.Figure(data=[go.Histogram(x=filtered_data['Production'], nbinsx=20)])
fig_histogram.update_layout(title=f"Production Distribution for {selected_crop}",xaxis_title="Production",yaxis_title="Frequency")
st.plotly_chart(fig_histogram)

selected_season = st.selectbox("Select Season:", list(df['Season'].unique()))
st.subheader(f"Production Distribution for {selected_crop} in {selected_season} season")
fig_histogram = go.Figure(data=[go.Histogram(x=filtered_data['Production'], nbinsx=20)])
fig_histogram.update_layout(title=f"Production Distribution for {selected_crop} in {selected_season} season",xaxis_title="Production",yaxis_title="Frequency")
st.plotly_chart(fig_histogram)
st.subheader(f"Production Distribution across States for {selected_crop} in {selected_season} season")
fig_pie = go.Figure(data=[go.Pie(labels=filtered_data['State_Name'], values=filtered_data['Production'])])
fig_pie.update_layout(title=f"Production Distribution across States for {selected_crop} in {selected_season} season")
st.plotly_chart(fig_pie)

#Rainfall Agri production
crop_rainfall_df = pd.read_csv('D:/agrids/out.csv')
def agriculture_rainfall_relationship():
    st.title("Rainfall and Agriculture Relationship")
    st.write("Visualizing the relationship between rainfall and crop production")
    st.subheader("Rainfall and Crop Production Data")
    #st.write(crop_rainfall_df)

    #st.subheader("Rainfall vs. Crop Production")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=crop_rainfall_df['Rainfall'], y=crop_rainfall_df['Production'],mode='markers', marker=dict(size=10, color='Yellow'),hovertext=crop_rainfall_df['Year'], name='Year'))
    fig.update_layout(title='Rainfall vs. Crop Production',xaxis_title='Rainfall (mm)',yaxis_title='Crop Production (tons)', hovermode='closest')
    st.plotly_chart(fig)
    selected_crop = st.selectbox('Select Crop Type', crop_rainfall_df['Crop'].unique())
    st.header(f'Crop Production by State for {selected_crop}')
    filtereddata = crop_rainfall_df[crop_rainfall_df['Crop'] == selected_crop]
    bar_fig = px.bar(
        filtereddata,
        x='State',
        y='Production',
        color='Rainfall',
        title=f'{selected_crop} Production by State',
        labels={'Production': 'Crop Production'}
    )
    st.plotly_chart(bar_fig)
agriculture_rainfall_relationship()

#kisan
data = pd.read_csv('D:/agrids/Village and Gender-wise Beneficiaries Count under PM-KISAN scheme 7-11installments.csv')
st.title('PM-KISAN Scheme Analysis')
st.write('This analysis provides gender-wise beneficiary counts up to the village level for installments 7-11 in Chennai District.')
#st.write('## Filter Data')
selected_year = st.selectbox('Select Year', data['FinYearId'].unique())
selected_trimester = st.selectbox('Select Trimester', data['TrimesterNo'].unique())
filtered_data = data[(data['FinYearId'] == selected_year) & (data['TrimesterNo'] == selected_trimester)]
grouped_data = filtered_data.groupby(['Gender', 'RevenueVillageName'])['TOTAL'].sum().reset_index()
colors = ['#1f77b4', '#ff7f0e']
fig, ax = plt.subplots(figsize=(10, 6))
for i, gender in enumerate(grouped_data['Gender'].unique()):
    data_subset = grouped_data[grouped_data['Gender'] == gender]
    ax.bar(data_subset['RevenueVillageName'], data_subset['TOTAL'], label=gender, color=colors[i])
ax.set_xlabel('Revenue Village Name')
ax.set_ylabel('Total Beneficiaries')
ax.set_title(f'Gender-wise Beneficiary Counts for Year {selected_year}, Trimester {selected_trimester}')
ax.legend()
st.pyplot(fig)

#kisan scheme wordcloud
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

csv_file_path = 'D:/agrids/kisancall-2019.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = None
st.title('Word Cloud of  PM-KISAN Scheme ')
st.write('Queries asked to Kishan Scheme Call Center')
selected_column_name = 'data__QueryText'
if df is not None and selected_column_name in df.columns:
    text = ' '.join(df[selected_column_name].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)


#CROP PRICE
import seaborn as sns
st.title('Commodity Prices Visualization')
csv_file_path = 'D:/agrids/Price_Agriculture_commodities_Week.csv'
try:
    data = pd.read_csv(csv_file_path)
except FileNotFoundError:
    data = None
if data is not None:
    #st.subheader('Filter Data')
    selected_state = st.selectbox('Select State', data['State'].unique())
    selected_commodity = st.selectbox('Select Commodity', data['Commodity'].unique())
    filtered_data = data[(data['State'] == selected_state) & (data['Commodity'] == selected_commodity)]
    #st.write('Filtered Data:')
   # st.write(filtered_data)
    st.subheader('Time Series Line Plot')
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Arrival_Date', y='Modal Price', data=filtered_data)
    plt.xlabel('Arrival Date')
    plt.ylabel('Modal Price')
    plt.title(f'Modal Price Trend for {selected_commodity} in {selected_state}')
    st.pyplot(plt)