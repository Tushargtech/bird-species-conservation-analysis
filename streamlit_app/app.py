import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset
df = pd.read_csv("cleaned_bird_observation_data.csv")

# Page config
st.set_page_config(page_title="Bird Species Observation Dashboard", layout="wide")
st.title("🕊️ Bird Species Observation Analysis")
st.markdown("""
Explore bird species observations across different locations, habitats, and environmental conditions using this interactive dashboard.
""")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    year = st.multiselect("Select Year(s)", options=sorted(df['Year'].dropna().unique()), default=sorted(df['Year'].dropna().unique()))
    habitat = st.multiselect("Select Habitat(s)", options=df['Habitat'].dropna().unique(), default=df['Habitat'].dropna().unique())
    season = st.multiselect("Select Season(s)", options=['Winter', 'Spring', 'Summer', 'Fall'], default=['Winter', 'Spring', 'Summer', 'Fall'])
    observer = st.multiselect("Select Observer(s)", options=df['Observer'].dropna().unique())

# Apply filters
filtered_df = df[df['Year'].isin(year) & df['Habitat'].isin(habitat) & df['Season'].isin(season)]
if observer:
    filtered_df = filtered_df[filtered_df['Observer'].isin(observer)]

# KPI Section
st.subheader("Key Statistics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Observations", len(filtered_df))
kpi2.metric("Unique Species", filtered_df['scientific_name'].nunique())
kpi3.metric("Watchlist Species", filtered_df[filtered_df['watchlist_status']==True]['scientific_name'].nunique())
kpi4.metric("Unique Sites", filtered_df['Site_Name'].nunique())

# Tabs for sections
tab1, tab2, tab3, tab4 = st.tabs(["Species Distribution", "Time Trends", "Environmental Factors", "Observer Insights"])

with tab1:
    st.subheader("Top 10 Most Observed Bird Species")
    species_count = filtered_df['common_name'].value_counts().nlargest(10).reset_index()
    species_count.columns = ['common_name', 'count']
    fig1 = px.bar(species_count, x='common_name', y='count', labels={'common_name': 'Species', 'count': 'Count'})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Observation by Habitat")
    fig2 = px.pie(filtered_df, names='Habitat', title='Habitat Distribution')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Observation Trends Over Time")
    by_year = filtered_df.groupby('Year')['common_name'].count().reset_index()
    fig3 = px.bar(by_year, x='Year', y='common_name', title='Observations by Year', labels={'common_name': 'Count'})
    st.plotly_chart(fig3, use_container_width=True)

    by_month = filtered_df['Month'].value_counts().sort_index().reset_index()
    by_month.columns = ['Month', 'Count']
    fig4 = px.bar(by_month, x='Month', y='Count', title='Observations by Month')
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Seasonal Observation Trend")
    season_count = filtered_df['Season'].value_counts().reset_index()
    season_count.columns = ['Season', 'Count']
    fig5 = px.bar(season_count, x='Season', y='Count')
    st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.subheader("Temperature and Humidity Distribution")
    col1, col2 = st.columns(2)
    with col1:
        fig6 = px.histogram(filtered_df, x='Temperature', nbins=30, title='Temperature Distribution')
        st.plotly_chart(fig6, use_container_width=True)
    with col2:
        fig7 = px.histogram(filtered_df, x='Humidity', nbins=30, title='Humidity Distribution')
        st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Sky and Wind Conditions")
    col3, col4 = st.columns(2)
    with col3:
        sky_count = filtered_df['Sky'].value_counts().reset_index()
        sky_count.columns = ['Sky', 'Count']
        fig8 = px.bar(sky_count, x='Sky', y='Count')
        st.plotly_chart(fig8, use_container_width=True)
    with col4:
        wind_count = filtered_df['Wind'].value_counts().reset_index()
        wind_count.columns = ['Wind', 'Count']
        fig9 = px.bar(wind_count, x='Wind', y='Count')
        st.plotly_chart(fig9, use_container_width=True)

with tab4:
    st.subheader("Top 10 Observers")
    top_obs = filtered_df['Observer'].value_counts().nlargest(10).reset_index()
    top_obs.columns = ['Observer', 'Observations']
    fig10 = px.bar(top_obs, x='Observer', y='Observations')
    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("Observers by Species Diversity")
    obs_species = filtered_df.groupby('Observer')['scientific_name'].nunique().sort_values(ascending=False).head(10).reset_index()
    obs_species.columns = ['Observer', 'Unique Species']
    fig11 = px.bar(obs_species, x='Observer', y='Unique Species')
    st.plotly_chart(fig11, use_container_width=True)

st.markdown("---")
st.caption("Developed using Streamlit and Plotly ✨ | Bird Monitoring Dataset")

