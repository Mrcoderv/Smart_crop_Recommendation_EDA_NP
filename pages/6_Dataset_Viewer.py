"""
Dataset Viewer Page - Browse and explore datasets
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_crop_data, load_climate_data

st.set_page_config(page_title="Dataset Viewer", page_icon="📊", layout="wide")

# Load custom CSS
with open("assets/styles/custom.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>📋 Dataset Viewer</h1>
        <p style='color: #d5f4e6; margin: 10px 0 0 0;'>Browse, Explore, and Download Datasets</p>
    </div>
""", unsafe_allow_html=True)

# Dataset Selection
st.markdown("### 📂 Available Datasets")

dataset_option = st.radio(
    "Select Dataset",
    ["Crop Production Data", "Climate Data"],
    horizontal=True
)

if dataset_option == "Crop Production Data":
    df = load_crop_data()
    dataset_name = "Crop Production"
else:
    df = load_climate_data()
    dataset_name = "Climate"

if df.empty:
    st.error(f"❌ {dataset_name} data not available")
    st.stop()

# Dataset Statistics
st.markdown("### 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Records", f"{len(df):,}")

with col2:
    st.metric("📋 Columns", len(df.columns))

with col3:
    st.metric("🔍 Missing Values", df.isnull().sum().sum())

with col4:
    st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# Data Preview
st.markdown("### 👀 Data Preview")

rows_to_show = st.slider("Number of rows to display", 5, 100, 20)
st.dataframe(df.head(rows_to_show), use_container_width=True)

# Column Information
st.markdown("### 📋 Column Information")

col_info = pd.DataFrame({
    'Column': df.columns,
    'Data Type': df.dtypes.values,
    'Non-Null Count': df.count().values,
    'Missing': df.isnull().sum().values,
    'Unique Values': [df[col].nunique() for col in df.columns]
})

st.dataframe(col_info, use_container_width=True)

# Descriptive Statistics
st.markdown("### 📈 Descriptive Statistics")

st.dataframe(df.describe().T, use_container_width=True)

# Filters
st.markdown("---")
st.markdown("### 🔍 Advanced Filters & Search")

col1, col2 = st.columns(2)

with col1:
    # Search by column
    search_column = st.selectbox("Select column to search", df.columns)
    
    if df[search_column].dtype == 'object':
        search_values = df[search_column].unique().tolist()
        selected_values = st.multiselect(
            f"Select {search_column}",
            search_values,
            default=search_values[:3] if len(search_values) > 3 else search_values
        )
        filtered_df = df[df[search_column].isin(selected_values)]
    else:
        min_val = df[search_column].min()
        max_val = df[search_column].max()
        selected_range = st.slider(
            f"{search_column} range",
            float(min_val),
            float(max_val),
            (float(min_val), float(max_val))
        )
        filtered_df = df[(df[search_column] >= selected_range[0]) & (df[search_column] <= selected_range[1])]

with col2:
    # Sort options
    sort_column = st.selectbox("Sort by column", df.columns)
    sort_order = st.radio("Sort order", ["Ascending", "Descending"], horizontal=True)
    
    ascending = sort_order == "Ascending"
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

st.markdown(f"### 📊 Filtered Data ({len(filtered_df)} records)")
st.dataframe(filtered_df, use_container_width=True)

# Export Options
st.markdown("---")
st.markdown("### 💾 Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{dataset_name.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

with col2:
    excel = filtered_df.to_excel(index=False) if 'openpyxl' in __import__('sys').modules else None
    
    try:
        buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
        filtered_df.to_excel(buffer, index=False)
        buffer.close()
        
        with open('temp.xlsx', 'rb') as f:
            st.download_button(
                label="📥 Download as Excel",
                data=f.read(),
                file_name=f"{dataset_name.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        import os
        os.remove('temp.xlsx')
    except:
        st.info("Excel export requires openpyxl library")

with col3:
    json_str = filtered_df.to_json(orient='records')
    st.download_button(
        label="📥 Download as JSON",
        data=json_str,
        file_name=f"{dataset_name.lower().replace(' ', '_')}.json",
        mime="application/json"
    )

# Data Quality Report
st.markdown("---")
st.markdown("### 🔍 Data Quality Report")

quality_report = {
    'Total Records': len(df),
    'Complete Records': len(df.dropna()),
    'Records with Missing Values': len(df) - len(df.dropna()),
    'Completeness Score': f"{(len(df.dropna()) / len(df) * 100):.1f}%",
    'Duplicate Records': len(df[df.duplicated()]),
    'Memory Usage': f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
}

for key, value in quality_report.items():
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write(f"**{key}**")
    with col_b:
        st.write(value)

# Data Distribution
st.markdown("---")
st.markdown("### 📊 Data Distribution Analysis")

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if numeric_cols:
    selected_col = st.selectbox("Select column for distribution", numeric_cols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"#### {selected_col} - Histogram")
        st.bar_chart(df[selected_col].value_counts().sort_index())
    
    with col2:
        st.write(f"#### {selected_col} - Statistics")
        col_stats = df[selected_col].describe()
        st.write(col_stats)

# Info Box
st.markdown("""
    <hr>
    <div style='background: #f0f9f7; padding: 15px; border-radius: 8px; border-left: 4px solid #9b59b6;'>
        <h4>ℹ️ About Datasets</h4>
        <ul>
            <li><strong>Crop Production Data:</strong> Contains information about crop production, area under cultivation, and yield across Nepal districts</li>
            <li><strong>Climate Data:</strong> Historical climate information including temperature, rainfall, and other meteorological parameters</li>
        </ul>
        <p>Use the filters and search features above to explore specific datasets and generate custom reports.</p>
    </div>
""", unsafe_allow_html=True)
