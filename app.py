import streamlit as st
from utils.data_loader import load_crop_data
from utils.processor import get_summary_stats

# Must be the first Streamlit command
st.set_page_config(
    page_title="Nepal SmartAgri System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🌾 Climate & Season Based Crop Recommendation system for Nepal")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Nepal SmartAgri Dashboard
    This platform provides comprehensive Exploratory Data Analysis (EDA) on crop production, 
    climate, and seasonal patterns across Nepal's districts and provinces. 
    It leverages GIS visualizations and rule-based logic to recommend suitable crops 
    for different geographic and climatic profiles in Nepal.
    """)
    
    # Load basic data for stats
    df = load_crop_data()
    
    if not df.empty:
        st.subheader("📊 Nepal Agriculture Statistics Overview")
        
        stats = get_summary_stats(df)
        
        # Dashboard cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Crops Analyzed", f"{stats['total_crops']}")
            st.metric("Districts Covered", f"{stats['total_districts']}")
        with col2:
            st.metric("Total Production (MT)", f"{stats['total_production']:,.2f}")
            st.metric("Total Area (Hectares)", f"{stats['total_area']:,.2f}")
        with col3:
            st.metric("Average Yield (Kg/Ha)", f"{stats['avg_yield']:,.2f}")
            st.metric("Top Crop by Production", f"{stats['top_crop']}")
        with col4:
            st.metric("Top Producing District", f"{stats['top_district']}")
            
        st.markdown("---")
        st.info("👈 Please use the Sidebar Navigation to explore the Dashboard, GIS Maps, and Crop Recommendation Tool.")
        
    else:
        st.warning("Data not available. Please ensure the dataset is generated.")
        
    # Add footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: gray;
            text-align: center;
        }
        </style>
        <div class="footer">
            <p>Developed for the Nepal Agriculture Community 🌿</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
