import pandas as pd
import plotly.express as px
import streamlit as st

# Title of dasboard
st.title("Sales Analytics Dashboard")
st.write("Analyse sales data withinteractive visulalisation.")

#load the dataset
def load_data():
    data = pd.read_csv("retail_sales_dataset.csv")
    data['Date'] = pd.to_datetime(data['Date']) # Conver date column to datetime
    return data

sales_data = load_data()

#Sidebar for filtering
st.sidebar.header("Filter options")

#Product category filter
categories = st.sidebar.multiselect(
    "Select product category(s):",
    options=sales_data['Product Category'].unique(),
    default=sales_data['Product Category'].unique()
)

#Gender filter
genders = st.sidebar.multiselect(
    "Select Genders(s)",
    options=sales_data['Gender'].unique(),
    default=sales_data['Gender'].unique()
)

#Date range filter
date_range = st.sidebar.date_input(
    "Select date range",
    value=[sales_data['Date'].min(), sales_data['Date'].max()]
)

#Apply filters
filtered_data = sales_data[
    (sales_data['Product Category'].isin(categories)) &
    (sales_data['Gender'].isin(genders)) &
    (sales_data['Date'] >= pd.Timestamp(date_range[0])) &
    (sales_data['Date'] <= pd.Timestamp(date_range[1]))
]

#display filtered datasets
st.subheader("Fitered Sales Data")
st.dataframe(filtered_data)

#STotal sales by product category plot
st.subheader("Total sales by product category")
category_sales=(
    filtered_data.groupby('Product category')['Total Amount']
    .sum()
    .reset_index()
    .sort_values('Total Amount', ascending=False)
)
fig1=px.bar(
    category_sales,
    x = 'Product Category',
    y = 'Total Amount',
    color = 'Product Category',
    title = "Sales by Product Category"
)
st.plotly_chart(fig1)

#Total Sales by gender plot
st.subheader("Total Sales by gender")
gender_sales = (
    filtered_data.groupby('Gender')['Total Amount']
    .sum()
    .reset_index()
    .sort_values('Total Amount', ascending=False)
)
fig2 = px.pie(
    gender_sales,
    names='Gender',
    values='Total Amount',
    title="Sales distribution by gender"
)
st.plotly_chart(fig2)

#Sales Trends Over Time Plot
st.subheader("Sales Trends Over Time")
time_sales = filtered_data.groupby('Date')['Total Amount'].sum().reset_index()
fig3 = px.line(
    time_sales,
    x='Date',
    y='Total Amount',
    title="Sales Trends Over Time",
    markers=True
)
st.plotly_chart(fig3)

#Quantity Sold by Product quantity plot
st.subheader("Quatity Sold by Product Quantity")
quantity_sales = (
    filtered_data.groupby('Product Category')['Quantity']
    .sum()
    .reset_index()
    .sort_values('Quantity', ascending=False)
)
fig4 = px.bar(
    quantity_sales,
    x='Product Category',
    y='Quantity',
    color='Product Category',
    title="Quantity Sold by Product Category"
)
st.plotly_chart(fig4)

#Footer
st.write("Dashboard created with streamlit and plotly")