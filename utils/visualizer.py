import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class TrafficVisualizer:
    def __init__(self):
        self.color_scheme = px.colors.qualitative.Set3
    
    def plot_vehicle_timeline(self, timeline_df):
        """Plot vehicle count over time"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timeline_df['time'],
            y=timeline_df['vehicle_count'],
            mode='lines+markers',
            name='Vehicle Count',
            line=dict(color='#1E88E5', width=3),
            fill='tozeroy',
            fillcolor='rgba(30, 136, 229, 0.2)'
        ))
        
        fig.update_layout(
            title='Vehicle Count Timeline',
            xaxis_title='Time (seconds)',
            yaxis_title='Number of Vehicles',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_vehicle_distribution(self, vehicle_types):
        """Plot vehicle type distribution"""
        df = pd.DataFrame({
            'Vehicle Type': list(vehicle_types.keys()),
            'Count': list(vehicle_types.values())
        })
        
        fig = px.pie(
            df,
            values='Count',
            names='Vehicle Type',
            title='Vehicle Type Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    
    def plot_density_heatmap(self, density_data):
        """Plot traffic density heatmap"""
        # Reshape data for heatmap
        density_array = np.array(density_data)
        rows = int(np.sqrt(len(density_array)))
        cols = len(density_array) // rows
        
        heatmap_data = density_array[:rows*cols].reshape(rows, cols)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            colorscale='RdYlGn_r',
            colorbar=dict(title='Density %')
        ))
        
        fig.update_layout(
            title='Traffic Density Heatmap',
            xaxis_title='Time Segment',
            yaxis_title='Road Section',
            height=400
        )
        
        return fig
    
    def plot_audio_timeline(self, timeline_df):
        """Plot sound level over time"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timeline_df['time'],
            y=timeline_df['sound_level'],
            mode='lines',
            name='Sound Level',
            line=dict(color='#43A047', width=2),
            fill='tozeroy',
            fillcolor='rgba(67, 160, 71, 0.2)'
        ))
        
        # Add threshold lines
        fig.add_hline(y=40, line_dash="dash", line_color="green", 
                     annotation_text="Low Threshold")
        fig.add_hline(y=70, line_dash="dash", line_color="red", 
                     annotation_text="High Threshold")
        
        fig.update_layout(
            title='Sound Level Timeline',
            xaxis_title='Time (seconds)',
            yaxis_title='Sound Level (dB)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_frequency_spectrum(self, frequency_df):
        """Plot frequency spectrum"""
        if frequency_df is None:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=frequency_df['frequency'],
            y=frequency_df['magnitude'],
            mode='lines',
            name='Magnitude',
            line=dict(color='#E53935', width=2),
            fill='tozeroy',
            fillcolor='rgba(229, 57, 53, 0.2)'
        ))
        
        fig.update_layout(
            title='Frequency Spectrum Analysis',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Magnitude',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_congestion_gauge(self, congestion_score):
        """Plot congestion gauge"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=congestion_score,
            title={'text': "Congestion Level"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightgreen"},
                    {'range': [33, 66], 'color': "yellow"},
                    {'range': [66, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400)
        
        return fig
    
    def plot_comparative_analysis(self, comparative_data):
        """Plot comparative analysis"""
        categories = list(comparative_data.keys())
        values = list(comparative_data.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['#1E88E5', '#43A047', '#FB8C00', '#8E24AA'],
                text=values,
                texttemplate='%{text:.1f}',
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='Comparative Traffic Analysis',
            xaxis_title='Time Period',
            yaxis_title='Traffic Level',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_predictions(self, prediction_df):
        """Plot traffic predictions"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=prediction_df['time'],
            y=prediction_df['predicted_value'],
            mode='lines+markers',
            name='Predicted Traffic',
            line=dict(color='#7B1FA2', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Traffic Prediction (Next 6 Hours)',
            xaxis_title='Time',
            yaxis_title='Predicted Traffic Level',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig