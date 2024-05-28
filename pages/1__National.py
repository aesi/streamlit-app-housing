import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    df['year'] = df['year'].astype(str)
    return df
st.write('# National-level Analysis')
grouped_year = load_data('grouped_year.xlsx')
grouped_year_state = load_data('grouped_year_state.xlsx')
def plot_sold(df):
    fig = px.line(
        df,
        x = 'year',
        y = 'homes_sold',
        title = 'Cumulative Inflation from 2012 to 2023',
        markers = True
    )
    st.plotly_chart(fig, use_container_width = True)

def price_change(old_price, new_price):
    return round(((new_price/old_price) - 1) * 100)

def plot_inflation(df):
    fig = px.line(
        df,
        x = 'year',
        y = 'cumulative_inflation_since_2012',
        title = 'Cumulative Inflation from 2012 to 2023',
        markers = True
    )
    st.plotly_chart(fig, use_container_width = True)

plot_inflation(grouped_year)


st.write("Cumulative Inflation has increased by about 31% from 2012 to 2023. Cumulative inflation provides a more accurate insight into long windows of analysis as it factors in the compounding effect of inflation that year-over-year (YOY) inflation doesn't take into account over a long period of time. This is important for determining the purchasing power of currency and can be used to adjust prices for inflation.", unsafe_allow_html=True)
st.write('Both average YOY inflation and cumulative inflation were calculated from CPI.')
st.write('We can use this to adjust salaries and housing prices for inflation to provide more accurate assessments of economic situations.')

def plot_sale_price_vs_adj(df):
    fig = px.line(df, x = 'year', 
                  y = ['median_sale_price', 'median_sale_price_adj'],
                  labels = {'_value': 'Median Sale Price'},
                  title = 'Median One Family Home Sale Price vs. Inflation Adjusted Price')
                  
    st.plotly_chart(fig, use_container_width = True)
plot_sale_price_vs_adj(grouped_year)

price_increase_adj_nat = price_change(166000, 283000)
price_increase_2019_2021 = price_change(233000, 277600)
price_decrease_2022 = abs(price_change(286600, 283700))
st.write(f'When accounting for inflation, the median sale price of a single-family home in the US increased from 166,000 in 2012 to 283,000 in 2023 ({price_increase_adj_nat}% price increase).')
st.write(f'Housing prices have been steadily increasing since 2012 and there was a massive inflation-adjusted jump from 2019 to 2021 at 233,000 to 277,600 for a single-family home ({price_increase_2019_2021}% price increase).')
st.write(f"Prices are starting to show signs of stabilization starting from 2022. The adjusted housing price slightly decreased from 286,600 to 283,700 from 2022 to 2023 ({price_decrease_2022}% decrease).")
def plot_wage_vs_adj(df):
    fig = px.line(df, x = 'year', 
                  y = ['median_salary', 'median_salary_adj'],
                  labels = {'_value': 'Median Salary'},
                  title = 'Median Salary vs. Inflation Adjusted Salary')
    st.plotly_chart(fig, use_container_width = False)

price_increase_salary_adj = price_change(33000, 36000)    
plot_wage_vs_adj(grouped_year)
st.write(f'On the other hand, the annual median salary has only increased from 33,000 in 2012 to 36,000 in 2023. This is a {price_increase_salary_adj}% increase in salary after adjusting for inflation.')
st.write("Inflation-adjusted wages decreased from 2020 to 2021 (35,900 to 33,600) during COVID yet inflation-adjusted median housing prices increased from 252,000 to 277,600.")