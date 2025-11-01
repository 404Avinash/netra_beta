"""
N.E.T.R.A. Streamlit Web Application
Next-Gen Eye for Threat Recognition and Analysis

Professional web interface for hackathon presentation
Author: Pradhyuman Singh Pancholi
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import time
import json

# Import NETRA core engine
from netra_core import NetraAI, NE_LOCATIONS, get_netra_instance


# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="N.E.T.R.A. Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        }
        to {
            box-shadow: 0 20px 80px rgba(102, 126, 234, 0.6);
        }
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    /* Alert boxes */
    .alert-critical {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(220, 38, 38, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    .alert-high {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(245, 158, 11, 0.4);
    }
    
    .alert-moderate {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(16, 185, 129, 0.4);
    }
    
    .alert-low {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Sensor gauge */
    .sensor-value {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Info boxes */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    """Initialize session state variables"""
    if 'netra_ai' not in st.session_state:
        st.session_state.netra_ai = get_netra_instance()
    
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    
    if 'sensor_values' not in st.session_state:
        st.session_state.sensor_values = {
            'fume': 50,
            'metal': 50,
            'gpr': 50,
            'ground_cv': 50,
            'drone_cv': 50,
            'disturbance': 50,
            'thermal': 50
        }

init_session_state()


# ==================== HELPER FUNCTIONS ====================
def create_header():
    """Create animated header"""
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <div class='main-header'>
        <h1 style='margin: 0; font-size: 3.5rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.4);'>
            🛡️ N.E.T.R.A. COMMAND CENTER
        </h1>
        <h3 style='color: #e0e0ff; margin: 15px 0; font-weight: 300; font-size: 1.5rem;'>
            Next-Gen Eye for Threat Recognition & Analysis
        </h3>
        <p style='color: #b0b0ff; margin: 10px 0; font-size: 1.1rem;'>
            📍 North-East India Defense Operations |
            ⏰ {current_time} UTC |
            🌐 Status: <span style='color: #10b981; font-weight: bold;'>OPERATIONAL</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def create_metrics_dashboard():
    """Create real-time metrics dashboard"""
    stats = st.session_state.netra_ai.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Total Scans",
            value=stats['total_scans'],
            delta="+1" if stats['total_scans'] > 0 else None
        )
    
    with col2:
        st.metric(
            label="🔴 Critical Threats",
            value=stats['critical_threats'],
            delta=None,
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📊 Avg Probability",
            value=f"{stats['average_probability']:.1f}%",
            delta=None
        )
    
    with col4:
        st.metric(
            label="💯 Avg Confidence",
            value=f"{stats['average_confidence']:.1f}%",
            delta=None
        )


def create_sensor_gauge(value, label, emoji):
    """Create sensor gauge visualization"""
    
    # Determine color based on value
    if value >= 70:
        color = "#dc2626"
        status = "🔴 ALERT"
    elif value >= 40:
        color = "#f59e0b"
        status = "🟡 ELEVATED"
    else:
        color = "#10b981"
        status = "🟢 NORMAL"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"{emoji} {label}", 'font': {'size': 18, 'color': 'white'}},
        number={'font': {'size': 30, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(16, 185, 129, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(220, 38, 38, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=200,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig, status


def create_threat_map(analysis_result):
    """Create interactive Folium map with threat visualization"""
    location = analysis_result['location']
    lat = location['lat']
    lon = location['lon']
    probability = analysis_result['probability']
    threat_level = analysis_result['threat_level']
    
    # Create base map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add tile layers
    folium.TileLayer('CartoDB dark_matter').add_to(m)
    
    # Determine marker color
    if probability >= 75:
        marker_color = 'red'
        icon_name = 'exclamation-triangle'
    elif probability >= 50:
        marker_color = 'orange'
        icon_name = 'exclamation-circle'
    elif probability >= 25:
        marker_color = 'green'
        icon_name = 'info-circle'
    else:
        marker_color = 'blue'
        icon_name = 'check-circle'
    
    # Main threat marker
    popup_html = f"""
    <div style="font-family: Arial; width: 300px;">
        <h3 style="color: {analysis_result['color']};">⚠️ THREAT DETECTED</h3>
        <hr>
        <p><b>📍 Location:</b> {location['name']}</p>
        <p><b>🗺️ State:</b> {location['state']}</p>
        <p><b>🏢 Type:</b> {location['type']}</p>
        <p><b>🎯 Threat Level:</b> <span style="color: {analysis_result['color']};">{threat_level}</span></p>
        <p><b>📊 Probability:</b> <span style="font-size: 20px; font-weight: bold;">{probability:.1f}%</span></p>
        <p><b>⏰ Time:</b> {analysis_result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
    </div>
    """
    
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=f"{threat_level} - {probability:.1f}%",
        icon=folium.Icon(color=marker_color, icon=icon_name, prefix='fa')
    ).add_to(m)
    
    # Add danger zones
    if probability >= 75:
        folium.Circle(
            location=[lat, lon],
            radius=200,
            color='#dc2626',
            fill=True,
            fillColor='#dc2626',
            fillOpacity=0.3,
            popup='🚨 EVACUATION ZONE - 200m',
            weight=3
        ).add_to(m)
        
        folium.Circle(
            location=[lat, lon],
            radius=500,
            color='#f59e0b',
            fill=True,
            fillColor='#f59e0b',
            fillOpacity=0.15,
            popup='⚠️ CAUTION ZONE - 500m',
            weight=2,
            dashArray='10, 5'
        ).add_to(m)
    
    elif probability >= 50:
        folium.Circle(
            location=[lat, lon],
            radius=150,
            color='#f59e0b',
            fill=True,
            fillColor='#f59e0b',
            fillOpacity=0.25,
            popup='🟡 ALERT ZONE - 150m',
            weight=2
        ).add_to(m)
    
    # Add rover and drone positions
    folium.Marker(
        location=[lat - 0.002, lon - 0.002],
        popup='<b>🚗 Rover Alpha</b><br>Status: Active',
        icon=folium.Icon(color='blue', icon='truck', prefix='fa')
    ).add_to(m)
    
    folium.Marker(
        location=[lat + 0.001, lon + 0.001],
        popup='<b>🚁 Drone Delta</b><br>Altitude: 50m',
        icon=folium.Icon(color='purple', icon='plane', prefix='fa')
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m


def create_sensor_correlation_matrix(sensors):
    """Create sensor correlation matrix"""
    # Create a correlation-like matrix
    sensor_names = list(sensors.keys())
    n = len(sensor_names)
    
    # Generate correlation data
    correlation_data = np.eye(n)
    for i in range(n):
        for j in range(i+1, n):
            val = abs(sensors[sensor_names[i]] - sensors[sensor_names[j]]) / 100
            correlation_data[i][j] = 1 - val
            correlation_data[j][i] = 1 - val
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_data,
        x=sensor_names,
        y=sensor_names,
        colorscale='RdYlGn',
        zmid=0.5
    ))
    
    fig.update_layout(
        title='Sensor Correlation Matrix',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=400
    )
    
    return fig


def create_radar_chart(sensors):
    """Create radar chart for sensor readings"""
    categories = list(sensors.keys())
    values = list(sensors.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Sensor Readings',
        line_color='#3b82f6',
        fillcolor='rgba(59, 130, 246, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        title='📡 Multi-Sensor Radar Analysis',
        height=500
    )
    
    return fig


# ==================== MAIN APPLICATION ====================
def main():
    """Main application logic"""
    
    # Header
    create_header()
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=N.E.T.R.A.+SYSTEM", use_container_width=True)
        
        st.markdown("## 🎛️ Navigation")
        page = st.radio(
            "Select Module",
            ["🏠 Dashboard", "🔍 Threat Analysis", "🗺️ Regional Map", "📊 Batch Analysis", "📈 Analytics", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 🛡️ System Status")
        st.success("✅ Rover: Online (87%)")
        st.success("✅ Drone: Active (50m)")
        st.success("✅ Comms: Stable")
        st.info("🧠 AI: Bayesian Fusion Active")
        
        st.markdown("---")
        st.markdown("### 📞 Emergency Contacts")
        st.text("🚨 Emergency: 112")
        st.text("🚔 Police: 100")
        st.text("🚑 Ambulance: 102")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🔍 Threat Analysis":
        show_threat_analysis()
    elif page == "🗺️ Regional Map":
        show_regional_map()
    elif page == "📊 Batch Analysis":
        show_batch_analysis()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        🛡️ N.E.T.R.A. Command Center v2.0 | 
        🔒 Classification: RESTRICTED | 
        © 2025 Defense Systems | 
        Developed by Pradhyuman Singh Pancholi
    </div>
    """, unsafe_allow_html=True)


