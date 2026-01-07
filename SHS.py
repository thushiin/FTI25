import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
import base64
from common_charts import plot_charts
from theme import set_theme
import math




def load_data():
    sheet_id = "1lWA-uWBUXzG5iu2ghPEym2SDLhfC3VlDnqBdev9q1H0"  
    sheet_name = "Sheet1"             
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df=pd.read_csv(url)
    return df[df["REGION"] == "SHS"]

def run():
    set_theme()
    st.markdown("<h1 style='text-align: center;'>ASH SHARQIYAH SOUTH</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
    df = load_data()

    col1, col2, col3 = st.columns([ 1, 3, 1])
    # Filter
    months = ["All Months"] + [f"{month} 2025" for month in df["Month"].unique()]
    selected_month = col3.selectbox("📅", months, label_visibility="collapsed")
    
    # Adjust the filter to remove the year when applying the filter to the DataFrame
    if selected_month != "All Months":
        # Remove the " 2025" suffix to match the original data
        filtered_month = selected_month.replace(" 2025", "")
        df = df[df["Month"] == filtered_month]
        

    
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
                <h5 style="margin-bottom:0px; font-family: 'Helvetica', serif; white-space: nowrap; color:white; font-size: 14px"">💧 Total Direct Savings (m&sup3;)</h5>
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
                <h5 style="margin-bottom: 0px; line-height: 1.1; font-family: 'Helvetica', serif; white-space: nowrap; color:white; font-size: 14px">⚠️ Illegal Connections</h5>
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


    
    left_col, right_col = st.columns([1, 6])  # Adjust width ratio as needed
    
    with left_col:
        
        st.markdown(
            f"""
            <div style="background-color: white; max-width: 170px; height: 40px; 
            border-radius: 20px; box-shadow: 1px 1px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; 
            text-align: center; margin-bottom: 6px; margin-left: 13px; padding-top: 8px; padding-left: 25px;">
                <h3 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:#2D6A4F; font-weight :1000; font-size: 11px">TOTAL TEAMS</h3>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 100px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 41px; margin-left: 13px; padding-top: 15px; padding-left: 25px">
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Galfar: 8</h5>
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
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:#2D6A4F; font-weight :1000; font-size: 10px">TOTAL ENGINEERS</h5>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 100px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 41px; margin-left: 13px; padding-top: 15px; padding-left: 25px">
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Galfar: 1</h5>
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
                <h5 style="margin-bottom:0px; font-family: 'Arial',serif; font-weight :1000; white-space: nowrap;  font-size: 10px; color:#2D6A4F;">PROJECT MANAGER</h5>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style="background-color: #2D6A4F; max-width: 170px; height: 100px; 
            border-radius: 12px; box-shadow: 1px 10px 6px rgba(0.3,0.3,0.3,0.3); 
            display: flex; align-items: center; justify-content: center; flex-direction: column; 
            text-align: center; margin-bottom: 10px; margin-left: 13px; padding-top: 15px; padding-left: 25px">
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap;  color:white; font-size: 14px"> Galfar: 0</h5>
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Global: 0</h5>
                <h5 style="margin-bottom:0px; font-family: 'Arial', serif; white-space: nowrap; color:white; font-size: 14px"> Al Tayer: 0</h5>
            </div>
            """,
            unsafe_allow_html=True
        )



        
    
    with right_col:

        # Charts
        plot_charts(df,"SHS")


# Optional: Direct run (for testing)
if __name__ == "__main__":
    run()


