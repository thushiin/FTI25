import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_charts(df,selected_region):
    custom_colors=[ "#1B4332", "#2D6A4F", "#40916C", "#52B788", "#74C69D", "#95D5B2", "#B7E4C7"]
    custom_color=[ "#245944", "#2D6A4F","#40916C","#52B788","#74C69D","#95D5B2","#B7E4C7","#D8F3DC","#E9FCEB","#F0FFF4","#E0F9E0","#CFF4D2"]
    hover_items = ["Month", "DIRECT SAVINGS"]
    if selected_region == "MCT":
        hover_items.insert(1, "WILAYAT")
    
    fig1 = px.bar(
        df,
        x="Month",
        y="DIRECT SAVINGS",
        color="Month",
        title="DIRECT SAVINGS",
        height=250,
        color_discrete_sequence=custom_color,
        hover_data=hover_items
    )

    fig1.update_layout(
        title=dict(
    text="DIRECT SAVINGS",
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
    
    
    fig2 = px.pie(df, names="REGION", values="ILLEGAL CONNECTION",title="ILLEGAL CONNECTION", hole=0.4, height=250, color_discrete_sequence=['#1B4332'])
    
    fig2.update_traces(
    texttemplate='%{value}',

)
    fig2.update_layout(   title=dict(
        text="ILLEGAL CONNECTION",
        x=0.5,
        xanchor='center'
    ),margin=dict(l=0, r=0, t=60, b=30),
    paper_bgcolor='white',  # optional same background style
    plot_bgcolor='rgba(183,204,194,0)',     # optional
    font=dict(color="black"), hoverlabel=dict(
    font_size=13,
    font_family="Segoe UI",
    bgcolor="#32483D",
    font_color="white"), title_font=dict(color='black'),
    legend=dict( orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5,font=dict(color='black'), bgcolor='rgba(0,0,0,0)'),
    
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
    paper_bgcolor='white',  # optional
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
    
    fig5 = px.bar(df, x="Month", y="FAULTY METER", color="Month",title="FAULTY METER", height=250, color_discrete_sequence=custom_color)
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
    
    # Layout
    row1_col1, row1_col2 = st.columns(2)
    row1_col1.plotly_chart(fig1, use_container_width=True)
    row1_col2.plotly_chart(fig2, use_container_width=True)

    row2_col1, row2_col2, row2_col3 = st.columns(3)
    row2_col1.plotly_chart(fig4, use_container_width=True)
    row2_col2.plotly_chart(fig3, use_container_width=True)
    row2_col3.plotly_chart(fig5, use_container_width=True)