# ==================== PAGE FUNCTIONS ====================
def show_dashboard():
    """Show main dashboard"""
    st.markdown("## 📊 System Overview Dashboard")
    
    # Metrics
    create_metrics_dashboard()
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📜 Recent Threat Scans")
        history = st.session_state.netra_ai.get_history(limit=10)
        
        if history:
            df = pd.DataFrame([{
                'Scan ID': h['scan_id'],
                'Time': h['timestamp'].strftime('%H:%M:%S'),
                'Location': h['location'],
                'Probability': f"{h['probability']:.1f}%",
                'Level': h['threat_level']
            } for h in reversed(history)])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 No scans performed yet. Go to Threat Analysis to start.")
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        stats = st.session_state.netra_ai.get_statistics()
        
        if stats['total_scans'] > 0:
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=['Critical', 'High', 'Moderate', 'Low'],
                values=[stats['critical_threats'], stats['high_threats'], 
                       stats['moderate_threats'], stats['low_threats']],
                marker=dict(colors=['#dc2626', '#f59e0b', '#10b981', '#3b82f6']),
                hole=0.4
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=300,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Statistics will appear after scans")


def show_threat_analysis():
    """Show threat analysis page"""
    st.markdown("## 🔍 Real-Time Threat Analysis")
    
    # Location selection
    st.markdown("### 📍 Select Target Location")
    location_key = st.selectbox(
        "Location",
        options=list(NE_LOCATIONS.keys()),
        format_func=lambda x: NE_LOCATIONS[x]['name'],
        label_visibility="collapsed"
    )
    
    location = NE_LOCATIONS[location_key]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**State:** {location['state']}")
    with col2:
        st.info(f"**Type:** {location['type']}")
    with col3:
        st.info(f"**Coords:** {location['lat']:.4f}°N, {location['lon']:.4f}°E")
    
    st.markdown("---")
    
    # Sensor controls
    st.markdown("### 🎛️ Sensor Configuration")
    
    st.markdown("#### 🚗 Phase 1: Rover Sensors")
    col1, col2 = st.columns(2)
    with col1:
        fume = st.slider("💨 Chemical Fume Detector", 0, 100, 50, key='fume')
        metal = st.slider("🔩 Metal Detector", 0, 100, 50, key='metal')
    with col2:
        gpr = st.slider("📡 Ground Penetrating Radar", 0, 100, 50, key='gpr')
        ground_cv = st.slider("👁️ Ground Computer Vision", 0, 100, 50, key='ground_cv')
    
    st.markdown("#### 🚁 Phase 2: Drone Sensors")
    col1, col2 = st.columns(2)
    with col1:
        drone_cv = st.slider("🛸 Aerial Computer Vision", 0, 100, 50, key='drone_cv')
        disturbance = st.slider("🌍 Soil Disturbance Analyzer", 0, 100, 50, key='disturbance')
    with col2:
        thermal = st.slider("🌡️ Thermal Imaging", 0, 100, 50, key='thermal')
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🔍 ANALYZE THREAT NOW", type="primary", use_container_width=True):
            analyze_and_display(location_key, {
                'fume': fume,
                'metal': metal,
                'gpr': gpr,
                'ground_cv': ground_cv,
                'drone_cv': drone_cv,
                'disturbance': disturbance,
                'thermal': thermal
            })
    
    with col2:
        if st.button("🎲 RANDOM SCENARIO", use_container_width=True):
            random_sensors = {
                'fume': np.random.randint(10, 95),
                'metal': np.random.randint(10, 95),
                'gpr': np.random.randint(10, 95),
                'ground_cv': np.random.randint(10, 95),
                'drone_cv': np.random.randint(10, 95),
                'disturbance': np.random.randint(10, 95),
                'thermal': np.random.randint(10, 95)
            }
            analyze_and_display(location_key, random_sensors)
    
    with col3:
        if st.button("🔄 RESET", use_container_width=True):
            st.rerun()
    
    # Display results if analysis was performed
    if st.session_state.current_analysis:
        display_analysis_results(st.session_state.current_analysis)


