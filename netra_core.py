"""
N.E.T.R.A. Core Engine
Next-Gen Eye for Threat Recognition and Analysis

This module contains the core AI engine extracted from NETRA_BETA_v2.ipynb
for use in production environments (Streamlit, API, etc.)
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, List, Optional
import json


# North-East India Strategic Locations Database
NE_LOCATIONS = {
    'Guwahati_Airport': {
        'lat': 26.1061,
        'lon': 91.5859,
        'name': 'Guwahati Airport Road, Assam',
        'state': 'Assam',
        'type': 'Critical Infrastructure'
    },
    'Imphal_City': {
        'lat': 24.8170,
        'lon': 93.9368,
        'name': 'Imphal City Center, Manipur',
        'state': 'Manipur',
        'type': 'Urban Center'
    },
    'Kohima_NH29': {
        'lat': 25.6747,
        'lon': 94.1078,
        'name': 'Kohima NH-29, Nagaland',
        'state': 'Nagaland',
        'type': 'Highway'
    },
    'Shillong_Bypass': {
        'lat': 25.5788,
        'lon': 91.8933,
        'name': 'Shillong Bypass Road, Meghalaya',
        'state': 'Meghalaya',
        'type': 'Highway'
    },
    'Agartala_Station': {
        'lat': 23.8315,
        'lon': 91.2868,
        'name': 'Agartala Railway Station, Tripura',
        'state': 'Tripura',
        'type': 'Critical Infrastructure'
    },
    'Itanagar_Zero': {
        'lat': 27.0844,
        'lon': 93.6053,
        'name': 'Itanagar Zero Point, Arunachal Pradesh',
        'state': 'Arunachal Pradesh',
        'type': 'Urban Center'
    },
    'Aizawl_NH54': {
        'lat': 23.7271,
        'lon': 92.7176,
        'name': 'Aizawl NH-54, Mizoram',
        'state': 'Mizoram',
        'type': 'Highway'
    },
    'Dimapur_Junction': {
        'lat': 25.9097,
        'lon': 93.7267,
        'name': 'Dimapur Junction, Nagaland',
        'state': 'Nagaland',
        'type': 'Critical Infrastructure'
    },
    'Silchar_Medical': {
        'lat': 24.8333,
        'lon': 92.7789,
        'name': 'Silchar Medical College Road, Assam',
        'state': 'Assam',
        'type': 'Medical Facility'
    },
    'Tinsukia_Border': {
        'lat': 27.4900,
        'lon': 95.3600,
        'name': 'Tinsukia Border Checkpoint, Assam',
        'state': 'Assam',
        'type': 'Border Area'
    }
}


class NetraAI:
    """
    Advanced AI Engine for IED Threat Detection using Bayesian Fusion
    
    This class implements a multi-sensor fusion algorithm that combines
    data from rover and drone platforms to assess explosive threat probability.
    """

    def __init__(self):
        """Initialize the NETRA AI Engine with optimized sensor weights"""
        
        # Sensor weights optimized for IED detection (sum = 1.0)
        self.sensor_weights = {
            'fume': 0.20,       # Chemical vapor detection (highest weight)
            'metal': 0.18,      # Metallic object detection
            'gpr': 0.15,        # Ground penetrating radar
            'ground_cv': 0.12,  # Ground-level computer vision
            'drone_cv': 0.15,   # Aerial computer vision
            'disturbance': 0.10, # Soil disturbance analysis
            'thermal': 0.10     # Thermal signature detection
        }
        
        self.threat_history = []
        self.analysis_count = 0

    def validate_sensors(self, sensors: Dict[str, float]) -> bool:
        """
        Validate sensor input data
        
        Args:
            sensors: Dictionary of sensor readings
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_sensors = set(self.sensor_weights.keys())
        provided_sensors = set(sensors.keys())
        
        # Check all required sensors are present
        if required_sensors != provided_sensors:
            missing = required_sensors - provided_sensors
            extra = provided_sensors - required_sensors
            if missing:
                raise ValueError(f"Missing sensors: {missing}")
            if extra:
                raise ValueError(f"Unknown sensors: {extra}")
        
        # Check value ranges
        for sensor, value in sensors.items():
            if not isinstance(value, (int, float)):
                raise TypeError(f"Sensor {sensor} must be numeric, got {type(value)}")
            if not 0 <= value <= 100:
                raise ValueError(f"Sensor {sensor} out of range [0-100]: {value}")
        
        return True

    def calculate_threat_probability(self, sensors: Dict[str, float]) -> float:
        """
        Calculate threat probability using Bayesian fusion algorithm
        
        This method combines weighted sensor scores with correlation analysis
        to provide an accurate threat assessment.
        
        Args:
            sensors: Dictionary of sensor readings (0-100%)
            
        Returns:
            float: Threat probability (0-100%)
            
        Example:
            >>> ai = NetraAI()
            >>> sensors = {'fume': 80, 'metal': 75, 'gpr': 70, ...}
            >>> probability = ai.calculate_threat_probability(sensors)
            >>> print(f"Threat: {probability:.1f}%")
        """
        # Validate input
        self.validate_sensors(sensors)
        
        # Calculate base weighted score
        weighted_score = sum(
            sensors[sensor] * weight
            for sensor, weight in self.sensor_weights.items()
        )
        
        # Bayesian correlation analysis - detect sensor correlations
        correlation_boost = 0
        
        # Strong correlation: Chemical + Metal detection (IED signature)
        if sensors['fume'] > 70 and sensors['metal'] > 70:
            correlation_boost += 12
        
        # Visual confirmation from both ground and aerial angles
        if abs(sensors['drone_cv'] - sensors['ground_cv']) < 15:
            correlation_boost += 8
        
        # Thermal + Chemical signature (explosive heat signature)
        if sensors['thermal'] > 60 and sensors['fume'] > 60:
            correlation_boost += 7
        
        # Ground disturbance + GPR detection (buried device)
        if sensors['disturbance'] > 65 and sensors['gpr'] > 65:
            correlation_boost += 6
        
        # Multi-sensor high alert
        high_sensors = sum(1 for v in sensors.values() if v > 75)
        if high_sensors >= 4:
            correlation_boost += 5
        
        # Calculate final probability (capped at 100%)
        final_probability = min(100, weighted_score + correlation_boost)
        
        return round(final_probability, 2)

    def get_threat_level(self, probability: float) -> Tuple[str, str, str]:
        """
        Classify threat level based on probability
        
        Args:
            probability: Threat probability (0-100%)
            
        Returns:
            Tuple of (level_label, color_code, description)
        """
        if probability >= 75:
            return "🔴 CRITICAL", "#dc2626", "Immediate Action Required"
        elif probability >= 50:
            return "🟡 HIGH", "#f59e0b", "Enhanced Monitoring"
        elif probability >= 25:
            return "🟢 MODERATE", "#10b981", "Routine Monitoring"
        else:
            return "⚪ LOW", "#3b82f6", "Area Cleared"

    def get_recommendations(self, probability: float) -> List[str]:
        """
        Generate actionable recommendations based on threat level
        
        Args:
            probability: Threat probability (0-100%)
            
        Returns:
            List of recommended actions
        """
        if probability >= 75:
            return [
                "⚠️ EVACUATE 200m radius IMMEDIATELY",
                "🚫 BLOCK all vehicle and pedestrian traffic",
                "⚡ DEPLOY bomb disposal unit",
                "📡 ALERT military and civilian authorities",
                "🚁 MAINTAIN continuous aerial surveillance",
                "📸 CAPTURE high-resolution evidence",
                "🔒 SECURE perimeter with armed forces"
            ]
        elif probability >= 50:
            return [
                "🔍 CONDUCT detailed ground investigation",
                "🚧 PLACE warning markers and caution tape",
                "🚁 INCREASE drone surveillance frequency",
                "📸 DOCUMENT area with multiple angles",
                "⏱️ REASSESS threat level every 15 minutes",
                "📞 NOTIFY local security personnel",
                "🗺️ PREPARE evacuation routes"
            ]
        elif probability >= 25:
            return [
                "👀 MONITOR area with routine patrols",
                "📊 LOG sensor data for pattern analysis",
                "🔄 SCHEDULE follow-up scans in 2 hours",
                "📝 UPDATE threat database",
                "✅ MAINTAIN low-risk status"
            ]
        else:
            return [
                "✅ AREA CLEARED - No immediate threat",
                "📝 UPDATE digital twin database",
                "🚦 SAFE for normal traffic operations",
                "📊 ARCHIVE scan data for future reference"
            ]

    def get_confidence_score(self, sensors: Dict[str, float]) -> float:
        """
        Calculate detection confidence based on sensor agreement
        
        Args:
            sensors: Dictionary of sensor readings
            
        Returns:
            float: Confidence score (0-100%)
        """
        values = list(sensors.values())
        mean_val = np.mean(values)
        variance = np.var(values)
        
        # Lower variance = higher confidence
        # Normalize variance to 0-100 scale
        confidence = max(0, min(100, 100 - (variance / 10)))
        
        return round(confidence, 2)

    def log_threat(self, location: str, probability: float, sensors: Dict[str, float]) -> str:
        """
        Log threat detection for historical analysis
        
        Args:
            location: Location name
            probability: Threat probability
            sensors: Sensor readings
            
        Returns:
            str: Unique scan ID
        """
        scan_id = f"NETRA-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{self.analysis_count:04d}"
        
        self.threat_history.append({
            'scan_id': scan_id,
            'timestamp': datetime.utcnow(),
            'location': location,
            'probability': probability,
            'sensors': sensors.copy(),
            'threat_level': self.get_threat_level(probability)[0],
            'confidence': self.get_confidence_score(sensors)
        })
        
        self.analysis_count += 1
        return scan_id

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get threat detection history
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of threat records
        """
        if limit:
            return self.threat_history[-limit:]
        return self.threat_history

    def export_history_to_csv(self, filename: str = 'netra_threat_log.csv') -> str:
        """
        Export threat history to CSV file
        
        Args:
            filename: Output filename
            
        Returns:
            str: Path to saved file
        """
        if not self.threat_history:
            raise ValueError("No threat history to export")
        
        # Flatten the data for CSV
        records = []
        for record in self.threat_history:
            flat_record = {
                'scan_id': record['scan_id'],
                'timestamp': record['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'location': record['location'],
                'probability': record['probability'],
                'threat_level': record['threat_level'],
                'confidence': record['confidence'],
                **record['sensors']
            }
            records.append(flat_record)
        
        df = pd.DataFrame(records)
        df.to_csv(filename, index=False)
        
        return filename

    def analyze_location(self, location_key: str, sensors: Dict[str, float]) -> Dict:
        """
        Complete threat analysis for a location
        
        Args:
            location_key: Key from NE_LOCATIONS
            sensors: Sensor readings
            
        Returns:
            Dictionary with complete analysis results
        """
        if location_key not in NE_LOCATIONS:
            raise ValueError(f"Unknown location: {location_key}")
        
        location = NE_LOCATIONS[location_key]
        
        # Calculate metrics
        probability = self.calculate_threat_probability(sensors)
        threat_level, color, description = self.get_threat_level(probability)
        recommendations = self.get_recommendations(probability)
        confidence = self.get_confidence_score(sensors)
        
        # Log the analysis
        scan_id = self.log_threat(location['name'], probability, sensors)
        
        # Return comprehensive results
        return {
            'scan_id': scan_id,
            'timestamp': datetime.utcnow(),
            'location': location,
            'sensors': sensors,
            'probability': probability,
            'threat_level': threat_level,
            'color': color,
            'description': description,
            'recommendations': recommendations,
            'confidence': confidence
        }

    def batch_analyze(self, location_keys: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Perform batch analysis on multiple locations
        
        Args:
            location_keys: List of location keys (None = all locations)
            
        Returns:
            DataFrame with analysis results
        """
        if location_keys is None:
            location_keys = list(NE_LOCATIONS.keys())
        
        results = []
        
        for key in location_keys:
            # Generate random sensor readings for demonstration
            sensors = {
                sensor: float(np.random.randint(10, 95))
                for sensor in self.sensor_weights.keys()
            }
            
            analysis = self.analyze_location(key, sensors)
            location = analysis['location']
            
            results.append({
                'Scan_ID': analysis['scan_id'],
                'Location': location['name'],
                'State': location['state'],
                'Type': location['type'],
                'Latitude': location['lat'],
                'Longitude': location['lon'],
                'Threat_Probability': analysis['probability'],
                'Threat_Level': analysis['threat_level'],
                'Confidence': analysis['confidence'],
                'Classification': analysis['description'],
                **analysis['sensors']
            })
        
        return pd.DataFrame(results)

    def get_statistics(self) -> Dict:
        """
        Get system statistics
        
        Returns:
            Dictionary with system stats
        """
        if not self.threat_history:
            return {
                'total_scans': 0,
                'critical_threats': 0,
                'high_threats': 0,
                'moderate_threats': 0,
                'low_threats': 0,
                'average_probability': 0,
                'average_confidence': 0
            }
        
        probabilities = [r['probability'] for r in self.threat_history]
        confidences = [r['confidence'] for r in self.threat_history]
        
        critical = sum(1 for p in probabilities if p >= 75)
        high = sum(1 for p in probabilities if 50 <= p < 75)
        moderate = sum(1 for p in probabilities if 25 <= p < 50)
        low = sum(1 for p in probabilities if p < 25)
        
        return {
            'total_scans': len(self.threat_history),
            'critical_threats': critical,
            'high_threats': high,
            'moderate_threats': moderate,
            'low_threats': low,
            'average_probability': round(np.mean(probabilities), 2),
            'average_confidence': round(np.mean(confidences), 2)
        }


# Singleton instance for global use
_netra_instance = None

def get_netra_instance() -> NetraAI:
    """Get or create the global NETRA AI instance"""
    global _netra_instance
    if _netra_instance is None:
        _netra_instance = NetraAI()
    return _netra_instance


if __name__ == "__main__":
    # Test the engine
    print("="*80)
    print("🛡️ N.E.T.R.A. Core Engine Test")
    print("="*80)
    
    ai = NetraAI()
    
    # Test with sample sensor data
    test_sensors = {
        'fume': 85,
        'metal': 80,
        'gpr': 75,
        'ground_cv': 70,
        'drone_cv': 72,
        'disturbance': 68,
        'thermal': 65
    }
    
    result = ai.analyze_location('Guwahati_Airport', test_sensors)
    
    print(f"\n📍 Location: {result['location']['name']}")
    print(f"🎯 Threat Probability: {result['probability']:.1f}%")
    print(f"⚠️ Threat Level: {result['threat_level']}")
    print(f"💯 Confidence: {result['confidence']:.1f}%")
    print(f"\n📋 Recommendations:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n✅ Core engine test completed successfully!")
