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
import matplotlib.colors as mcolors


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
# 💼 ECONOMY ANALYSIS SECTION
# -------------------------------
elif selected_section == "💼 Economy Analysis":
    st.markdown('<h2 class="section-header">💼 Economy Type Analysis</h2>', unsafe_allow_html=True)

    # --- Intro Card ---
    st.markdown("""
    <div class="luxury-card" style="padding: 1rem 1.5rem;">
        <h3 style="color: #D4AF37; margin-bottom: 0.5rem;">📈 Economic Activity Overview</h3>
        <p style="color: #a0aec0; margin-top: 0;">Explore Egypt’s economic landscape, segmented by activity type and gender, to understand participation and distribution.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Color Palette ---
    luxury_colors = ['#D4AF37', '#8B5CF6', '#10B981', '#EF4444', '#3B82F6', '#F97316', '#EC4899']
    gender_colors = ['#D4AF37', '#8B5CF6'] # Gold & Purple
    male_color = '#3B82F6'
    female_color = '#EC4899'
    
    plt.style.use('dark_background')
    
    # --- Data Pre-computation ---
    if 'economy' in data and not data['economy'].empty:
        econ_data = data['economy'].copy()
        
        # Ensure 'Total' is numeric
        econ_data['Total'] = pd.to_numeric(econ_data['Total'], errors='coerce')
        econ_data = econ_data.dropna(subset=['Total'])
        
        # Create short labels for charts
        econ_data['Economy_Short'] = econ_data['Economy_Type'].apply(
            lambda x: x if len(x) <= 25 else x[:23] + "..."
        )

        # Aggregations
        econ_counts = econ_data.groupby("Economy_Short")["Total"].sum().sort_values(ascending=False)
        gender_counts = econ_data.groupby("Gender_Type")["Total"].sum()
        
        # --- Row 1: Overall Status & Gender Breakdown ---
        col1, col2 = st.columns(2)

        # --- Chart 1: Donut Chart (Economy Type) ---
        with col1:
            # Use top 7 for pie chart, group others
            if len(econ_counts) > 7:
                pie_data = econ_counts.nlargest(6)
                pie_data['Others'] = econ_counts.nsmallest(len(econ_counts) - 6).sum()
            else:
                pie_data = econ_counts
                
            fig1, ax1 = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax1.pie(
                pie_data.values,
                autopct='%1.1f%%',
                startangle=90,
                colors=luxury_colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.2, 'width': 0.4}
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax1.set_title("Economy Type Distribution (Top 6 + Others)", fontsize=16, fontweight='bold', color='#FFD700')
            ax1.legend(wedges, pie_data.index,
                       title="Economy Type",
                       title_fontsize=12,
                       fontsize=10,
                       loc="center left",
                       bbox_to_anchor=(0.95, 0.5))
            st.pyplot(fig1)

        # --- Chart 2: Donut Chart (Gender Distribution) ---
        with col2:
            plt.style.use('dark_background')
            fig2, ax2 = plt.subplots(figsize=(8, 8))

            # Donut chart with smoother edges and balanced layout
            wedges, texts, autotexts = ax2.pie(
                gender_counts.values,
                labels=None,  # hide raw labels, we’ll handle them manually
                autopct='%1.1f%%',
                startangle=90,
                colors=gender_colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.2, 'width': 0.35},
                textprops={'color': 'white', 'fontweight': 'bold', 'fontsize': 12}
            )

            # Improve percentage text style
            for autotext in autotexts:
                autotext.set_color("#FFFFFF")  # black text on colored wedges
                autotext.set_fontweight('bold')
                autotext.set_fontsize(12)

            # Add category labels (around the donut, clearer than overlapping)
            for i, (label, wedge) in enumerate(zip(gender_counts.index, wedges)):
                angle = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
                x = np.cos(np.deg2rad(angle))
                y = np.sin(np.deg2rad(angle))
                ax2.text(
                    1.25 * x, 1.25 * y, label,
                    ha='center', va='center',
                    fontsize=13, fontweight='bold',
                    color='#FFD700'
                )

            # Add a nice center label showing total
            total = gender_counts.sum()
            ax2.text(
                0, 0, f"Total\n{total:,}",
                ha='center', va='center',
                fontsize=15, fontweight='bold',
                color='#D4AF37'
            )

            # Title
            ax2.set_title(
                "Overall Gender Distribution in Economy",
                fontsize=16, fontweight='bold',
                color='#FFD700', pad=25
            )

            # Add legend for clarity
            ax2.legend(
                gender_counts.index,
                title="Gender",
                title_fontsize=12,
                fontsize=10,
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )

            plt.tight_layout()
            st.pyplot(fig2)


        # --- Row 2: Status by Gender ---
        st.markdown("---")
        
        # --- Chart 3: Bar Chart by Gender ---
        if 'Gender_Type' in econ_data.columns:
            fig3, ax3 = plt.subplots(figsize=(12, 7))
            
            # Use the sorted order from econ_counts
            status_order = econ_counts.index
            
            sns.barplot(
                data=econ_data,
                x="Economy_Short", y="Total", hue="Gender_Type",
                palette=gender_colors,
                edgecolor='white', linewidth=0.6, ax=ax3,
                order=status_order
            )
            ax3.set_title("Total Count by Economy Type & Gender", fontsize=18, fontweight='bold', color='#FFD700')
            ax3.set_xlabel("Economy Type", fontweight='bold', color='white', fontsize=12)
            ax3.set_ylabel("Total Count", fontweight='bold', color='white', fontsize=12)
            ax3.tick_params(axis='x', rotation=45, labelcolor='white', labelsize=10)
            ax3.tick_params(axis='y', labelcolor='white')
            ax3.legend(title="Gender", title_fontsize=12, fontsize=10)
            st.pyplot(fig3, use_container_width=True)

        # --- Row 3: Top Statuses by Gender ---
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        # --- Chart 4: Top 5 Economy Types for Males ---
        with col3:
            male_data = econ_data[econ_data['Gender_Type'] == 'Male']
            male_status = male_data.groupby('Economy_Short')['Total'].sum().nlargest(5).sort_values()
            
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x=male_status.values, y=male_status.index,
                palette=[male_color] * len(male_status),
                ax=ax4, edgecolor='white', linewidth=0.7
            )
            ax4.set_title("Top 5 Economy Types (Male)", fontsize=16, fontweight='bold', color='#FFD700')
            ax4.set_xlabel("Total Count", fontweight='bold', color='white')
            ax4.set_ylabel("Economy Type", fontweight='bold', color='white')
            ax4.tick_params(colors='white')
            # Add value labels
            for i, v in enumerate(male_status.values):
                ax4.text(v + (male_status.values.max() * 0.01), i, f'{v:,.0f}', color='white', va='center')
            st.pyplot(fig4)

        # --- Chart 5: Top 5 Economy Types for Females ---
        with col4:
            female_data = econ_data[econ_data['Gender_Type'] == 'Female']
            female_status = female_data.groupby('Economy_Short')['Total'].sum().nlargest(5).sort_values()
            
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x=female_status.values, y=female_status.index,
                palette=[female_color] * len(female_status),
                ax=ax5, edgecolor='white', linewidth=0.7
            )
            ax5.set_title("Top 5 Economy Types (Female)", fontsize=16, fontweight='bold', color='#FFD700')
            ax5.set_xlabel("Total Count", fontweight='bold', color='white')
            ax5.set_ylabel("Economy Type", fontweight='bold', color='white')
            ax5.tick_params(colors='white')
            # Add value labels
            for i, v in enumerate(female_status.values):
                ax5.text(v + (female_status.values.max() * 0.01), i, f'{v:,.0f}', color='white', va='center')
            st.pyplot(fig5)

        # --- Row 4: Gender Proportions ---
        st.markdown("---")

        # --- Chart 6: 100% Stacked Bar - Gender Percentage by Economy Type ---
        if 'Gender_Type' in econ_data.columns:
            # Pivot data
            pivot_df = econ_data.pivot_table(index='Economy_Short', columns='Gender_Type', values='Total', aggfunc='sum').fillna(0)
            
            # Add total sum and sort
            pivot_df['Total_Sum'] = pivot_df.sum(axis=1)
            pivot_df = pivot_df.sort_values('Total_Sum', ascending=False)
            
            # Calculate percentage
            pivot_df_percent = pivot_df[['Male', 'Female']].divide(pivot_df['Total_Sum'], axis=0)
            
            fig6, ax6 = plt.subplots(figsize=(12, 7))
            pivot_df_percent.plot(
                kind='bar',
                stacked=True,
                ax=ax6,
                color=gender_colors,
                edgecolor='white',
                linewidth=0.5
            )
            ax6.set_title("Gender Percentage by Economy Type", fontsize=18, fontweight='bold', color='#FFD700')
            ax6.set_xlabel("Economy Type", fontweight='bold', color='white', fontsize=12)
            ax6.set_ylabel("Percentage", fontweight='bold', color='white', fontsize=12)
            ax6.legend(title="Gender", title_fontsize=11, fontsize=9, loc='center left', bbox_to_anchor=(1, 0.5))
            ax6.tick_params(axis='x', rotation=45, labelcolor='white')
            ax6.tick_params(axis='y', labelcolor='white')
            ax6.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            
            st.pyplot(fig6, use_container_width=True)

        # --- Insights Cards ---
        total_count = econ_data["Total"].sum()
        top_econ_type = econ_counts.idxmax()
        top_gender = gender_counts.idxmax()
        num_econ_types = len(econ_counts)

        st.markdown("""
        <div class="luxury-card" style="margin-top: 1.5rem; text-align:center;">
            <h3 style="color: #D4AF37;">📊 Key Insights</h3>
        </div>
        """, unsafe_allow_html=True)

        colA, colB, colC, colD = st.columns(4)
        with colA:
            st.markdown(f"""
            <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #D4AF37; height: 100%;">
                <h4 style="color:#FFD700;">Top Economy Type</h4>
                <p style="color:white; font-size:1.1rem;"><b>{top_econ_type}</b></p>
            </div>
            """, unsafe_allow_html=True)
        with colB:
            st.markdown(f"""
            <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #8B5CF6; height: 100%;">
                <h4 style="color:#8B5CF6;">Dominant Gender</h4>
                <p style="color:white; font-size:1.1rem;"><b>{top_gender}</b></p>
            </div>
            """, unsafe_allow_html=True)
        with colC:
            st.markdown(f"""
            <div class-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #10B981; height: 100%;">
                <h4 style="color:#10B981;">Economy Types</h4>
                <p style="color:white; font-size:1.1rem;"><b>{num_econ_types}</b> Categories</p>
            </div>
            """, unsafe_allow_html=True)
        with colD:
            st.markdown(f"""
            <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #EF4444; height: 100%;">
                <h4 style="color:#EF4444;">Total Recorded</h4>
                <p style="color:white; font-size:1.1rem;"><b>{total_count:,.0f}</b></p>
            </div>
            """, unsafe_allow_html=True)

        # --- Footer ---
        st.markdown("""
        <div style="margin-top: 2rem; text-align:center; color:#a0aec0;">
            <em>This economic analysis provides a detailed breakdown of activity by type and gender.</em>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("Economy data could not be loaded. Please check the data source.")
    

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

    # --- Intro Card ---
    st.markdown("""
    <div class="luxury-card" style="padding: 1rem 1.5rem;">
        <h3 style="color: #D4AF37; margin-bottom: 0.5rem;">📚 Comprehensive Educational Analysis</h3>
        <p style="color: #a0aec0; margin-top: 0;">Deep dive into Egypt's education landscape with multi-dimensional insights across status, gender, regions, and time.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Color Palette ---
    luxury_colors = ['#D4AF37', '#8B5CF6', '#10B981', '#EF4444', '#3B82F6', '#F59E0B', '#EC4899', '#06B6D4', '#84CC16']
    plt.style.use('dark_background')

    # --- Data Preparation ---
    # Create education level mapping
    education_mapping = {
        'Illiterate': 'Basic Literacy',
        'Literate (can read and write without formal qualification)': 'Basic Literacy', 
        'Literacy certificate (post-illiteracy program)': 'Basic Literacy',
        'Primary school': 'Primary',
        'Preparatory school (Middle school)': 'Preparatory',
        'General Secondary / Azhar Secondary': 'Secondary',
        'Intermediate Technical Qualification': 'Technical',
        'Above Intermediate Qualification (Diploma)': 'Diploma',
        'University Degree (Bachelor\'s)': 'University',
        'Higher Diploma': 'Postgraduate',
        'Master\'s Degree': 'Postgraduate',
        'Doctorate (PhD)': 'Postgraduate',
        'Intellectual Education (special education)': 'Special Education'
    }
    
    # Apply mapping and ensure all categories exist
    data['education']['Education_Level'] = data['education']['Status'].map(education_mapping)
    
    # Define all possible education levels
    all_education_levels = [
        'Basic Literacy', 'Primary', 'Preparatory', 'Secondary', 
        'Technical', 'Diploma', 'University', 'Postgraduate', 'Special Education'
    ]

    # --- Chart 1: Enhanced Pie Chart with Education Levels ---
    col1, col2 = st.columns([1, 1])
    with col1:
        level_counts = data['education'].groupby("Education_Level")["Total"].sum().reindex(all_education_levels, fill_value=0)
        level_counts = level_counts[level_counts > 0]  # Remove zero counts
        
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax1.pie(
            level_counts.values,
            autopct='%1.1f%%',
            startangle=90,
            colors=luxury_colors[:len(level_counts)],
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.2}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax1.set_title("Education Level Distribution", fontsize=16, fontweight='bold', color='#FFD700')
        ax1.legend(level_counts.index, title="Education Level", title_fontsize=10, fontsize=9, 
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig1)

    # --- Chart 2: Gender Distribution by Education Level ---
    with col2:
        gender_level = data['education'].pivot_table(
            index='Education_Level', columns='Gender_Type', values='Total', aggfunc='sum'
        ).reindex(all_education_levels, fill_value=0)
        
        # Remove rows with zero totals
        gender_level = gender_level[(gender_level.sum(axis=1) > 0)]
        
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        gender_level.plot(kind='bar', ax=ax2, color=['#D4AF37', '#8B5CF6'], edgecolor='white', linewidth=0.6)
        ax2.set_title("Education Level Distribution by Gender", fontsize=16, fontweight='bold', color='#FFD700')
        ax2.set_xlabel("Education Level", fontweight='bold', color='white')
        ax2.set_ylabel("Total Count", fontweight='bold', color='white')
        ax2.tick_params(axis='x', rotation=45, labelcolor='white')
        ax2.tick_params(axis='y', labelcolor='white')
        ax2.legend(title="Gender", title_fontsize=12, fontsize=10)
        ax2.grid(axis='y', alpha=0.3, color='gray')
        st.pyplot(fig2)

    # --- Chart 3: Literacy Rate by Governorate ---
    st.markdown("### 📊 Regional Analysis")
    col3, col4 = st.columns([1, 1])
    
    with col3:
        # Create pivot table with all education levels
        gov_data = data['education'].pivot_table(
            index='Governorate', columns='Education_Level', values='Total', aggfunc='sum'
        ).reindex(columns=all_education_levels, fill_value=0)
        
        gov_data['Total_Population'] = gov_data.sum(axis=1)
        gov_data['Literacy_Rate'] = (1 - (gov_data['Basic Literacy'] / gov_data['Total_Population'])) * 100
        
        top_literacy = gov_data.nlargest(10, 'Literacy_Rate')['Literacy_Rate']
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_literacy.values, y=top_literacy.index, palette=['#10B981'] * len(top_literacy),
                   ax=ax3, edgecolor='white', linewidth=0.7)
        ax3.set_title("Top 10 Governorates by Literacy Rate (%)", fontsize=14, fontweight='bold', color='#FFD700')
        ax3.set_xlabel("Literacy Rate (%)", fontweight='bold', color='white')
        ax3.set_ylabel("Governorate", fontweight='bold', color='white')
        ax3.tick_params(colors='white')
        st.pyplot(fig3)

    # --- Chart 4: Higher Education Concentration ---
    with col4:
        # Safely calculate higher education (handle missing columns)
        higher_edu_columns = [col for col in ['University', 'Postgraduate'] if col in gov_data.columns]
        if higher_edu_columns:
            higher_edu = gov_data[higher_edu_columns].sum(axis=1)
        else:
            higher_edu = gov_data['Total_Population'] * 0  # Fallback if no higher education data
            
        top_higher_edu = higher_edu.nlargest(10)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_higher_edu.values, y=top_higher_edu.index, palette=['#8B5CF6'] * len(top_higher_edu),
                   ax=ax4, edgecolor='white', linewidth=0.7)
        ax4.set_title("Top 10 Governorates - Higher Education Population", fontsize=14, fontweight='bold', color='#FFD700')
        ax4.set_xlabel("University & Postgraduate Students", fontweight='bold', color='white')
        ax4.set_ylabel("Governorate", fontweight='bold', color='white')
        ax4.tick_params(colors='white')
        st.pyplot(fig4)

    # --- Chart 5: Gender Gap in Education ---
    st.markdown("### ⚖️ Gender Parity Analysis")
    col5, col6 = st.columns([1, 1])
    
    with col5:
        gender_gap = data['education'].pivot_table(
            index='Education_Level', columns='Gender_Type', values='Total', aggfunc='sum'
        ).reindex(all_education_levels, fill_value=0)
        
        # Calculate ratio only where both genders have data
        gender_gap['Gender_Ratio'] = 0
        mask = (gender_gap['Male'] > 0) & (gender_gap['Female'] > 0)
        gender_gap.loc[mask, 'Gender_Ratio'] = (gender_gap.loc[mask, 'Female'] / gender_gap.loc[mask, 'Male']) * 100
        
        gender_gap = gender_gap[gender_gap.sum(axis=1) > 0]  # Remove empty rows
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        bars = ax5.barh(gender_gap.index, gender_gap['Gender_Ratio'], color='#EC4899', edgecolor='white', linewidth=0.7)
        ax5.axvline(x=100, color='#FFD700', linestyle='--', alpha=0.7, label='Gender Parity (100%)')
        ax5.set_title("Female-to-Male Ratio by Education Level (%)", fontsize=14, fontweight='bold', color='#FFD700')
        ax5.set_xlabel("Female/Male Ratio (%)", fontweight='bold', color='white')
        ax5.set_ylabel("Education Level", fontweight='bold', color='white')
        ax5.tick_params(colors='white')
        ax5.legend()
        st.pyplot(fig5)

    # --- Chart 6: Technical vs Academic Education ---
    with col6:
        # Safely get technical and academic columns
        tech_academic_cols = [col for col in ['Technical', 'University', 'Secondary'] if col in gov_data.columns]
        if tech_academic_cols:
            tech_vs_academic = gov_data[tech_academic_cols].sum(axis=1)
        else:
            tech_vs_academic = gov_data['Total_Population'] * 0
            
        top_tech_academic = tech_vs_academic.nlargest(10)
        
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        top_tech_academic.plot(kind='bar', ax=ax6, color='#F59E0B', edgecolor='white', linewidth=0.7)
        ax6.set_title("Technical & Academic Education by Governorate", fontsize=14, fontweight='bold', color='#FFD700')
        ax6.set_xlabel("Governorate", fontweight='bold', color='white')
        ax6.set_ylabel("Total Students", fontweight='bold', color='white')
        ax6.tick_params(axis='x', rotation=45, labelcolor='white')
        ax6.tick_params(axis='y', labelcolor='white')
        st.pyplot(fig6)

    # --- Chart 7: Education Pyramid ---
    st.markdown("### 📐 Education Structure")
    col7, col8 = st.columns([1.7, 0.3])  # col7 = 85% width, col8 = 15%

    
    with col7:
        # Create education pyramid with existing levels only
        pyramid_data = level_counts.sort_values(ascending=False)
        
        fig7, ax7 = plt.subplots(figsize=(18, 14))
        y_pos = range(len(pyramid_data))
        ax7.barh(y_pos, pyramid_data.values, color=luxury_colors[:len(pyramid_data)], edgecolor='white', linewidth=0.7)
        ax7.set_yticks(y_pos)
        ax7.set_yticklabels(pyramid_data.index)
        ax7.set_title("Education Pyramid - Population by Level", fontsize=14, fontweight='bold', color='#FFD700')
        ax7.set_xlabel("Total Population", fontweight='bold', color='white')
        ax7.set_ylabel("Education Level", fontweight='bold', color='white')
        ax7.tick_params(colors='white')
        ax7.grid(axis='x', alpha=0.3, color='gray')
        st.pyplot(fig7)

    # --- Chart 9: Education Status Original Breakdown ---
    st.markdown("### 📋 Detailed Status View")
    
    # Original education status breakdown
    edu_status_counts = data['education'].groupby("Status")["Total"].sum().nlargest(15)
    
    fig9, ax9 = plt.subplots(figsize=(12, 8))
    sns.barplot(x=edu_status_counts.values, y=edu_status_counts.index, palette=luxury_colors,
               ax=ax9, edgecolor='white', linewidth=0.7)
    ax9.set_title("Top 15 Detailed Education Status Categories", fontsize=16, fontweight='bold', color='#FFD700')
    ax9.set_xlabel("Total Count", fontweight='bold', color='white')
    ax9.set_ylabel("Education Status", fontweight='bold', color='white')
    ax9.tick_params(colors='white')
    st.pyplot(fig9)

    # --- Enhanced Insights Cards ---
    total_students = data['education']["Total"].sum()
    
    # Safe literacy rate calculation
    basic_literacy_total = gov_data['Basic Literacy'].sum() if 'Basic Literacy' in gov_data.columns else 0
    total_population = gov_data['Total_Population'].sum()
    literacy_rate = (1 - (basic_literacy_total / total_population)) * 100 if total_population > 0 else 0
    
    # Safe highest education region
    if 'University' in gov_data.columns:
        highest_edu_region = gov_data['University'].idxmax()
    else:
        highest_edu_region = "N/A"
    
    # Gender parity calculation
    female_total = data['education'][data['education']['Gender_Type'] == 'Female']['Total'].sum()
    male_total = data['education'][data['education']['Gender_Type'] == 'Male']['Total'].sum()
    gender_parity_index = (female_total / male_total) * 100 if male_total > 0 else 0

    st.markdown("""
    <div class="luxury-card" style="margin-top: 1.5rem; text-align:center;">
        <h3 style="color: #D4AF37;">📊 Comprehensive Insights</h3>
    </div>
    """, unsafe_allow_html=True)

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #D4AF37;">
            <h4 style="color:#FFD700;">National Literacy</h4>
            <p style="color:white; font-size:1.1rem;"><b>{literacy_rate:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    with col10:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #8B5CF6;">
            <h4 style="color:#8B5CF6;">Highest Education Region</h4>
            <p style="color:white; font-size:1.1rem;"><b>{highest_edu_region}</b></p>
        </div>
        """, unsafe_allow_html=True)
    with col11:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #10B981;">
            <h4 style="color:#10B981;">Gender Parity Index</h4>
            <p style="color:white; font-size:1.1rem;"><b>{gender_parity_index:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    with col12:
        st.markdown(f"""
        <div class="insight-card" style="background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #F59E0B;">
            <h4 style="color:#F59E0B;">Total Analyzed</h4>
            <p style="color:white; font-size:1.1rem;"><b>{total_students:,.0f}</b></p>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div style="margin-top: 2rem; text-align:center; color:#a0aec0;">
        <em>This comprehensive educational analysis reveals Egypt's learning landscape through literacy rates, gender parity, regional disparities, and educational diversity.</em>
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
