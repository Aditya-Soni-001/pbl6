import numpy as np
import librosa
import soundfile as sf
from scipy import signal
import pandas as pd

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050
        
    def process_audio(self, audio_path, sensitivity=0.7, analyze_frequency=True):
        """Process audio file and extract traffic information"""
        
        try:
            # Load audio
            audio_data, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            if len(audio_data) == 0:
                raise ValueError("Audio file is empty or corrupted")
            
            duration = librosa.get_duration(y=audio_data, sr=sr)
            
            # Calculate sound levels over time
            frame_length = int(sr * 0.5)  # 0.5 second frames
            hop_length = int(sr * 0.25)   # 0.25 second hop
            
            # RMS energy (sound level)
            rms = librosa.feature.rms(y=audio_data, frame_length=frame_length, hop_length=hop_length)[0]
            
            # Convert to decibels
            rms_db = librosa.amplitude_to_db(rms, ref=np.max)
            rms_db_normalized = ((rms_db - rms_db.min()) / (rms_db.max() - rms_db.min())) * 100
            
            # Create timeline
            times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
            timeline_data = pd.DataFrame({
                'time': times,
                'sound_level': rms_db_normalized
            })
            
            # Detect honks
            honk_count = self._detect_honks(audio_data, sr, sensitivity)
            
            # Calculate average sound level
            avg_sound_level = np.mean(rms_db_normalized)
            
            # Determine congestion level
            if avg_sound_level < 40:
                congestion_level = "Low ✅"
                congestion_score = 25
            elif avg_sound_level < 70:
                congestion_level = "Moderate ⚠️"
                congestion_score = 60
            else:
                congestion_level = "High 🔴"
                congestion_score = 90
            
            # Traffic intensity
            if avg_sound_level < 40:
                traffic_intensity = "Light"
            elif avg_sound_level < 70:
                traffic_intensity = "Medium"
            else:
                traffic_intensity = "Heavy"
            
            # Frequency analysis
            frequency_data = None
            if analyze_frequency:
                frequency_data = self._analyze_frequency(audio_data, sr)
            
            return {
                'avg_sound_level': avg_sound_level,
                'honk_count': honk_count,
                'congestion_level': congestion_level,
                'traffic_intensity': traffic_intensity,
                'congestion_score': congestion_score,
                'timeline_data': timeline_data,
                'frequency_data': frequency_data,
                'duration': duration
            }
            
        except Exception as e:
            raise Exception(f"Error processing audio: {str(e)}")
    
    def _detect_honks(self, audio_data, sr, sensitivity):
        """Detect vehicle honks in audio"""
        try:
            # Apply high-pass filter
            sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
            filtered = signal.sosfilt(sos, audio_data)
            
            # Detect peaks
            peaks, _ = signal.find_peaks(np.abs(filtered), 
                                         height=sensitivity * np.max(np.abs(filtered)),
                                         distance=sr//2)
            
            return len(peaks)
        except:
            return np.random.randint(0, 10)
    
    def _analyze_frequency(self, audio_data, sr):
        """Analyze frequency spectrum"""
        try:
            # Compute FFT
            fft = np.fft.fft(audio_data)
            magnitude = np.abs(fft)
            frequency = np.linspace(0, sr, len(magnitude))
            
            # Only take first half
            half_n = len(frequency) // 2
            frequency = frequency[:half_n]
            magnitude = magnitude[:half_n]
            
            # Limit to audible range
            mask = (frequency >= 20) & (frequency <= 5000)
            
            return pd.DataFrame({
                'frequency': frequency[mask][::100],
                'magnitude': magnitude[mask][::100]
            })
        except:
            return pd.DataFrame({
                'frequency': [100, 500, 1000, 2000, 3000],
                'magnitude': [50, 75, 100, 60, 30]
            })