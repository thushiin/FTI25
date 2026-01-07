import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
import base64
from theme import set_theme
import math



def load_combined_data():
    sheet_id = "1lWA-uWBUXzG5iu2ghPEym2SDLhfC3VlDnqBdev9q1H0"  
    sheet_name = "Sheet1"              
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)



def run():
    set_theme()



    st.markdown("<h1 style='text-align: center; font-size: 38px;'>FIELD TECHNICAL INVESTIGATION 2025</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
    # Load Data
    df = load_combined_data()
    
    cluster_map = {
    "Cluster 1": ["MCT", "SHN", "SHS"],
    "Cluster 2": ["BTN", "DHR", "MSD"],
    "Cluster 3": ["DKL", "BTS", "WST", "BRM"],
    "All Clusters": ["MCT", "SHN", "SHS",
                         "BTN", "DHR", "MSD",
                         "DKL", "BTS", "WST", "BRM"]
    }
    
    
    team_engineer_data = {
    "MCT": {"teams": {"Galfar": 19, "Global": 27, "Al Tayer": 0}, "engineers": {"Galfar": 7, "Global": 4, "Al Tayer": 0}, "mg": {"Galfar": 1, "Global": 0, "Al Tayer": 0}},
    "SHN": {"teams": {"Galfar": 0, "Global": 0, "Al Tayer": 10}, "engineers": {"Galfar": 0, "Global": 0, "Al Tayer": 10}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "SHS": {"teams": {"Galfar": 8, "Global": 0, "Al Tayer": 0}, "engineers": {"Galfar": 1, "Global": 0, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "BTN": {"teams": {"Galfar": 10, "Global": 0, "Al Tayer": 0}, "engineers": {"Galfar": 1, "Global": 0, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "DHR": {"teams": {"Galfar": 0, "Global": 8, "Al Tayer": 0}, "engineers": {"Galfar": 0, "Global": 2, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 1, "Al Tayer": 0}},
    "MSD": {"teams": {"Galfar": 4, "Global": 0, "Al Tayer": 0}, "engineers": {"Galfar": 1, "Global": 0, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "DKL": {"teams": {"Galfar": 16, "Global": 0, "Al Tayer": 0}, "engineers": {"Galfar": 1, "Global": 0, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "BTS": {"teams": {"Galfar": 24, "Global": 0, "Al Tayer": 0}, "engineers": {"Galfar": 1, "Global": 0, "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "WST": {"teams": {"Galfar": 0, "Global": 0, "Al Tayer": 2}, "engineers": {"Galfar": 0, "Global": 0, "Al Tayer": 2}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}},
    "BRM": {"teams": {"Galfar": 0, "Global": 4, "Al Tayer": 0}, "engineers": {"Galfar": 0, "Global":0 , "Al Tayer": 0}, "mg": {"Galfar": 0, "Global": 0, "Al Tayer": 0}}
}



    # Better horizontal layout using 4 columns
    col1, col2, col3 = st.columns([1, 3, 1])
    

    
    # Cluster checkboxes inline
    cluster_labels = list(cluster_map.keys())[:-1]  # Exclude "All Clusters"
    col_check1, col_check2, col_check3 = col2.columns(3)
    checkbox_columns = [col_check1, col_check2, col_check3]
    
    selected_clusters = []
    for i, cluster in enumerate(cluster_labels):
        if checkbox_columns[i%3].checkbox(cluster, value=True):
            selected_clusters.append(cluster)

    
    # Combine selected regions
    selected_regions = []
    for cluster in selected_clusters:
        selected_regions.extend(cluster_map[cluster])
    
    # Fallback if none selected
    if not selected_clusters:
        selected_regions = cluster_map["All Clusters"]

    if st.session_state.get('last_clusters') != selected_clusters:
        st.session_state['selected_clusters'] = selected_clusters
        st.session_state['last_clusters'] = selected_clusters
        st.rerun()
        
    # Month selector
    months = ["All Months"] + [f"{month} 2025" for month in df["Month"].unique()]
    selected_month = col3.selectbox("📅", months, label_visibility="collapsed")
    
    # Adjust the filter to remove the year when applying the filter to the DataFrame
    if selected_month != "All Months":
        # Remove the " 2025" suffix to match the original data
        filtered_month = selected_month.replace(" 2025", "")
        df = df[df["Month"] == filtered_month]
    
    # Filter regions
    df = df[df["REGION"].isin(selected_regions)]
        
        
    def sum_nested_values(regions, data, key):
        result = {"Galfar": 0, "Global": 0, "Al Tayer": 0}
        for region in regions:
            if region in data:
                for company, count in data[region][key].items():
                    result[company] += count
        return result
    
    total_teams = sum_nested_values(selected_regions, team_engineer_data, "teams")
    total_engineers = sum_nested_values(selected_regions, team_engineer_data, "engineers")
    pm= sum_nested_values(selected_regions, team_engineer_data, "mg")




    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    total = df['OMR CONVERSION'].sum()
    
    if total >= 1_000_000:
        value = math.floor(total / 10_000) / 100  # Truncate to 2 decimal places
        display_value = f"{value:,.2f}M"
    elif total >= 1_000:
        value = math.floor(total / 100) / 10  # Truncate to 1 decimal place
        display_value = f"{value:,.1f}K"
    else:
        display_value = f"{int(total):,}"

    
    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: #2D6A4F; 
                padding: 10px 15px; 
                border-radius: 12px; 
                box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
                text-align:center; 
                max-width: 250px; 
                margin: auto;
                margin-top: -45px;">
                <h5 style="margin-bottom:0px; padding-top:10px; font-family: 'Helvetica', serif; white-space: nowrap; color:white; height: 30px; font-size: 16px"">💰 Total Direct Savings </h5>
                <h5 style="margin-bottom:0px; margin-left: 20px; padding-top:5px; font-family: 'Helvetica', serif; white-space: nowrap; color:white; height: 30px; font-size: 16px""> OMR </h5>
                <p style="font-size: 30px; line-height: 1.6; font-family: 'Arial', serif; font-weight: 900; margin: 0; color:white; text-align: center;  text-shadow: 1px 1px 2px #000;">{display_value}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div style="
                background-color: #2D6A4F; 
                padding: 10px 15px; 
                border-radius: 12px; 
                box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
                text-align:center; 
                max-width: 250px; 
                margin: auto;">
                <h5 style="margin-bottom:0px; font-family: 'Helvetica', serif; white-space: nowrap; color:white; font-size: 14px">💧 Total Direct Savings (m&sup3;)</h5>
                <p style="font-size: 20px; line-height: 1.1; font-family: 'Arial', serif; font-weight: 1000; margin: 0; color:white; text-align: center;">{int(df['DIRECT SAVINGS'].sum()):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="
                background-color: #2D6A4F; 
                padding: 10px 15px; 
                border-radius: 12px; 
                box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
                text-align: center; 
                max-width: 250px;
                margin: auto;">
                <h5 style="margin-bottom: 0px; line-height: 1.1; font-family: 'Helvetica', serif; white-space: nowrap; color:white; font-size: 14px">⚠ Illegal Connections</h5>
                <p style="font-size: 20px; line-height: 1.1; font-family: 'Arial', serif; font-weight: 1000; margin: 0; color:white; text-align: center;">{int(df['ILLEGAL CONNECTION'].sum())}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f"""
            <div style="
                background-color: #2D6A4F; 
                padding: 10px 15px; 
                border-radius: 12px; 
                box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
                text-align: center; 
                max-width: 270px; 
                margin: auto;">
                <h5 style="margin-bottom: 0px; font-family: 'Helvetica', serif; white-space: nowrap; color:white;  font-size: 14px"">📊 Total Unique Meters</h5>
                <p style="font-size: 20px; line-height: 1.1; font-family: 'Arial', serif; font-weight: 1000; margin: 0; color:white; text-align: center;">{int(df['METER SURVEYED'].sum()):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(
            f"""
            <div style="
                background-color: #2D6A4F; 
                padding: 10px 15px; 
                border-radius: 12px; 
                box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
                text-align: center; 
                max-width: 250px; 
                margin: auto;">
                <h5 style="margin-bottom: 0px; font-family: 'Helvetica', serif; white-space: nowrap; color:white; font-size: 14px"">⚙️ Faulty Meters</h5>
                <p style="font-size: 20px; line-height: 1.1; font-family: 'Arial', serif; font-weight: 1000; margin: 0; color:white; text-align: center;">{int(df['UNIQUE FAULTY'].sum()):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)


    # Visualizations
    custom_colors = ["#74c69d", "#52b788", "#40916c", "#1b4332", "#95d5b2", "#d8f3dc"]
    custom_color1=["#081C15", "#1B4332", "#2D6A4F", "#40916C", "#52B788", "#74C69D", "#95D5B2", "#B7E4C7"]
    custom_color= ["#245944", "#2D6A4F","#40916C","#52B788","#74C69D","#95D5B2","#B7E4C7","#D8F3DC","#E9FCEB","#F0FFF4","#E0F9E0","#CFF4D2"]

    fig1 = px.bar(df, x="REGION", y="DIRECT SAVINGS", color="Month", title="DIRECT SAVINGS", color_discrete_sequence=custom_color, height=250)
    fig1.update_layout(
        title=dict(
    text="DIRECT SAVINGS",
    x=0.5,           # Center the title horizontally
    xanchor='center' # Anchor the title at the center
    ),margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor='white',
    plot_bgcolor='rgba(183,204,194,0)',
        font=dict(color="black", family='Segoe UI', size=14),
        hoverlabel=dict(
    font_size=13,
    font_family="Segoe UI",
    bgcolor="#32483D",
    font_color="white"), title_font=dict(color='black'), # Title font color
    legend=dict(font=dict(color='black'), bgcolor='rgba(0,0,0,0)'), xaxis=dict(
        tickfont=dict(color='black'),
        title_font=dict(color='black'),
        showgrid=False
    ),
    yaxis=dict(
        tickfont=dict(color='black'),
        title_font=dict(color='black'),
        showgrid=False
    )
    )

    

    fig2 = px.pie(df, names="REGION", values="ILLEGAL CONNECTION",title="ILLEGAL CONNECTION", color_discrete_sequence=custom_color, hole=0.4, height=250, width=500)
    fig2.update_traces(
    texttemplate='%{value}',
    textposition='inside',  # force all text to stay inside the pie slice
    insidetextorientation='radial',
    textfont=dict(color='white', size=12)
)
    
    fig2.update_layout(   title=dict(
        text="ILLEGAL CONNECTION",
        x=0.5,
        xanchor='center'
    ),margin=dict(l=0, r=0, t=60, b=30),
    paper_bgcolor='white',  # optional same background style
    plot_bgcolor='rgba(183,204,194,0)',     # optional
    font=dict(color="black"),title_font=dict(color='black'),hoverlabel=dict(
        font_size=13,
        font_family="Segoe UI",
        bgcolor="#32483D",
        font_color="white"), legend=dict(
        x=0.85,  # Move to the left by decreasing this value
        y=0.5,
        xanchor='left',
        bgcolor='rgba(0,0,0,0)' )

    )
    
    fig6 = px.pie(df, names="REGION", values="FAULTY METER",title="FAULTY METER", color_discrete_sequence=custom_color, hole=0.4, height=250, width=500)
    fig6.update_traces(
    texttemplate='%{value}',
    textposition='inside',  # force all text to stay inside the pie slice
    insidetextorientation='radial',
    textfont=dict(color='white', size=12)
)
    fig6.update_layout(   title=dict(
        text="FAULTY METER",
        x=0.5,
        xanchor='center'
    ),margin=dict(l=0, r=0, t=60, b=30),
    paper_bgcolor='white',  # optional same background style
    plot_bgcolor='rgba(183,204,194,0)',     # optional
    font=dict(color="black"),title_font=dict(color='black'),hoverlabel=dict(
        font_size=13,
        font_family="Segoe UI",
        bgcolor="#32483D",
        font_color="white"),

    )
    
    total_surveyed = df["TOTAL METER SURVEYED"].sum()

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_surveyed,
       
        gauge={'axis': {'range': [0, df["TOTAL METER SURVEYED"].max()*6]},'bar': {'color': '#74c69d'},  # Change this color to match theme
        'bgcolor': "rgba(255,255,255,0.05)",
        'borderwidth': 2,
        'bordercolor': "#1b4332"}
    ))
    
    fig3.update_layout( title=dict(text="Total Meters Surveyed",x=0.5,xanchor='center'),
                       title_font=dict(color='black'),
    paper_bgcolor='white',
    font=dict(color="black"),margin=dict(l=35, r=35, t=40, b=0),height=250)
    
    total_meters = {
    "Mechanical": df["MECHANICAL METER"].sum(),
    "Smart": df["SMART METER"].sum()
    }
    
    fig4 = px.pie(names=list(total_meters.keys()),
                   values=list(total_meters.values()),title='ss',
                    hole=0.4, height=250, color_discrete_sequence=["#40916C", "#1B4332"])
    fig4.update_layout(title=dict(text="Overall Meter Type Composition",x=0.5,xanchor='center'),
                       title_font=dict(color='black'),margin=dict(l=0, r=0, t=60, b=30),
    paper_bgcolor='white', hoverlabel=dict(
    font_size=13,
    font_family="Segoe UI",
    bgcolor="#32483D",
    font_color="white"),
    font=dict(color="black"),legend=dict( orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5,font=dict(color='black'), bgcolor='rgba(0,0,0,0)')
    )
    
    fig5 = px.bar(df, x="REGION", y="FAULTY METER", color="Month",title="FAULTY METER", height=250, color_discrete_sequence=custom_color)
    fig5.update_layout(
        title=dict(
    text="FAULTY METER",
    x=0.5,           # Center the title horizontally
    xanchor='center' # Anchor the title at the center
    ),margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor='white',
    plot_bgcolor='rgba(183,204,194,0)',hoverlabel=dict(
    font_size=13,
    font_family="Segoe UI",
    bgcolor="#32483D",
    font_color="white"),
        font=dict(color="black"), title_font=dict(color='black'), # Title font color
    legend=dict(font=dict(color='black'), bgcolor='rgba(0,0,0,0)'), xaxis=dict(
        tickfont=dict(color='black'),
        title_font=dict(color='black'),
        showgrid=False
    ),
    yaxis=dict(
        tickfont=dict(color='black'),
        title_font=dict(color='black'),
        showgrid=False
    )
    )

    
    # Layout: Left for stat boxes, Right for charts
    left_col, right_col = st.columns([1, 6])  # Adjust width ratio as needed
    
    with left_col:
        
        st.markdown(
            f"""
            <div style="background-color: white;  max-width: 170px; height: 40px; 
            border-radius: 20px; box-shadow: 1px 1px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; 
            text-align: center; margin-top:5px; margin-bottom: 6px; margin-left: 13px; padding-top: 8px; padding-left: 25px;">
                <h3 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-weight :1000; font-size: 11px; color:#2D6A4F;">TOTAL TEAMS</h3>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 105px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 31px; margin-left: 13px; padding-top: 15px;  padding-left: 25px">
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Galfar:  {total_teams['Galfar']}</h5>
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Global:  {total_teams['Global']}</h5>
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Al Tayer:  {total_teams['Al Tayer']}</h5>
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div style="background-color: white; max-width: 170px; height: 40px; 
            border-radius: 20px; box-shadow: 1px 1px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; 
            text-align: center; margin-bottom: 6px; margin-left: 13px; padding-top: 15px; padding-left: 25px;">
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-weight :1000; font-size: 10px; color:#2D6A4F;">TOTAL ENGINEERS</h5>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 105px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 31px; margin-left: 13px; padding-top: 15px; padding-left: 25px">
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Galfar: {total_engineers['Galfar']}</h5>
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Global: {total_engineers['Global']}</h5>
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Al Tayer: {total_engineers['Al Tayer']}</h5>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="background-color: white; max-width: 170px; height: 40px; 
            border-radius: 20px; box-shadow: 1px 1px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; 
            text-align: center; margin-bottom: 6px; margin-left: 13px; padding-top: 15px; padding-left: 25px">
                <h5 style="margin-bottom:0px; font-family: 'Arial',serif; font-weight :1000; white-space: nowrap; color:white; font-size: 10px; color:#2D6A4F;">PROJECT MANAGER</h5>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 105px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 10px; margin-left: 13px; padding-top: 15px; line-height: 1.1; padding-left: 25px">
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap;  color:white; font-size: 14px"> Galfar: {pm['Galfar']}</h5>
                <h5 style="margin-bottom:-8px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Global: {pm['Global']}</h5>
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Al Tayer: {pm['Al Tayer']}</h5>
            </div>
            """,
            unsafe_allow_html=True
        )
        



        
    
    with right_col:
        row1_col1, row1_col2  = st.columns(2)
        row1_col1.plotly_chart(fig1, use_container_width=True)
        row1_col2.plotly_chart(fig2, use_container_width=True)
        
    
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        row2_col1.plotly_chart(fig4, use_container_width=True)
        row2_col2.plotly_chart(fig3, use_container_width=True)
        row2_col3.plotly_chart(fig5, use_container_width=True)
        

  



if __name__ == "__main__":
    run()



















