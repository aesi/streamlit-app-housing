import streamlit as st
import pandas as pd
import plotly.express as px

st.write(' # Housing Price and Salary Analysis')
st.write(' ## Table of Contents')
st.write(' #### 1. National - Analysis spanning across the entire US as an aggregate')
st.write('a. Cumulative Inflation from 2012 to 2023')
st.write('b. Median One-Family Home Sale Price vs. Inflation Adjusted Price')
st.write('c. Median Salary vs. Inflation Adjusted Salary')
st.write(' #### 2. State - Analysis of individual states in the US')
st.write('a. Median Salary by State in 2023')
st.write('b. Median One-Family Home Sale Price by State in 2023')
st.write('c. Median Salary vs. Median Home Price in 2023')
st.write('d. Best Salary to Housing Price Ratios')
st.write(' #### 3. Interactive  - Contains Dynamic Streamlit Dashboard')
st.write('a. Dashboard that allows user to pick specific states through a picklist which dynamically updates the all elements on the dashboard')
st.write('b. 2023 Median Salary')
st.write('c. 2023 Median One-Family Home Sale Price')
st.write('d. Homes Sold by Year')
st.write('e. Inflation Adjusted Median One-Family Home Sale Price by Year')
st.write('f. Inflation Adjusted Median Salary by Year')
st.write('g. 2023 Affordability ratio and ranking')
st.write(' #### 4. PowerBI - Contains downloadable Power BI dashboard')
st.write('a. Power BI Dashboard preview')
st.write('b .pbix Power BI eXchange link file download')