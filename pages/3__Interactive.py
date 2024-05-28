import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Interactive Streamlit Dashboard')
@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    df['year'] = df['year'].astype(str)
    return df

state = load_data('grouped_year_state.xlsx')
state_2023 = state[state['year'] == '2023']
state_2023['wage_relative_to_price'] = state_2023['median_salary']/state_2023['median_sale_price']
option = st.selectbox(label = 'Please select a state to see information', options = state['state'].unique())
state_sub = state[state['state'] == option]
state_2023_sub = state_2023[state_2023['state'] == option]

def price_change(old_price, new_price):
    return round(((new_price/old_price) - 1) * 100)

# Home Sales Hist Section
def plot_hist(df):
    fig = px.bar(
        df,
        x = 'year',
        y = 'homes_sold',
        title = 'Homes Sold by Year',
        color = 'homes_sold',
        color_continuous_scale = 'RdYlGn',

    )
    fig.update_layout(height = 500, width = 500)
    st.plotly_chart(fig, use_container_width = False)

homes_sold_min = state_sub['homes_sold'].min()
homes_sold_max = state_sub['homes_sold'].max()
homes_sold_min_year = state_sub[state_sub['homes_sold'] == homes_sold_min]['year'].iloc[0]
homes_sold_max_year = state_sub[state_sub['homes_sold'] == homes_sold_max]['year'].iloc[0]

# Home Sale Price by Year
def price_year(df):
    fig = px.line(
        df,
        x = 'year',
        y = ['median_sale_price', 'median_sale_price_adj'],
        labels = {'_value': 'Median Sale Price'},
        title = 'Inflation Adjusted Median One-Family Home Sale Price by Year',
        markers = True
    )
    fig.update_layout(height = 500, width = 500)
    st.plotly_chart(fig, use_container_width = False)

price_2012 = round(state_sub[state_sub['year'] == '2012']['median_sale_price'].iloc[0])
price_2023 = round(state_sub[state_sub['year'] == '2023']['median_sale_price'].iloc[0])
price_2023_adj = round(state_sub[state_sub['year'] == '2023']['median_sale_price_adj'].iloc[0])

price_increase = price_change(price_2012, price_2023)
price_increase_adj = price_change(price_2012, price_2023_adj)
price_adj_diff_2023 = price_change(price_2023_adj, price_2023)

def salary_year(df):
    fig = px.line(
        df,
        x = 'year',
        y = ['median_salary', 'median_salary_adj'],
        labels = {'_value': 'Median Salary'},
        title = 'Inflation Adjusted Median Salary by Year',
        markers = True
    )
    fig.update_layout(height = 500, width = 500)
    st.plotly_chart(fig, use_container_width = False)



ratio_lst = state_2023['wage_relative_to_price'].to_list()
ratio_lst.sort(reverse = True)
ratio = state_2023_sub['wage_relative_to_price'].iloc[0]
rank = ratio_lst.index(ratio)
true_rank = rank + 1
better_states = 50 - true_rank

salary_2012 = state_sub[state_sub['year'] == '2012']['median_salary'].iloc[0]
salary_2023 = state_sub[state_sub['year'] == '2023']['median_salary'].iloc[0]
salary_2023_adj =  state_sub[state_sub['year'] == '2023']['median_salary_adj'].iloc[0]
salary_increase = price_change(salary_2012, salary_2023)
salary_increase_adj = price_change(salary_2012, salary_2023_adj)

st.markdown("""
    <style>
    .full-width-markdown {
        width: 100% !important;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

col1, _, col2 = st.columns([1, 1.5, 1])
with col1:
    st.markdown("## <span style='white-space: nowrap;'>2023 Median Salary</span>", unsafe_allow_html=True)
    st.metric(label = f'State: {option}', value = state_2023_sub['median_salary'])
    plot_hist(state_sub)
    st.markdown(f"""<span style='white-space: nowrap;'> 
                In {option} the minimum count of home sales was <span style  = 'color: red;'>{homes_sold_min}</span> in {homes_sold_min_year} 
                <br> and the maximum was <span style  = 'color: green;'>{homes_sold_max}</span> in {homes_sold_max_year}.
                </span>""", unsafe_allow_html=True)
    salary_year(state_sub)
    st.markdown(f"""<span style='white-space: nowrap;'>
                {option}'s median salary increased from {salary_2012} in 2012 to {salary_2023} in 2023.
                <br> This was a <span style = 'color: green'>{salary_increase}%</span> increase. When adjusted for inflation, the increase was <span style = 'color: orange'>{salary_increase_adj}%</span>.
                </span>""", unsafe_allow_html=True)
with col2:
    st.markdown("## <span style='white-space: nowrap;'>2023 Median Home Price</span>", unsafe_allow_html=True)
    st.metric('Single-Family Home Sale Price', value = state_2023_sub['median_sale_price'])
    price_year(state_sub)
    st.markdown(f"""<span style='white-space: nowrap;'> 
                {option}'s home sale prices increased from {price_2012} in 2012 to {price_2023} in 2023.
                <br> This was a(n) <span style = 'color: red'>{price_increase}%</span> increase in price.
                <br> The inflation-adjusted price in 2023 was {price_2023_adj} (<span style = 'color: orange'>{price_adj_diff_2023}%</span> less than {price_2023}).
                </span>""", unsafe_allow_html=True)
# <br> The difference between the price and inflation-adjusted price is <span style = 'color: red'>{price_increase_adj}%</span>.
    st.markdown("## <span style='white-space: nowrap;'>2023 Affordability</span>", unsafe_allow_html=True)
    # st.markdown("# 2023 Affordability Comparison")
    st.metric(label = f"{option}'s Affordability Rank", value = str(rank + 1) + '/ 50')
    st.metric(label = f"Score of ", value = round(ratio, 2) , help = 'Calculated as salary / price to represent how many times the salary can afford the given price. Higher is better.')
    st.markdown(f"""<span style='white-space: nowrap;'>
                {option} comes in at rank {true_rank} out of 50 according to the affordability index.
                <br> There are currently {better_states} state(s) that rank lower than {option} in the US.
                <br> 
                </span>""", unsafe_allow_html=True)