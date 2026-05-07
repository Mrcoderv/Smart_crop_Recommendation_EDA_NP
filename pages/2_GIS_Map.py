import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from utils.data_loader import load_crop_data, load_geojson_data, get_unique_crops, get_unique_provinces

st.set_page_config(page_title="GIS Map", page_icon="🗺️", layout="wide")

st.title("🗺️ GIS Crop Production Map of Nepal")
st.markdown("Visualize crop distribution and production intensity across various districts.")

# Load Data
df = load_crop_data()
gdf = load_geojson_data()

if df.empty or gdf.empty:
    st.warning("Data or GIS files missing. Please run the dummy dataset generator.")
    st.stop()

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    selected_crop = st.selectbox("Select Crop to Visualize", ["All"] + get_unique_crops(df))
with col2:
    selected_province = st.selectbox("Select Province", ["All"] + get_unique_provinces(df))
with col3:
    map_metric = st.selectbox("Metric to visualize", ["Production_MT", "Area_Hectares", "Yield_Kg_Ha"])

# Process Data for Map
map_df = df.copy()

if selected_crop != "All":
    map_df = map_df[map_df['Crop'] == selected_crop]
if selected_province != "All":
    map_df = map_df[map_df['Province'] == selected_province]

# Aggregate metrics by district
agg_df = map_df.groupby('District', as_index=False)[map_metric].sum()

st.markdown(f"### {map_metric} by District")

# Centered at Nepal Coordinates
m = folium.Map(location=[28.3949, 84.1240], zoom_start=6, tiles="cartodbpositron")

if not agg_df.empty:
    # Creating a dictionary for custom tooltips (if desired) or simple choropleth
    # For a real dataset, we ideally merge geojson with DataFrame, but choropleth takes key_on
    choropleth = folium.Choropleth(
        geo_data=gdf.__geo_interface__,
        name="choropleth",
        data=agg_df,
        columns=["District", map_metric],
        key_on="feature.properties.DISTRICT",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{map_metric}",
        highlight=True
    ).add_to(m)

    # Add tooltips over GEOJSON
    # First, let's create a lookup dict
    metric_dict = agg_df.set_index('District')[map_metric].to_dict()

    # Add tooltip using GeoJsonTooltip
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add metric to properties for tooltip
    # First we have to iterate the GeoDataFrame to inject the metric.
    # We loaded json directly or as GeoDataFrame. We use the original gdf.
    gdf_tooltip = gdf.copy()
    gdf_tooltip['Metric'] = gdf_tooltip['DISTRICT'].map(metric_dict).fillna(0).apply(lambda x: f"{x:,.2f}")

    folium.features.GeoJson(
        gdf_tooltip,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['DISTRICT', 'Province', 'Metric'],
            aliases=['District: ', 'Province: ', f'{map_metric}: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    ).add_to(m)
else:
    st.info("No data to aggregate for the selected filters.")

# Render Map
st_folium(m, width=1000, height=500, returned_objects=[])

st.markdown("---")
st.markdown("### Top Districts for selected filters")
if not agg_df.empty:
    st.dataframe(agg_df.sort_values(by=map_metric, ascending=False).head(10).reset_index(drop=True), use_container_width=True)
