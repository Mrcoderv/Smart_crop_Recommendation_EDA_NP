import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_crop_data, get_unique_provinces, get_unique_districts, get_unique_crops, get_unique_months
from utils.processor import filter_data

st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

st.title("📈 Agriculture Data Analysis Dashboard")
st.markdown("Explore crop production patterns, rainfall variations, and temperature impacts.")

df = load_crop_data()

if df.empty:
    st.warning("No data available to display dashboard.")
    st.stop()

# Interactive Filters
st.sidebar.header("Filter Data")
selected_province = st.sidebar.selectbox("Select Province", ["All"] + get_unique_provinces(df))
selected_district = st.sidebar.selectbox("Select District", ["All"] + get_unique_districts(df))
selected_crop = st.sidebar.selectbox("Select Crop", ["All"] + get_unique_crops(df))
selected_month = st.sidebar.selectbox("Select Planting Month", ["All"] + get_unique_months(df))

# Apply filters
filtered_df = df.copy()
if selected_province != "All":
    filtered_df = filtered_df[filtered_df['Province'] == selected_province]
if selected_district != "All":
    filtered_df = filtered_df[filtered_df['District'] == selected_district]
if selected_crop != "All":
    filtered_df = filtered_df[filtered_df['Crop'] == selected_crop]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df['Planting_Month'] == selected_month]

if filtered_df.empty:
    st.warning("No data matching the selected filters.")
    st.stop()

# Row 1: Bar Chart & Pie Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Production by District")
    prod_by_dist = filtered_df.groupby('District')['Production_MT'].sum().reset_index()
    fig1 = px.bar(prod_by_dist, x='District', y='Production_MT', color='Production_MT', color_continuous_scale='Greens')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Crop Production Share")
    prod_by_crop = filtered_df.groupby('Crop')['Production_MT'].sum().reset_index()
    fig2 = px.pie(prod_by_crop, names='Crop', values='Production_MT', hole=0.3, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Line chart (Yearly Trend) and Histogram
col3, col4 = st.columns(2)

with col3:
    st.subheader("Yearly Production Trend")
    yearly_prod = filtered_df.groupby('Year')['Production_MT'].sum().reset_index()
    fig3 = px.line(yearly_prod, x='Year', y='Production_MT', markers=True)
    fig3.update_traces(line_color='green')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Distribution of Yield (Kg/Ha)")
    fig4 = px.histogram(filtered_df, x='Yield_Kg_Ha', nbins=30, color_discrete_sequence=['#ff9999'])
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Scatter Plot & Correlation Matrix Heatmap
col5, col6 = st.columns(2)

with col5:
    st.subheader("Rainfall vs Production")
    fig5 = px.scatter(filtered_df, x='Avg_Rainfall_mm', y='Production_MT', color='Crop', size='Area_Hectares', hover_data=['District'])
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Correlation Matrix")
    # Select numerical columns
    num_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
    corr_matrix = filtered_df[num_cols].corr()
    
    fig6 = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.markdown("### Raw Data Viewer")
st.dataframe(filtered_df, use_container_width=True)
