import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pywaffle import Waffle
import plotly.express as px
import pyodbc
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from PIL import Image
import os
import base64


# Check if logo exists and display it
logo_path = "assets/images/logo.png"

if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path)
        # Center layout columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Display logo (larger and centered)
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}"
                         style="width:180px; margin-bottom: 10px;">
                    <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                              font-size: 1.5rem; font-weight: 700; color: #D4AF37; margin-bottom: 3px;">
                        Egypt Employment Analytics
                    </div>
                    <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                              font-size: 0.9rem; color: #8B5CF6; font-weight: 500;">
                        Advanced Labor Market Intelligence
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        # Fallback if image fails to load
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 3rem;">📊</div>
            <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                      font-size: 1.5rem; font-weight: 700; color: #D4AF37;">
                Egypt Employment Analytics
            </div>
            <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                      font-size: 0.9rem; color: #8B5CF6; font-weight: 500;">
                Advanced Labor Market Intelligence
            </div>
            <div style="font-size: 3rem;">🇪🇬</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Fallback if logo file doesn't exist
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 3rem;">📊</div>
        <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                  font-size: 1.5rem; font-weight: 700; color: #D4AF37;">
            Egypt Employment Analytics
        </div>
        <div style="font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                  font-size: 0.9rem; color: #8B5CF6; font-weight: 500;">
            Advanced Labor Market Intelligence
        </div>
        <div style="font-size: 3rem;">🇪🇬</div>
    </div>
    """, unsafe_allow_html=True)
# -------------------------------
# 1️⃣ Connect to SQL Server & Load Data
# -------------------------------
@st.cache_data
def load_data():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost\\SQLEXPRESS;"   
            "Database=Employment_in_Egypt;"
            "Trusted_Connection=yes;"
        )
        
        # Load all datasets
        df_economy = pd.read_sql("SELECT * FROM [dbo].[Economy_And_LifeOfWork]", conn)
        df_economy_age = pd.read_sql("SELECT * FROM [EconomyAndAge_Fact]", conn)
        df_emp_age = pd.read_sql("SELECT * FROM [dbo].[Emp&Age]", conn)
        df_main_jobs = pd.read_sql("SELECT * FROM [dbo].[MainjobsSecAndAge]", conn)
        df_nature_work = pd.read_sql("SELECT * FROM [dbo].[NatureOfWork]", conn)
        df_pop_age = pd.read_sql("SELECT * FROM [dbo].[PopAndAge]", conn)
        df_education = pd.read_sql("SELECT * FROM [dbo].[Educational_Status]", conn)
        df_insurance = pd.read_sql("SELECT * FROM [dbo].[Social_Insurance]", conn)
        df_main_job_sectors = pd.read_sql("SELECT * FROM [dbo].[MainJobAndSectors]", conn)
        df_sector_age = pd.read_sql("SELECT * FROM [dbo].[Sector&Age]", conn)
        
        conn.close()
        
        return {
            'economy': df_economy,
            'economy_age': df_economy_age,
            'emp_age': df_emp_age,
            'main_jobs': df_main_jobs,
            'nature_work': df_nature_work,
            'pop_age': df_pop_age,
            'education': df_education,
            'insurance': df_insurance,
            'main_job_sectors': df_main_job_sectors,
            'sector_age': df_sector_age
        }
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

# Load data
with st.spinner('🔄 Loading data from SQL Server...'):
    data = load_data()

if data is None:
    st.error("🚫 Failed to load data. Please check your database connection.")
    st.stop()

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <h2 style="color: #D4AF37;">🌙 Navigation</h2>
    <div class="custom-badge">Premium Dashboard</div>
</div>
""", unsafe_allow_html=True)

sections = [
    "🏠 Overview",
    "💼 Economy Analysis", 
    "👥 Employment & Age",
    "🎓 Education Analysis",
    "🗺️ Geographical Analysis",
    "🏥 Social Insurance",
    "📊 Summary Report"
]
selected_section = st.sidebar.selectbox("", sections)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #a0aec0; font-size: 0.8rem;">
    <p>🌟 Premium Analytics</p>
    <p>Egypt Employment Insights</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# OVERVIEW SECTION
