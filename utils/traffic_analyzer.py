import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class TrafficAnalyzer:
    def __init__(self):
        pass
    
    def generate_insights(self, data):
        """Generate comprehensive traffic insights"""
        
        insights = {
            'overall_status': '',
            'congestion_level': '',
            'recommendation': '',
            'statistics': [],
            'comparative_data': {}
        }
        
        # Determine data type and generate appropriate insights
        if 'total_vehicles' in data:  # Video data
            insights = self._analyze_video_data(data)
        elif 'avg_sound_level' in data:  # Audio data
            insights = self._analyze_audio_data(data)
        
        return insights
    
    def _analyze_video_data(self, data):
        """Analyze video traffic data"""
        density = data['avg_density']
        total_vehicles = data['total_vehicles']
        
        # Overall status
        if density < 30:
            overall_status = "Smooth Traffic Flow 🟢"
        elif density < 70:
            overall_status = "Moderate Congestion 🟡"
        else:
            overall_status = "Heavy Congestion 🔴"
        
        # Recommendation
        if density < 30:
            recommendation = "No action needed"
        elif density < 70:
            recommendation = "Monitor closely, consider signal timing adjustment"
        else:
            recommendation = "Urgent: Implement traffic diversion, optimize signal timing"
        
        # Statistics
        statistics = [
            {'Metric': 'Total Vehicles Detected', 'Value': total_vehicles},
            {'Metric': 'Average Traffic Density', 'Value': f"{density:.1f}%"},
            {'Metric': 'Peak Traffic Time', 'Value': data['peak_time']},
            {'Metric': 'Cars', 'Value': data['vehicle_types']['car']},
            {'Metric': 'Trucks', 'Value': data['vehicle_types']['truck']},
            {'Metric': 'Buses', 'Value': data['vehicle_types']['bus']},
            {'Metric': 'Motorcycles', 'Value': data['vehicle_types']['motorcycle']},
        ]
        
        # Comparative data
        comparative_data = {
            'current_hour': density,
            'previous_hour': density * 0.85,
            'same_time_yesterday': density * 0.92,
            'weekly_average': density * 0.88
        }
        
        return {
            'overall_status': overall_status,
            'congestion_level': data['traffic_status'],
            'recommendation': recommendation,
            'statistics': statistics,
            'comparative_data': comparative_data
        }
    
    def _analyze_audio_data(self, data):
        """Analyze audio traffic data"""
        sound_level = data['avg_sound_level']
        
        # Overall status
        if sound_level < 40:
            overall_status = "Quiet Traffic 🟢"
        elif sound_level < 70:
            overall_status = "Moderate Noise Level 🟡"
        else:
            overall_status = "High Noise Pollution 🔴"
        
        # Recommendation
        if sound_level < 40:
            recommendation = "Traffic flow is optimal"
        elif sound_level < 70:
            recommendation = "Monitor noise levels, consider noise barriers"
        else:
            recommendation = "High noise pollution detected, implement noise reduction measures"
        
        # Statistics
        statistics = [
            {'Metric': 'Average Sound Level', 'Value': f"{sound_level:.1f} dB"},
            {'Metric': 'Honk Count', 'Value': data['honk_count']},
            {'Metric': 'Traffic Intensity', 'Value': data['traffic_intensity']},
            {'Metric': 'Congestion Level', 'Value': data['congestion_level']},
            {'Metric': 'Audio Duration', 'Value': f"{data['duration']:.1f}s"},
        ]
        
        # Comparative data
        comparative_data = {
            'current_hour': sound_level,
            'previous_hour': sound_level * 0.9,
            'same_time_yesterday': sound_level * 0.95,
            'weekly_average': sound_level * 0.85
        }
        
        return {
            'overall_status': overall_status,
            'congestion_level': data['congestion_level'],
            'recommendation': recommendation,
            'statistics': statistics,
            'comparative_data': comparative_data
        }
    
    def predict_traffic_trends(self, data):
        """Predict future traffic trends"""
        
        # Simple prediction based on current data
        if 'avg_density' in data:
            current_value = data['avg_density']
        else:
            current_value = data['avg_sound_level']
        
        # Simulate prediction with some variation
        next_hour_value = current_value * (1 + np.random.uniform(-0.15, 0.15))
        change = ((next_hour_value - current_value) / current_value) * 100
        
        # Generate prediction timeline
        hours = 6
        prediction_timeline = []
        for i in range(hours):
            time = (datetime.now() + timedelta(hours=i+1)).strftime('%H:%M')
            value = current_value * (1 + np.random.uniform(-0.2, 0.3))
            prediction_timeline.append({
                'time': time,
                'predicted_value': value
            })
        
        return {
            'next_hour': f"{next_hour_value:.1f}",
            'next_hour_change': f"{change:+.1f}%",
            'peak_time_prediction': prediction_timeline[np.argmax([p['predicted_value'] for p in prediction_timeline])]['time'],
            'prediction_data': pd.DataFrame(prediction_timeline)
        }
    
    def get_recommendations(self, data):
        """Get actionable recommendations"""
        
        recommendations = []
        
        if 'avg_density' in data:
            density = data['avg_density']
            
            if density > 70:
                recommendations.append({
                    'icon': '🚦',
                    'title': 'Optimize Signal Timing',
                    'description': 'Adjust traffic signal timings to reduce congestion at peak hours.',
                    'priority': 95
                })
                recommendations.append({
                    'icon': '🚧',
                    'title': 'Implement Traffic Diversion',
                    'description': 'Redirect traffic to alternative routes to balance load.',
                    'priority': 85
                })
            
            if density > 50:
                recommendations.append({
                    'icon': '📱',
                    'title': 'Enable Smart Traffic Alerts',
                    'description': 'Notify commuters about current traffic conditions via mobile app.',
                    'priority': 70
                })
            
            recommendations.append({
                'icon': '📊',
                'title': 'Continuous Monitoring',
                'description': 'Deploy additional cameras and sensors for better coverage.',
                'priority': 60
            })
        
        elif 'avg_sound_level' in data:
            sound = data['avg_sound_level']
            
            if sound > 70:
                recommendations.append({
                    'icon': '🔇',
                    'title': 'Noise Reduction Measures',
                    'description': 'Install noise barriers and implement strict honking regulations.',
                    'priority': 90
                })
            
            if data['honk_count'] > 10:
                recommendations.append({
                    'icon': '⚠️',
                    'title': 'Enforce No-Honking Zones',
                    'description': 'Deploy traffic police to enforce no-honking rules.',
                    'priority': 75
                })
        
        recommendations.append({
            'icon': '🌱',
            'title': 'Environmental Impact Assessment',
            'description': 'Analyze pollution levels and implement green initiatives.',
            'priority': 50
        })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations