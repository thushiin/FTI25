import streamlit as st
import importlib

st.set_page_config(page_title="FTI", layout="wide", initial_sidebar_state="expanded")

region_modules = {
    "All Regions": "main_dashboard",
    "Muscat": "MCT",
    "Ad Dakhliyah": "DKL",
    "Ash Sharqiyah South": "SHS",
    "Ash Sharqiyah North": "SHN",
    "Al Wusta": "WST",
    "Al Batinah North": "BTN",
    "Al Batinah South": "BTS",
    "Musandam": "MSD",
    "Adh Dhahirah": "DHR",
    "Buraimi":"BRM"
}

cluster_map = {
    "Cluster 1": ["Muscat", "Ash Sharqiyah North", "Ash Sharqiyah South"],
    "Cluster 2": ["Al Batinah North", "Adh Dhahirah", "Musandam"],
    "Cluster 3": ["Ad Dakhliyah", "Al Batinah South", "Al Wusta","Buraimi"],
    "All Clusters": ["Muscat", "Ash Sharqiyah North", "Ash Sharqiyah South",
                    "Al Batinah North", "Adh Dhahirah", "Musandam",
                    "Ad Dakhliyah", "Al Batinah South", "Al Wusta","Buraimi"],
}

# Initialize selected_clusters in session_state if missing, so sidebar_options are stable
if 'initialized' not in st.session_state:
    st.session_state['selected_clusters'] = ["All Clusters"]
    st.session_state['initialized'] = True
    st.rerun()


selected_clusters = st.session_state['selected_clusters']

if selected_clusters:
    # Flatten selected regions from the clusters
    selected_regions = []
    for cluster in selected_clusters:
        selected_regions.extend(cluster_map.get(cluster, []))
    
    # Always keep "All Regions" as first option if you want
    sidebar_options = ["All Regions"] + selected_regions
else:
    # Default to all regions if nothing selected
    sidebar_options = list(region_modules.keys())

# Sidebar selection
st.sidebar.title("🔎 Select Dashboard")
page = st.sidebar.radio("Navigation", sidebar_options, label_visibility="collapsed")

# Map sidebar name to module name — handle "All Regions" accordingly
if page == "All Regions":
    module_name = region_modules["All Regions"]
else:
    # If user picks a region code like "MCT", make sure mapping is consistent:
    # If your sidebar_options contains region codes, map them correctly here
    # If sidebar_options contains full names, map using region_modules
    module_name = region_modules.get(page, "main_dashboard")

st.sidebar.markdown(
    f"""
    <style>
    .last-updated {{
        position: fixed;
        bottom: 10px;
        left: 10px;
        font-size: 12px;
        color: gray;
        z-index: 9999;
    }}
    </style>
    <div class="last-updated">
        Last updated on: 30-11-2025
    </div>
    """,
    unsafe_allow_html=True
)


module = importlib.import_module(module_name)
#importlib.reload(module)
module.run()