# -------------------------------
if selected_section == "🏠 Overview":
    st.markdown('<h2 class="section-header">📈 Dataset Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏢 Economy Records", f"{len(data['economy']):,}")
        st.metric("👥 Population Records", f"{len(data['pop_age']):,}")
    
    with col2:
        st.metric("💼 Employment Records", f"{len(data['emp_age']):,}")
        st.metric("🎓 Education Records", f"{len(data['education']):,}")
    
    with col3:
        st.metric("🏥 Insurance Records", f"{len(data['insurance']):,}")
        st.metric("🏭 Sector Records", f"{len(data['sector_age']):,}")
    
    with col4:
        total_records = sum(len(df) for df in data.values())
        st.metric("📊 Total Records", f"{total_records:,}")
        st.metric("🗂️ Datasets", f"{len(data)}")
    
    st.markdown("""
    <div class="luxury-card">
        <h3 style="color: #D4AF37; margin-bottom: 1rem;">🔍 Dataset Explorer</h3>
    """, unsafe_allow_html=True)
    
    dataset_choice = st.selectbox("Select dataset to preview", list(data.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Shape:** {data[dataset_choice].shape[0]:,} rows × {data[dataset_choice].shape[1]} columns")
    with col2:
        st.info(f"**Columns:** {', '.join(data[dataset_choice].columns[:5])}...")
    
    st.dataframe(data[dataset_choice].head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# ECONOMY ANALYSIS SECTION
# -------------------------------
elif selected_section == "💼 Economy Analysis":
    st.markdown('<h2 class="section-header">💼 Economy Type Analysis</h2>', unsafe_allow_html=True)
    
    # Set dark theme for matplotlib
    plt.style.use('dark_background')
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    
    economy_summary = data['economy'].groupby('Economy_Type')['Total'].sum().sort_values(ascending=True)
    
    colors = ['#D4AF37', '#FFD700', '#C9A227', '#B8860B']
    
    bars = ax1.barh(range(len(economy_summary)), economy_summary.values,
                    color=colors * (len(economy_summary) // len(colors) + 1),
                    edgecolor='white', linewidth=0.5)
    
    ax1.set_title("Economy Type Distribution", fontsize=16, fontweight='bold', pad=20, color='white')
    ax1.set_xlabel("Total Count", fontsize=12, fontweight='bold', color='white')
    ax1.set_ylabel("Economy Type", fontsize=12, fontweight='bold', color='white')
    
    labels = [f"{label[:20]}..." if len(label) > 20 else label for label in economy_summary.index]
    ax1.set_yticks(range(len(economy_summary)))
    ax1.set_yticklabels(labels, color='white')
    
    for i, (bar, value) in enumerate(zip(bars, economy_summary.values)):
        ax1.text(bar.get_width() + bar.get_width() * 0.01, 
                 bar.get_y() + bar.get_height()/2, 
                 f'{value:,}', va='center', ha='left', fontsize=10, color='white', fontweight='bold')
    
    ax1.grid(axis='x', alpha=0.3, linestyle='--', color='white')
    plt.tight_layout()
    st.pyplot(fig1)
    
    # Gender Analysis
    if 'Gender_Type' in data['economy'].columns:
        st.markdown("""
        <div class="luxury-card" style="margin-top: 2rem;">
            <h3 style="color: #FFD700; text-align:center; margin-bottom: 0.5rem;">👥 Gender Distribution Analysis</h3>
            <p style="color:#a0aec0; text-align:center;">Visualizing gender participation across economy sectors with clarity & luxury design.</p>
        </div>
        """, unsafe_allow_html=True)

        # Prepare the data
        df_econ = data['economy'].copy()
        df_econ['Economy_Short'] = df_econ['Economy_Type'].apply(
            lambda x: x if len(x) <= 20 else x[:18] + "..."
        )

        col1, col2 = st.columns(2)

        # ======================================
        # Chart 1 — Smoothed Point Plot by Gender
        # ======================================
        with col1:
            st.markdown("""
            <div class="luxury-card" style="padding:1rem; border-left: 3px solid #D4AF37;">
                <h4 style="color:#FFD700;">💼 Economy Type by Gender</h4>
            """, unsafe_allow_html=True)

            plt.style.use('dark_background')
            fig2, ax2 = plt.subplots(figsize=(10, 5))

            sns.pointplot(
                data=df_econ,
                x="Economy_Short", y="Total", hue="Gender_Type",
                palette=['#D4AF37', '#8B5CF6'],
                errorbar=None, markers=['o', 's'], linestyles=['-', '--'], ax=ax2
            )

            ax2.set_title("Economy Type by Gender", fontsize=13, fontweight='bold', color='#FFD700')
            ax2.set_xlabel("", color='white')
            ax2.set_ylabel("Total Count", fontweight='bold', color='white')
            ax2.tick_params(axis='x', rotation=35, labelsize=9, colors='white')
            ax2.tick_params(axis='y', labelsize=9, colors='white')
            ax2.legend(title="Gender", title_fontsize=11, fontsize=9, loc='upper right', frameon=False)
            ax2.grid(alpha=0.2, linestyle='--', color='#555')

            plt.tight_layout()
            st.pyplot(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

        # ======================================
        # Chart 2 — Bar Plot (Average by Gender)
        # ======================================
        with col2:
            st.markdown("""
            <div class="luxury-card" style="padding:1rem; border-left: 3px solid #8B5CF6;">
                <h4 style="color:#FFD700;">📊 Average Distribution by Gender</h4>
            """, unsafe_allow_html=True)

            plt.style.use('dark_background')
            fig3, ax3 = plt.subplots(figsize=(10, 5))

            pivot_data = (
                df_econ
                .pivot_table(index="Economy_Short", columns="Gender_Type", values="Total", aggfunc='mean')
                .fillna(0)
            )

            pivot_data.plot(
                kind='bar', ax=ax3,
                color=['#D4AF37', '#8B5CF6'],
                edgecolor='white', linewidth=0.6
            )

            ax3.set_title("Average Distribution by Gender", fontsize=13, fontweight='bold', color='#FFD700')
            ax3.set_xlabel("", color='white')
            ax3.set_ylabel("Average Count", fontweight='bold', color='white')
            ax3.tick_params(axis='x', rotation=35, labelsize=9, colors='white')
            ax3.tick_params(axis='y', labelsize=9, colors='white')
            ax3.legend(title="Gender", title_fontsize=11, fontsize=9, loc='upper right', frameon=False)
            ax3.grid(axis='y', alpha=0.2, linestyle='--', color='#555')

            plt.tight_layout()
            st.pyplot(fig3)
            st.markdown("</div>", unsafe_allow_html=True)
    
    

# -------------------------------
# EMPLOYMENT & AGE SECTION
# -------------------------------
elif selected_section == "👥 Employment & Age":
    st.markdown('<h2 class="section-header">👥 Employment & Age Analysis</h2>', unsafe_allow_html=True)
    
    # Nature of Work Waffle Chart
    if "Employment_Type_Name" in data['nature_work'].columns:
        st.markdown("""
        <div class="luxury-card">
            <h3 style="color: #D4AF37; margin-bottom: 1rem;">🧇 Nature of Work Distribution</h3>
        """, unsafe_allow_html=True)
        
        work_nature_counts = (
            data['nature_work'].groupby("Employment_Type_Name")["Total"]
            .sum()
            .sort_values(ascending=False)
        )
        total_tiles = 100
        proportions = (work_nature_counts / work_nature_counts.sum() * total_tiles).round().astype(int)

        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=proportions.to_dict(),
            figsize=(10, 6),
            colors=["#D4AF37", "#8B5CF6", "#10B981", "#EF4444"],
            title={"label": "Nature of Work Distribution", "loc": "center", "color": "white"}
        )
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Job Distribution Heatmap
    if 'Occupation_Type' in data['main_jobs'].columns and 'Age_Range' in data['main_jobs'].columns:
        st.markdown("""
        <div class="luxury-card">
            <h3 style="color: #D4AF37; margin-bottom: 1rem;">🔥 Job Distribution Heatmap</h3>
        """, unsafe_allow_html=True)
        
        jobs_pivot = data['main_jobs'].pivot_table(index="Occupation_Type", columns="Age_Range", 
                                                 values="Total", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.style.use('dark_background')
        sns.heatmap(jobs_pivot, cmap="YlOrRd", annot=True, fmt=".0f", cbar_kws={'label': 'Total'}, ax=ax)
        ax.set_title("Job Distribution by Occupation Type and Age Range", color='white', fontweight='bold')
        ax.set_xlabel("Age Range", color='white', fontweight='bold')
        ax.set_ylabel("Occupation Type", color='white', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Population & Age Analysis
    st.markdown("""
    <div class="luxury-card">
        <h3 style="color: #D4AF37; margin-bottom: 1rem;">📊 Population & Age Analysis</h3>
    """, unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.style.use('dark_background')
    
    if 'Gender_Type' in data['pop_age'].columns:
        pop_pivot = data['pop_age'].groupby(["Age_Range","Gender_Type"])["Total"].sum().unstack(fill_value=0)
        pop_pivot.plot(kind="bar", stacked=True, ax=ax, width=0.8, color=['#D4AF37', '#8B5CF6'])
        ax.set_title("Population Distribution by Age Range and Gender", color='white', fontweight='bold')
        ax.set_xlabel("Age Range", color='white', fontweight='bold')
        ax.set_ylabel("Total Population", color='white', fontweight='bold')
        ax.legend(title="Gender", title_fontsize=12, fontsize=10)
    else:
        age_summary = data['pop_age'].groupby('Age_Range')['Total'].sum()
        ax.bar(range(len(age_summary)), age_summary.values, color='#D4AF37', alpha=0.7)
        ax.set_title("Population Distribution by Age Range", color='white', fontweight='bold')
        ax.set_xlabel("Age Range", color='white', fontweight='bold')
        ax.set_ylabel("Total Population", color='white', fontweight='bold')
        ax.set_xticks(range(len(age_summary)))
        ax.set_xticklabels(age_summary.index, rotation=45, color='white')
    
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 🎓 EDUCATION ANALYSIS SECTION
# -------------------------------
elif selected_section == "🎓 Education Analysis":
    st.markdown('<h2 class="section-header">🎓 Educational Status Analysis</h2>', unsafe_allow_html=True)

    # --- Intro & Description ---
    st.markdown("""
    <div class="luxury-card" style="padding: 1rem 1.5rem;">
        <h3 style="color: #D4AF37; margin-bottom: 0.5rem;">📚 Educational Status Distribution</h3>
        <p style="color: #a0aec0; margin-top: 0;">Explore Egypt’s education levels by status, gender, and region to reveal development trends.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Layout Columns ---
    col1, col2 = st.columns([1.1, 1])

    # --- Pie Chart: Educational Status Distribution ---
    with col1:
        edu_counts = data['education'].groupby("Status")["Total"].sum().sort_values(ascending=False)
        luxury_colors = ['#D4AF37', '#8B5CF6', '#10B981', '#EF4444', '#3B82F6']

        fig1, ax1 = plt.subplots(figsize=(8, 8))
        plt.style.use('dark_background')

        wedges, texts, autotexts = ax1.pie(
            edu_counts.values,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=luxury_colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.2}
        )

        # Text style improvements
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        for text in texts:
            text.set_color('#E0E0E0')

        ax1.set_title("Educational Status Breakdown", fontsize=16, fontweight='bold', color='#FFD700')
        ax1.legend(
            edu_counts.index,
            title="Status",
            title_fontsize=12,
            fontsize=10,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        plt.tight_layout()
        st.pyplot(fig1)

    # --- Bar Chart: Status by Gender ---
    with col2:
        if 'Gender_Type' in data['education'].columns:
            plt.style.use('dark_background')
            fig2, ax2 = plt.subplots(figsize=(9, 7))

            sns.barplot(
                data=data['education'],
                x="Status", y="Total", hue="Gender_Type",
                palette=['#D4AF37', '#8B5CF6'],
                edgecolor='white', linewidth=0.6, ax=ax2
            )

            ax2.set_title("Educational Status by Gender", fontsize=16, fontweight='bold', color='#FFD700')
            ax2.set_xlabel("Educational Status", fontweight='bold', color='white')
            ax2.set_ylabel("Total Count", fontweight='bold', color='white')
            ax2.tick_params(axis='x', rotation=40, labelcolor='white')
            ax2.tick_params(axis='y', labelcolor='white')
            ax2.legend(title="Gender", title_fontsize=12, fontsize=10)

            plt.tight_layout()
            st.pyplot(fig2)

    # --- Insights Cards ---
    total_students = data['education']["Total"].sum()
    top_status = edu_counts.idxmax()
    top_value = edu_counts.max()
    top_ratio = (top_value / total_students) * 100

    st.markdown("""
    <div class="luxury-card" style="margin-top: 1.5rem; text-align:center;">
        <h3 style="color: #D4AF37;">📊 Key Insights</h3>
    </div>
    """, unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #D4AF37;">
            <h4 style="color:#FFD700;">Top Educational Status</h4>
            <p style="color:white; font-size:1.1rem;"><b>{top_status}</b></p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #8B5CF6;">
            <h4 style="color:#8B5CF6;">Highest Share</h4>
            <p style="color:white; font-size:1.1rem;"><b>{top_ratio:.1f}%</b> of total</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #10B981;">
            <h4 style="color:#10B981;">Total Recorded</h4>
            <p style="color:white; font-size:1.1rem;"><b>{total_students:,.0f}</b></p>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div style="margin-top: 2rem; text-align:center; color:#a0aec0;">
        <em>This educational breakdown highlights Egypt’s learning progress across gender and qualification levels.</em>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# GEOGRAPHICAL ANALYSIS SECTION
# -------------------------------
elif selected_section == "🗺️ Geographical Analysis":
    st.markdown('<h2 class="section-header">🗺️ Geographical Distribution</h2>', unsafe_allow_html=True)

    map_type = st.selectbox(
        "Select Map Type",
        ["Education Distribution", "Population Heatmap", "Employment Heatmap"]
    )

    # Governorate coordinates
    governorate_coords = {
        'CAIRO': {'lat': 30.0444, 'lon': 31.2357},
        'ALEXANDRIA': {'lat': 31.2001, 'lon': 29.9187},
        'GIZA': {'lat': 30.0131, 'lon': 31.2089},
        'DAKAHLIA': {'lat': 31.0409, 'lon': 31.3785},
        'BEHEIRA': {'lat': 31.0424, 'lon': 30.4712},
        'QALYUBIA': {'lat': 30.4167, 'lon': 31.2167},
        'MENOUFIA': {'lat': 30.4659, 'lon': 30.9309},
        'SHARKIA': {'lat': 30.5877, 'lon': 31.5021},
        'GHARBIA': {'lat': 30.7865, 'lon': 30.9955},
        'KAFR EL SHEIKH': {'lat': 31.1117, 'lon': 30.9394},
        'DAMIETTA': {'lat': 31.4165, 'lon': 31.8133},
        'PORT SAID': {'lat': 31.2653, 'lon': 32.3019},
        'ISMAILIA': {'lat': 30.5965, 'lon': 32.2715},
        'SUEZ': {'lat': 29.9668, 'lon': 32.5498},
        'NORTH SINAI': {'lat': 31.1300, 'lon': 33.8000},
        'SOUTH SINAI': {'lat': 28.5390, 'lon': 33.9750},
        'BANI SUEF': {'lat': 29.0667, 'lon': 31.0833},
        'FAIYUM': {'lat': 29.3084, 'lon': 30.8428},
        'MINYA': {'lat': 28.0871, 'lon': 30.7618},
        'ASIUT': {'lat': 27.1809, 'lon': 31.1837},
        'SOHAG': {'lat': 26.5560, 'lon': 31.6948},
        'QENA': {'lat': 26.1642, 'lon': 32.7267},
        'LUXOR': {'lat': 25.6872, 'lon': 32.6396},
        'ASWAN': {'lat': 24.0889, 'lon': 32.8998},
        'RED SEA': {'lat': 26.5560, 'lon': 33.9667},
        'NEW VALLEY': {'lat': 25.4439, 'lon': 28.9229},
        'MATROUH': {'lat': 31.3525, 'lon': 27.2373}
    }

    # Define dataset and visual style dynamically
    if map_type == "Education Distribution":
        title = "🎓 Education Distribution Map"
        dataset = data['education']
        color = "#D4AF37"
        use_heatmap = False
    elif map_type == "Population Heatmap":
        title = "🔥 Population Heatmap"
        dataset = data['pop_age']
        color = "#FF4500"
        use_heatmap = True
    else:
        title = "💼 Employment Heatmap"
        dataset = data['emp_age']
        color = "#FFD700"
        use_heatmap = True

    st.markdown(f"""
    <div class="luxury-card">
        <h3 style="color: #D4AF37; margin-bottom: 1rem;">{title}</h3>
    </div>
    """, unsafe_allow_html=True)

    # Prepare data
    df_governorates = dataset.groupby('Governorate')['Total'].sum().reset_index()
    df_governorates['Governorate_upper'] = df_governorates['Governorate'].str.upper()
    df_governorates['lat'] = df_governorates['Governorate_upper'].map(lambda x: governorate_coords.get(x, {}).get('lat'))
    df_governorates['lon'] = df_governorates['Governorate_upper'].map(lambda x: governorate_coords.get(x, {}).get('lon'))
    df_governorates = df_governorates.dropna(subset=['lat', 'lon'])

    # Create map
    mymap = folium.Map(location=[26.8206, 30.8025], zoom_start=6, tiles="CartoDB positron")

    if use_heatmap:
        heat_data = [
            [row['lat'], row['lon'], float(row['Total'])]
            for _, row in df_governorates.iterrows()
            if not pd.isna(row['lat']) and not pd.isna(row['lon'])
        ]
        HeatMap(heat_data, min_opacity=0.3, radius=25, blur=20, max_zoom=6).add_to(mymap)
    else:
        for _, row in df_governorates.iterrows():
            try:
                total_value = float(row['Total'])
                if total_value > 0:
                    radius = max(total_value / 50000, 5)
                    folium.CircleMarker(
                        location=[row['lat'], row['lon']],
                        radius=radius,
                        popup=f"<b>{row['Governorate']}</b><br>Total: {total_value:,.0f}",
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.6,
                        tooltip=row['Governorate']
                    ).add_to(mymap)
            except (ValueError, TypeError):
                continue

    # Display map and data side-by-side
    col1, col2 = st.columns([2, 1])
    with col1:
        st_folium(mymap, width=750, height=500)

    with col2:
        st.markdown("### 🧾 Top 5 Governorates")
        top5 = df_governorates.nlargest(5, 'Total')[['Governorate', 'Total']]
        st.dataframe(top5.style.format({'Total': '{:,.0f}'}).set_properties(**{
            'background-color': '#1a1a1a', 'color': '#FFD700'
        }))

    st.markdown("""
    <div style="margin-top: 1.5rem; text-align:center; color:#a0aec0;">
        <em>Geographical analysis visualizes Egypt’s regional differences and development indicators.</em>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# SOCIAL INSURANCE SECTION
# -------------------------------
elif selected_section == "🏥 Social Insurance":
    st.markdown('<h2 class="section-header">🏥 Social Insurance Analysis</h2>', unsafe_allow_html=True)
    
    if 'Insurance_Type' in data['insurance'].columns:
        st.markdown("""
        <div class="luxury-card">
            <h3 style="color: #D4AF37; margin-bottom: 1rem;">🛡️ Social Insurance Coverage</h3>
        """, unsafe_allow_html=True)
        
        fig = px.pie(data['insurance'], names="Insurance_Type", values="Total",
                    title="Social Insurance Coverage Distribution",
                    color_discrete_sequence=['#D4AF37', '#8B5CF6', '#10B981', '#EF4444'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if 'Occupation_Type' in data['main_job_sectors'].columns:
        st.markdown("""
        <div class="luxury-card">
            <h3 style="color: #D4AF37; margin-bottom: 1rem;">💼 Employment by Job Sector</h3>
        """, unsafe_allow_html=True)
        
        sector_summary = data['main_job_sectors'].groupby('Occupation_Type')['Total'].sum().reset_index()
        fig = px.bar(sector_summary, x='Occupation_Type', y='Total',
                    title="Employment by Job Sector",
                    color_discrete_sequence=['#D4AF37'])
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if all(col in data['sector_age'].columns for col in ['Sector_Name', 'Age_Range', 'Gender_Type']):
        st.markdown("""
        <div class="luxury-card">
            <h3 style="color: #D4AF37; margin-bottom: 1rem;">🌐 Sector, Age & Gender Hierarchy</h3>
        """, unsafe_allow_html=True)
        
        fig = px.sunburst(data['sector_age'], path=["Sector_Name", "Age_Range", "Gender_Type"], 
                         values="Total", title="Sector, Age & Gender Hierarchy")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# SUMMARY SECTION
# -------------------------------
elif selected_section == "📊 Summary Report":
    st.markdown('<h2 class="section-header">📋 Analysis Summary</h2>', unsafe_allow_html=True)
    
    try:
        economy_total = data['economy']['Total'].sum() if 'economy' in data and 'Total' in data['economy'].columns else 0
        pop_total = data['pop_age']['Total'].sum() if 'pop_age' in data and 'Total' in data['pop_age'].columns else 0
        emp_total = data['emp_age']['Total'].sum() if 'emp_age' in data and 'Total' in data['emp_age'].columns else 0
        edu_total = data['education']['Total'].sum() if 'education' in data and 'Total' in data['education'].columns else 0
        insurance_total = data['insurance']['Total'].sum() if 'insurance' in data and 'Total' in data['insurance'].columns else 0
        
        economy_records = len(data['economy']) if 'economy' in data else 0
    except (KeyError, AttributeError, TypeError) as e:
        st.error(f"Error calculating summary statistics: {e}")
        economy_total = pop_total = emp_total = edu_total = insurance_total = 0
        economy_records = 0

    html_summary = f"""
    <div style="background-color: rgba(20, 20, 20, 0.95); padding: 2rem; border-radius: 10px;">
        <h3 style="color: #D4AF37; margin-bottom: 2rem;">📊 EMPLOYMENT IN EGYPT - ANALYSIS SUMMARY</h3>
        
        <div style="color: #a0aec0; line-height: 2.5;">
            <h4 style="color: #D4AF37;">🏢 ECONOMY & WORK:</h4>
            <p>• Total records in Economy dataset: <strong style="color: #FFD700;">{economy_records:,}</strong></p>
            <p>• Total employment figure: <strong style="color: #FFD700;">{economy_total:,}</strong></p>
            
            <h4 style="color: #D4AF37;">👥 DEMOGRAPHICS:</h4>
            <p>• Total population analyzed: <strong style="color: #FFD700;">{pop_total:,}</strong></p>
            
            <h4 style="color: #D4AF37;">💼 EMPLOYMENT:</h4>
            <p>• Total employment records: <strong style="color: #FFD700;">{emp_total:,}</strong></p>
            
            <h4 style="color: #D4AF37;">🎓 EDUCATION:</h4>
            <p>• Educational status records: <strong style="color: #FFD700;">{edu_total:,}</strong></p>
            
            <h4 style="color: #D4AF37;">🏥 SOCIAL INSURANCE:</h4>
            <p>• Insurance coverage records: <strong style="color: #FFD700;">{insurance_total:,}</strong></p>
        </div>
        
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(212, 175, 55, 0.1); border-radius: 8px; border-left: 4px solid #D4AF37;">
            <h4 style="color: #D4AF37; margin: 0;">✅ Analysis Complete!</h4>
            <p style="margin: 0.5rem 0 0 0; color: #a0aec0;">All visualizations show employment patterns, demographics, and economic indicators for Egypt.</p>
        </div>
    </div>
    """

    # ✅ Render properly as HTML
    components.html(html_summary, height=600, scrolling=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <p style="color: #D4AF37; font-size: 1.1rem; font-weight: 600;">🌟 Egypt Employment Analysis Dashboard</p>
    <p style="color: #a0aec0; font-size: 0.9rem;">Premium Analytics Platform • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)