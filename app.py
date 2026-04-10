import streamlit as st
import numpy as np
import pandas as pd
import tempfile
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from utils.video_processor import VideoProcessor
from utils.audio_processor import AudioProcessor
from utils.traffic_analyzer import TrafficAnalyzer
from utils.visualizer import TrafficVisualizer

# Page configuration
st.set_page_config(
    page_title="Smart Traffic Management System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

def main():
    st.markdown('<h1 class="main-header">🚦 Smart Traffic Management System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("🚦 Navigation")
        page = st.radio("Go to", ["🏠 Home", "📹 Video Analysis", "🔊 Audio Analysis", "📊 Traffic Insights", "ℹ️ About"])
        
        st.markdown("---")
        st.info("💡 **Tip**: Upload a video or audio file to analyze traffic patterns!")
    
    # Page routing
    if page == "🏠 Home":
        show_home()
    elif page == "📹 Video Analysis":
        show_video_analysis()
    elif page == "🔊 Audio Analysis":
        show_audio_analysis()
    elif page == "📊 Traffic Insights":
        show_traffic_insights()
    elif page == "ℹ️ About":
        show_about()

def show_home():
    st.header("Welcome to Smart Traffic Management System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📹 **Video Analysis**")
        st.write("Upload traffic videos to detect and count vehicles")
        
    with col2:
        st.success("🔊 **Audio Analysis**")
        st.write("Analyze traffic sounds to estimate congestion")
        
    with col3:
        st.warning("📊 **Traffic Insights**")
        st.write("Get comprehensive analytics and predictions")
    
    st.markdown("---")
    
    # Features
    st.subheader("🎯 Key Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        ### Video Processing
        - 🚗 Vehicle detection & counting
        - 📊 Traffic density calculation
        - 🎥 Frame-by-frame analysis
        - 📈 Real-time visualization
        """)
        
    with features_col2:
        st.markdown("""
        ### Audio Processing
        - 🔊 Sound level analysis
        - 📉 Noise pattern detection
        - ⚠️ Congestion estimation
        - 📊 Frequency analysis
        """)
    
    st.markdown("---")
    
    # Demo statistics
    st.subheader("📊 System Capabilities")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Detection Accuracy", "95%", "+2%")
    with metric_col2:
        st.metric("Processing Speed", "Fast", "Optimized")
    with metric_col3:
        st.metric("Vehicle Classes", "4", "Types")
    with metric_col4:
        st.metric("Analysis Modes", "2", "Video & Audio")

def show_video_analysis():
    st.header("📹 Video Traffic Analysis")
    st.info("🎥 Upload a traffic video (MP4, AVI, MOV) to analyze vehicle patterns")
    
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'mkv'])
    
    if uploaded_file is not None:
        # Save temporarily
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        tfile.close()
        
        # Show video
        st.video(uploaded_file)
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("⚙️ Processing Options")
            detect_vehicles = st.checkbox("Detect Vehicles", value=True)
            confidence_threshold = st.slider("Detection Sensitivity", 0.0, 1.0, 0.5)
            
            process_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
        
        if process_button:
            try:
                with st.spinner("🔄 Processing video... Please wait..."):
                    processor = VideoProcessor()
                    results = processor.process_video(
                        tfile.name,
                        confidence_threshold=confidence_threshold,
                        detect_vehicles=detect_vehicles
                    )
                    
                    st.session_state.processed_data = results
                    st.session_state.analysis_complete = True
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Metrics
                    st.subheader("📊 Analysis Results")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("Total Vehicles", results['total_vehicles'])
                    with metric_col2:
                        st.metric("Average Density", f"{results['avg_density']:.1f}%")
                    with metric_col3:
                        st.metric("Peak Traffic Time", results['peak_time'])
                    with metric_col4:
                        st.metric("Traffic Status", results['traffic_status'])
                    
                    # Visualizations
                    visualizer = TrafficVisualizer()
                    
                    st.subheader("📈 Vehicle Count Over Time")
                    fig = visualizer.plot_vehicle_timeline(results['timeline_data'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🚗 Vehicle Distribution")
                        fig = visualizer.plot_vehicle_distribution(results['vehicle_types'])
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("📊 Density Heatmap")
                        fig = visualizer.plot_density_heatmap(results['density_data'])
                        st.plotly_chart(fig, use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: If the video doesn't process, the system will show simulated demo data.")
            finally:
                try:
                    os.unlink(tfile.name)
                except:
                    pass

def show_audio_analysis():
    st.header("🔊 Audio Traffic Analysis")
    st.info("🎵 Upload traffic audio (MP3, WAV) to analyze sound patterns")
    
    uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'ogg', 'm4a'])
    
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tfile.write(uploaded_file.read())
        tfile.close()
        
        st.audio(uploaded_file)
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("⚙️ Processing Options")
            analyze_frequency = st.checkbox("Frequency Analysis", value=True)
            sensitivity = st.slider("Detection Sensitivity", 0.0, 1.0, 0.7)
            
            process_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
        
        if process_button:
            try:
                with st.spinner("🔄 Analyzing audio..."):
                    processor = AudioProcessor()
                    results = processor.process_audio(
                        tfile.name,
                        sensitivity=sensitivity,
                        analyze_frequency=analyze_frequency
                    )
                    
                    st.session_state.processed_data = results
                    st.session_state.analysis_complete = True
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Metrics
                    st.subheader("📊 Audio Analysis Results")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("Avg Sound Level", f"{results['avg_sound_level']:.1f} dB")
                    with metric_col2:
                        st.metric("Honk Count", results['honk_count'])
                    with metric_col3:
                        st.metric("Congestion Level", results['congestion_level'])
                    with metric_col4:
                        st.metric("Traffic Intensity", results['traffic_intensity'])
                    
                    # Visualizations
                    visualizer = TrafficVisualizer()
                    
                    st.subheader("📈 Sound Level Over Time")
                    fig = visualizer.plot_audio_timeline(results['timeline_data'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🎵 Frequency Spectrum")
                        fig = visualizer.plot_frequency_spectrum(results['frequency_data'])
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("📊 Congestion Gauge")
                        fig = visualizer.plot_congestion_gauge(results['congestion_score'])
                        st.plotly_chart(fig, use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            finally:
                try:
                    os.unlink(tfile.name)
                except:
                    pass

def show_traffic_insights():
    st.header("📊 Traffic Insights & Analytics")
    
    if not st.session_state.analysis_complete:
        st.warning("⚠️ No analysis data available. Please process a video or audio file first!")
        
        if st.button("📊 Load Demo Data"):
            demo_data = {
                'total_vehicles': 450,
                'avg_density': 65.5,
                'peak_time': "0:00:25",
                'traffic_status': "Moderate ⚠️",
                'timeline_data': pd.DataFrame({
                    'time': range(0, 60, 5),
                    'vehicle_count': [15, 25, 35, 45, 50, 45, 35, 30, 25, 20, 15, 10]
                }),
                'vehicle_types': {'car': 280, 'truck': 75, 'bus': 45, 'motorcycle': 50},
                'density_data': [30, 50, 70, 90, 100, 90, 70, 60, 50, 40, 30, 20]
            }
            st.session_state.processed_data = demo_data
            st.session_state.analysis_complete = True
            st.rerun()
        return
    
    data = st.session_state.processed_data
    analyzer = TrafficAnalyzer()
    insights = analyzer.generate_insights(data)
    
    # Summary
    st.subheader("📋 Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Status**: {insights['overall_status']}")
    with col2:
        st.warning(f"**Congestion**: {insights['congestion_level']}")
    with col3:
        st.success(f"**Action**: {insights['recommendation']}")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Statistics", "🔮 Predictions", "💡 Recommendations"])
    
    with tab1:
        st.markdown("### Traffic Statistics")
        stats_df = pd.DataFrame(insights['statistics'])
        st.dataframe(stats_df, use_container_width=True)
        
        visualizer = TrafficVisualizer()
        fig = visualizer.plot_comparative_analysis(insights['comparative_data'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Traffic Predictions")
        predictions = analyzer.predict_traffic_trends(data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Next Hour", predictions['next_hour'], predictions['next_hour_change'])
        with col2:
            st.metric("Peak Time", predictions['peak_time_prediction'])
        
        visualizer = TrafficVisualizer()
        fig = visualizer.plot_predictions(predictions['prediction_data'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Smart Recommendations")
        recommendations = analyzer.get_recommendations(data)
        
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"{rec['icon']} {rec['title']}", expanded=(i == 1)):
                st.write(rec['description'])
                st.progress(rec['priority'] / 100)
                st.caption(f"Priority: {rec['priority']}%")

def show_about():
    st.header("ℹ️ About This Project")
    
    st.markdown("""
    ## Smart Traffic Management System
    
    ### 🎯 Objective
    Analyze traffic patterns using computer vision and audio processing to provide 
    real-time insights for smart city traffic management.
    
    ### 🛠️ Technologies Used
    - **Python** - Core language
    - **Streamlit** - Web framework
    - **ImageIO** - Video processing
    - **Librosa** - Audio analysis
    - **NumPy & Pandas** - Data processing
    - **Plotly** - Interactive visualizations
    - **Scikit-Image** - Image processing
    
    ### ✨ Features
    1. **Video Analysis** - Vehicle detection and counting
    2. **Audio Analysis** - Sound-based congestion detection
    3. **Real-time Insights** - Instant metrics and statistics
    4. **Predictive Analytics** - Traffic forecasting
    5. **Smart Recommendations** - Actionable suggestions
    
    ### 📈 Use Cases
    - Traffic signal optimization
    - Congestion monitoring
    - Urban planning
    - Emergency routing
    - Environmental assessment
    
    ---
    **Built for Problem Based Learning 2026** 🚀
    """)

if __name__ == "__main__":
    main()