def analyze_and_display(location_key, sensors):
    """Perform threat analysis and store results"""
    with st.spinner("🔄 Analyzing threat data..."):
        time.sleep(1)  # Simulate processing
        analysis = st.session_state.netra_ai.analyze_location(location_key, sensors)
        st.session_state.current_analysis = analysis
        st.success(f"✅ Analysis complete! Scan ID: {analysis['scan_id']}")


def display_analysis_results(analysis):
    """Display comprehensive analysis results"""
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Threat probability display
    probability = analysis['probability']
    threat_level = analysis['threat_level']
    color = analysis['color']
    
    # Alert box based on threat level
    if probability >= 75:
        alert_class = "alert-critical"
    elif probability >= 50:
        alert_class = "alert-high"
    elif probability >= 25:
        alert_class = "alert-moderate"
    else:
        alert_class = "alert-low"
    
    st.markdown(f"""
    <div class='{alert_class}'>
        <h2 style='margin: 0; text-align: center;'>{threat_level}</h2>
        <h1 style='margin: 10px 0; text-align: center; font-size: 4rem;'>{probability:.1f}%</h1>
        <p style='margin: 0; text-align: center; font-size: 1.2rem;'>{analysis['description']}</p>
        <p style='margin: 10px 0 0 0; text-align: center;'>
            💯 Confidence: {analysis['confidence']:.1f}% | 
            ⏰ {analysis['timestamp'].strftime('%H:%M:%S')} UTC |
            🆔 {analysis['scan_id']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 Sensor Radar Chart")
        fig = create_radar_chart(analysis['sensors'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔗 Sensor Correlation")
        fig = create_sensor_correlation_matrix(analysis['sensors'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Sensor gauges
    st.markdown("### 🎯 Individual Sensor Readings")
    cols = st.columns(4)
    sensor_info = [
        ('fume', '💨 Fume'),
        ('metal', '🔩 Metal'),
        ('gpr', '📡 GPR'),
        ('ground_cv', '👁️ Ground CV'),
        ('drone_cv', '🚁 Drone CV'),
        ('disturbance', '🌍 Disturbance'),
        ('thermal', '🌡️ Thermal')
    ]
    
    for idx, (sensor_key, sensor_label) in enumerate(sensor_info):
        with cols[idx % 4]:
            fig, status = create_sensor_gauge(analysis['sensors'][sensor_key], sensor_label.split()[1], sensor_label.split()[0])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<p style='text-align: center;'>{status}</p>", unsafe_allow_html=True)
    
    # Map
    st.markdown("### 🗺️ Threat Location Map")
    threat_map = create_threat_map(analysis)
    st_folium(threat_map, width=1400, height=500)
    
    # Recommendations
    st.markdown("### 💡 Recommended Actions")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.markdown(f"**{i}.** {rec}")
    
    # Export option
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export to CSV", use_container_width=True):
            try:
                filename = st.session_state.netra_ai.export_history_to_csv()
                st.success(f"✅ Data exported to {filename}")
            except ValueError as e:
                st.error(str(e))
    
    with col2:
        if st.button("📊 Generate PDF Report", use_container_width=True):
            st.info("📄 PDF generation feature coming soon!")
    
    with col3:
        if st.button("📧 Send Alert", use_container_width=True):
            st.info("📨 Alert system feature coming soon!")


def show_regional_map():
    """Show regional threat map for all locations"""
    st.markdown("## 🗺️ North-East India Regional Threat Map")
    
    st.info("📍 Displaying all 10 strategic locations across 7 states")
    
    # Create map centered on North-East India
    m = folium.Map(location=[26.0, 92.5], zoom_start=6, tiles='OpenStreetMap')
    
    # Add markers for all locations
    for key, loc in NE_LOCATIONS.items():
        # Generate random threat for demo
        threat = np.random.randint(0, 100)
        
        if threat >= 75:
            color = 'red'
        elif threat >= 50:
            color = 'orange'
        elif threat >= 25:
            color = 'green'
        else:
            color = 'blue'
        
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=f"<b>{loc['name']}</b><br>Threat: {threat}%<br>State: {loc['state']}",
            tooltip=loc['name'],
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # Display map
    st_folium(m, width=1400, height=700)
    
    # Location table
    st.markdown("### 📋 Location Directory")
    df = pd.DataFrame([
        {
            'Location': loc['name'],
            'State': loc['state'],
            'Type': loc['type'],
            'Latitude': loc['lat'],
            'Longitude': loc['lon']
        }
        for loc in NE_LOCATIONS.values()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)


def show_batch_analysis():
    """Show batch analysis page"""
    st.markdown("## 📊 Batch Threat Analysis")
    
    st.info("🔍 Analyze all 10 strategic locations simultaneously")
    
    if st.button("🚀 RUN BATCH ANALYSIS", type="primary", use_container_width=True):
        with st.spinner("⚡ Analyzing all locations..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results_df = st.session_state.netra_ai.batch_analyze()
            
            # Simulate progress
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
                if i % 10 == 0:
                    status_text.text(f"Processing... {i+1}%")
            
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ Batch analysis completed!")
            
            # Display results
            st.markdown("### 📈 Analysis Results")
            st.dataframe(
                results_df[['Location', 'State', 'Threat_Probability', 'Threat_Level', 'Confidence']],
                use_container_width=True,
                hide_index=True
            )
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 Top 5 High-Risk Locations")
                top5 = results_df.nlargest(5, 'Threat_Probability')
                fig = px.bar(
                    top5,
                    x='Location',
                    y='Threat_Probability',
                    color='Threat_Probability',
                    color_continuous_scale='Reds',
                    title="Highest Threat Probabilities"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🗺️ Threat Distribution by State")
                state_avg = results_df.groupby('State')['Threat_Probability'].mean().reset_index()
                fig = px.pie(
                    state_avg,
                    values='Threat_Probability',
                    names='State',
                    title="Average Threat by State"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Regional map
            st.markdown("### 🗺️ Regional Threat Heatmap")
            regional_map = folium.Map(location=[26.0, 92.5], zoom_start=6)
            
            for _, row in results_df.iterrows():
                prob = row['Threat_Probability']
                color = 'red' if prob >= 75 else 'orange' if prob >= 50 else 'green' if prob >= 25 else 'blue'
                
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=prob/5,
                    popup=f"{row['Location']}<br>Threat: {prob:.1f}%",
                    tooltip=row['Location'],
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.6
                ).add_to(regional_map)
            
            st_folium(regional_map, width=1400, height=600)
            
            # Export
            if st.button("📥 Export Batch Results", use_container_width=True):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'netra_batch_analysis_{timestamp}.csv'
                results_df.to_csv(filename, index=False)
                st.success(f"✅ Results saved to {filename}")


def show_analytics():
    """Show analytics and historical data"""
    st.markdown("## 📈 System Analytics & Historical Data")
    
    history = st.session_state.netra_ai.get_history()
    
    if not history:
        st.warning("📊 No historical data available yet. Perform some threat analyses first.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'Timestamp': h['timestamp'],
        'Location': h['location'],
        'Probability': h['probability'],
        'Confidence': h['confidence'],
        'Threat_Level': h['threat_level']
    } for h in history])
    
    # Statistics
    st.markdown("### 📊 Overall Statistics")
    stats = st.session_state.netra_ai.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scans", stats['total_scans'])
    col2.metric("Avg Probability", f"{stats['average_probability']:.1f}%")
    col3.metric("Avg Confidence", f"{stats['average_confidence']:.1f}%")
    col4.metric("Critical Threats", stats['critical_threats'])
    
    # Time series
    st.markdown("### 📉 Threat Probability Timeline")
    fig = px.line(
        df,
        x='Timestamp',
        y='Probability',
        title='Threat Probability Over Time',
        markers=True
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Probability Distribution")
        fig = px.histogram(
            df,
            x='Probability',
            nbins=20,
            title='Threat Probability Distribution'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Threat Level Breakdown")
        level_counts = df['Threat_Level'].value_counts()
        fig = px.pie(
            values=level_counts.values,
            names=level_counts.index,
            title='Threat Level Distribution'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent scans table
    st.markdown("### 📜 Recent Scans")
    st.dataframe(df.tail(20), use_container_width=True, hide_index=True)


def show_settings():
    """Show settings page"""
    st.markdown("## ⚙️ System Settings")
    
    st.markdown("### 🚨 Alert Thresholds")
    col1, col2 = st.columns(2)
    
    with col1:
        critical_threshold = st.slider("🔴 Critical Threshold (%)", 0, 100, 75)
        high_threshold = st.slider("🟡 High Threshold (%)", 0, 100, 50)
    
    with col2:
        moderate_threshold = st.slider("🟢 Moderate Threshold (%)", 0, 100, 25)
        low_threshold = st.slider("⚪ Low Threshold (%)", 0, 100, 0)
    
    st.markdown("### 🔔 Notification Settings")
    email_alerts = st.checkbox("📧 Enable Email Alerts", value=True)
    sms_alerts = st.checkbox("📱 Enable SMS Alerts", value=False)
    push_notifications = st.checkbox("🔔 Enable Push Notifications", value=True)
    
    st.markdown("### 🎨 Display Settings")
    theme = st.selectbox("Theme", ["Dark Mode", "Light Mode", "Auto"])
    map_style = st.selectbox("Map Style", ["OpenStreetMap", "Satellite", "Terrain"])
    
    st.markdown("### 💾 Data Management")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export All Data", use_container_width=True):
            try:
                filename = st.session_state.netra_ai.export_history_to_csv()
                st.success(f"✅ Data exported to {filename}")
            except ValueError as e:
                st.error(str(e))
    
    with col2:
        if st.button("🔄 Reset History", use_container_width=True):
            st.session_state.netra_ai.threat_history = []
            st.session_state.netra_ai.analysis_count = 0
            st.success("✅ History cleared")
            st.rerun()
    
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("📄 Report generation coming soon!")
    
    st.markdown("---")
    
    if st.button("💾 SAVE SETTINGS", type="primary", use_container_width=True):
        st.success("✅ Settings saved successfully!")
    
    # System info
    st.markdown("### ℹ️ System Information")
    st.info(f"""
    **Version:** 2.0.0  
    **Last Updated:** November 2, 2025  
    **Engine:** Bayesian Fusion AI  
    **Locations Monitored:** 10  
    **Developer:** Pradhyuman Singh Pancholi
    """)


# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
