import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    df['year'] = df['year'].astype(str)
    return df

state = load_data('grouped_year_state.xlsx')
state_2023 = state[state['year'] == '2023']
state_2023['wage_relative_to_price'] = (state_2023['median_salary'] / state_2023['median_sale_price'])
affordability_lst = state_2023['wage_relative_to_price'].to_list()

def price_change(old_price, new_price):
    return round(((new_price/old_price) - 1) * 100)

st.write('# State-level Analysis')
def plot_wage(df):
    fig = px.choropleth(
        df,
        locations = 'state_code',
        scope = 'usa',
        locationmode = 'USA-states',
        color = 'median_salary',
        color_continuous_scale = 'RdYlGn',
        hover_data = 'state',
        title = 'Median Salary by State in 2023'
    )
    st.plotly_chart(fig, use_container_width = True)

plot_wage(state_2023)
st.write("In 2023 the state with the highest median salary in the US was Massachusetts at about 60,700 and the lowest being Mississippi at 37,500.")
st.write("The trend across the US is that the states with the lowest salaries tend to be centralized along the southeast.")
st.write("The highest salaried states seem to be centralized at both the northeast section of the US near New York and alongside the west coast encompassing Washington, Oregon, and California.")
def plot_price(df):
    fig = px.choropleth(
        df,
        locations = 'state_code',
        scope = 'usa',
        locationmode = 'USA-states',
        color = 'median_sale_price',
        color_continuous_scale = 'RdYlGn_r',
        hover_data = 'state',
        title = 'Median One Family Home Sale Price by State in 2023'
    )
    st.plotly_chart(fig, use_container_width = True)

plot_price(state_2023)
st.write("The median sale prices of single-family homes appears to positively correlate with median salaries.")
st.write("We see that the cheapest single-family homes are centralized around the southeast and midwest regions of the US.")
st.write("Hawaii and California have astronomically high median home sale prices at 902,000 and 812,000 respectively.")
def ratio_scatter(df):
    fig = px.scatter(
        df,
        x = 'median_sale_price',
        y = 'median_salary',
        text = 'state_code',
        color = 'median_sale_price',
        color_continuous_scale = 'Blackbody_r',
        title = 'Median Salary vs. Median Home Price (2023)',
    )
    fig.update_traces(textposition = 'top right')
    st.plotly_chart(fig, use_container_width = True)
ratio_scatter(state_2023)

# median_price_normality = stats.normaltest(state_2023['median_sale_price'])
# median_salary_normality = stats.normaltest(state_2023['median_salary'])
correlation = stats.pearsonr(state_2023['median_sale_price'], state_2023['median_salary'])
# st.write(median_price_normality)
# st.write(median_salary_normality)


st.write("We see that the vast majority of states possess a positive correlation between median salary and median home sale price. This is reflected in the Pearson Correlation Coefficient:")
st.write(correlation)
st.write("A correlation coefficient of about 0.6 indicates a moderately positive correlation between wage and price. The p-value is extremely low which stands to reject the null hypothesis that there is no correlation between the two variables.")
st.write("Median salaries of Iowa (46,500) and Ohio (46,700) have relatively high median salaries compared to their housing prices (226,500 and 237,100 respectively). These are the states with the least egregious salary to price ratios and thus would be prime candidates financially for people looking to live, work, and purchase a home.")
st.write("California and Hawaii are the only states that blatantly exist outside of the general positive correlation between salary and home price. This means that it is much more difficult to purchase a house in these two states provided the individual also works in one of these states when compared to working and purchasing in other states.")

def plot_ratio(df):
    fig = px.choropleth(
        df,
        locations = 'state_code',
        scope = 'usa',
        locationmode = 'USA-states',
        color = 'wage_relative_to_price',
        color_continuous_scale = 'RdYlGn',
        hover_data = 'state',
        title = 'Best Salary to Housing Price Ratios'
    )
    st.plotly_chart(fig, use_container_width = True)

plot_ratio(state_2023)
st.write("This map shows the affordability ratio of each state and was calculated by salary / price which represents how many times the median salary can afford the median home price. This allows us to see the best and worst states relative to their salaries and home prices.")
st.write("When we visualize and rank the salary to housing price ratios on a map we see that the best performing states are in the midwest. This is mostly due to the fact that median wages are fairly close across states in comparison to housing prices which vary widely.")
st.write("We see that both the west and east coast suffer massively with this ratio as a metric. This means that the salaries of the coasts are too low and housing prices are too high when compared to other states.")