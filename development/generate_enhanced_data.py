"""
Enhanced Data Generator for N.E.T.R.A. System
Generates 1000+ threat analyses with 1500+ explosive variants
Integrates explosives_dataset_1500_entries_Version2.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def load_explosive_database():
    """
    Load comprehensive explosive database from CSV
    Returns dictionary of explosive types with characteristics
    """
    db_file = '../explosives_dataset_1500_entries_Version2.csv'
    
    if not os.path.exists(db_file):
        print(f"⚠️ Warning: {db_file} not found. Using fallback database.")
        return get_fallback_explosives()
    
    try:
        df = pd.read_csv(db_file)
        print(f"✅ Loaded {len(df)} explosive variants from database")
        
        explosives = {}
        for idx, row in df.iterrows():
            name = str(row['Explosive Name']).strip()
            fume_info = str(row.get('Detonation Products & Inferred Fume Color', 'Unknown'))
            
            # Extract fume color from description
            fume_color = 'Unknown'
            if 'Black' in fume_info:
                fume_color = 'Black/Orange-Brown'
            elif 'Orange' in fume_info or 'Brown' in fume_info:
                fume_color = 'Orange/Brown NOx'
            elif 'White' in fume_info:
                fume_color = 'White vapor'
            elif 'Yellow' in fume_info:
                fume_color = 'Yellow smoke'
            elif 'Colorless' in fume_info:
                fume_color = 'Colorless'
            
            # Classify danger based on detonation velocity
            velocity = float(row.get('Detonation Velocity (m/s)', 0))
            if velocity > 7500:
                danger = 'Very High'
            elif velocity > 5000:
                danger = 'High'
            elif velocity > 3000:
                danger = 'Medium'
            else:
                danger = 'Low'
            
            # Handle brisance - ensure not NaN
            brisance_val = row.get('Brisance', 'Medium')
            if pd.isna(brisance_val) or str(brisance_val).strip() == '':
                brisance_val = 'Medium'
            
            explosives[name] = {
                'fume_color': fume_color,
                'danger': danger,
                'velocity': int(velocity),
                'density': float(row.get('Density (g/cm³)', 1.0)) if pd.notna(row.get('Density (g/cm³)')) else 1.0,
                'brisance': str(brisance_val).strip(),
                'type': str(row.get('Type/Class', 'Unknown'))
            }
        
        return explosives
        
    except Exception as e:
        print(f"⚠️ Error loading explosive database: {e}")
        return get_fallback_explosives()

def get_fallback_explosives():
    """Fallback explosive database if CSV not available"""
    return {
        # Military/Common Explosives
        'TNT': {'fume_color': 'Black/Orange-Brown', 'danger': 'High', 'velocity': 6900, 'density': 1.65, 'brisance': 'High', 'type': 'Nitroaromatic'},
        'RDX': {'fume_color': 'Orange/Brown NOx', 'danger': 'Very High', 'velocity': 8750, 'density': 1.82, 'brisance': 'Very High', 'type': 'Nitramine'},
        'HMX': {'fume_color': 'Brown NOx', 'danger': 'Very High', 'velocity': 9100, 'density': 1.91, 'brisance': 'Very High', 'type': 'Nitramine'},
        'PETN': {'fume_color': 'Colorless/Brown', 'danger': 'Very High', 'velocity': 8400, 'density': 1.77, 'brisance': 'Very High', 'type': 'Nitrate Ester'},
        'C4': {'fume_color': 'Brown/Orange', 'danger': 'Very High', 'velocity': 8040, 'density': 1.59, 'brisance': 'Very High', 'type': 'Plastic Explosive'},
        'TATP': {'fume_color': 'White vapor', 'danger': 'Very High', 'velocity': 5300, 'density': 1.22, 'brisance': 'High', 'type': 'Peroxide'},
        'ANFO': {'fume_color': 'Brown/Orange NOx', 'danger': 'Medium', 'velocity': 4200, 'density': 0.93, 'brisance': 'Medium', 'type': 'Ammonium Nitrate'}
    }

# Load explosive database at module level
EXPLOSIVE_TYPES = load_explosive_database()

def generate_enhanced_threats(num_records=1000, days_back=60):
    """
    Generate threat analyses with realistic explosive signatures
    
    Args:
        num_records: Number of analyses to generate (default 1000)
        days_back: Time range in days (default 60)
    """
    print(f"🚀 Generating {num_records} threat analyses over {days_back} days...")
    
    # Load existing locations (from parent directory)
    locations_file = '../locations_northeast_india.csv'
    if not os.path.exists(locations_file):
        locations_file = 'locations_northeast_india.csv'  # Try current directory
    
    locations_df = pd.read_csv(locations_file)
    
    # Create a mapping of location to state
    location_state_map = dict(zip(locations_df['Location'], locations_df['State']))
    locations = locations_df['Location'].tolist()
    
    records = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Generate threat distribution
    threat_distribution = {
        'CRITICAL': int(num_records * 0.21),
        'HIGH': int(num_records * 0.26),
        'MODERATE': int(num_records * 0.32),
        'LOW': num_records - int(num_records * 0.79)  # Remaining
    }
    
    threat_levels = []
    for level, count in threat_distribution.items():
        threat_levels.extend([level] * count)
    random.shuffle(threat_levels)
    
    explosive_names = list(EXPLOSIVE_TYPES.keys())
    
    for i in range(num_records):
        # Random timestamp
        random_days = random.uniform(0, days_back)
        timestamp = start_date + timedelta(days=random_days)
        
        # Select explosive type
        explosive = random.choice(explosive_names)
        explosive_data = EXPLOSIVE_TYPES[explosive]
        
        # Generate sensor readings based on threat level AND explosive characteristics
        threat_level = threat_levels[i]
        
        # Base ranges by threat level
        if threat_level == 'CRITICAL':
            base_range = (75, 95)
        elif threat_level == 'HIGH':
            base_range = (60, 80)
        elif threat_level == 'MODERATE':
            base_range = (40, 65)
        else:  # LOW
            base_range = (10, 45)
        
        # Adjust based on explosive velocity (higher velocity = more detectable)
        velocity_modifier = 0
        if explosive_data['velocity'] > 7500:
            velocity_modifier = 8  # Military-grade, very detectable
        elif explosive_data['velocity'] > 5000:
            velocity_modifier = 5  # High-power
        elif explosive_data['velocity'] > 3000:
            velocity_modifier = 2  # Medium-power
        
        # Apply velocity modifier to base range
        base_range = (
            min(95, base_range[0] + velocity_modifier),
            min(100, base_range[1] + velocity_modifier)
        )
        
        # Generate correlated sensor readings
        fume = np.random.uniform(*base_range)
        metal = np.random.uniform(base_range[0] - 10, base_range[1])
        gpr = np.random.uniform(base_range[0] - 15, base_range[1] - 5)
        ground_cv = np.random.uniform(base_range[0] - 10, base_range[1] - 10)
        drone_cv = np.random.uniform(base_range[0] - 5, base_range[1] - 10)
        disturbance = np.random.uniform(base_range[0] - 20, base_range[1] - 15)
        thermal = np.random.uniform(base_range[0] - 15, base_range[1] - 20)
        
        # Clip to valid range
        sensors = {
            'fume': np.clip(fume, 0, 100),
            'metal': np.clip(metal, 0, 100),
            'gpr': np.clip(gpr, 0, 100),
            'ground_cv': np.clip(ground_cv, 0, 100),
            'drone_cv': np.clip(drone_cv, 0, 100),
            'disturbance': np.clip(disturbance, 0, 100),
            'thermal': np.clip(thermal, 0, 100)
        }
        
        # Calculate probability
        weights = {
            'fume': 0.25, 'metal': 0.20, 'gpr': 0.20,
            'ground_cv': 0.10, 'drone_cv': 0.10,
            'disturbance': 0.10, 'thermal': 0.05
        }
        probability = sum(sensors[k] * weights[k] for k in sensors.keys())
        
        # Select location
        location = random.choice(locations)
        state = location_state_map.get(location, 'North-East India')
        
        # Action recommendation
        actions = {
            'CRITICAL': 'Immediate evacuation and EOD deployment',
            'HIGH': 'Route diversion and increased surveillance',
            'MODERATE': 'Enhanced monitoring and caution advised',
            'LOW': 'Standard patrol procedures'
        }
        
        record = {
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Location': location,
            'State': state,  # Added State column
            'Threat_Level': threat_level,
            'Threat_Probability': round(probability, 2),  # Changed from Confidence
            'Fume_Detection': round(sensors['fume'], 2),
            'Metal_Detection': round(sensors['metal'], 2),
            'GPR_Reading': round(sensors['gpr'], 2),
            'Ground_CV': round(sensors['ground_cv'], 2),
            'Drone_CV': round(sensors['drone_cv'], 2),
            'Disturbance': round(sensors['disturbance'], 2),
            'Thermal': round(sensors['thermal'], 2),
            'Explosive_Type': explosive,
            'Fume_Signature': explosive_data['fume_color'],
            'Danger_Level': explosive_data['danger'],
            'Detonation_Velocity': explosive_data['velocity'],
            'Density': explosive_data.get('density', 0),
            'Brisance': explosive_data.get('brisance', 'Unknown'),
            'Explosive_Class': explosive_data.get('type', 'Unknown'),
            'Action': actions[threat_level]
        }
        
        records.append(record)
        
        if (i + 1) % 100 == 0:
            print(f"  ✓ Generated {i + 1}/{num_records} records...")
    
    # Create DataFrame
    df = pd.DataFrame(records)
    df = df.sort_values('Timestamp')
    
    # Save to CSV in parent directory (root)
    output_file = '../netra_threat_log.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Successfully generated {num_records} threat analyses!")
    print(f"📁 Saved to: {output_file}")
    print(f"\n📊 Threat Distribution:")
    print(f"   CRITICAL: {threat_distribution['CRITICAL']} ({threat_distribution['CRITICAL']/num_records*100:.1f}%)")
    print(f"   HIGH: {threat_distribution['HIGH']} ({threat_distribution['HIGH']/num_records*100:.1f}%)")
    print(f"   MODERATE: {threat_distribution['MODERATE']} ({threat_distribution['MODERATE']/num_records*100:.1f}%)")
    print(f"   LOW: {threat_distribution['LOW']} ({threat_distribution['LOW']/num_records*100:.1f}%)")
    print(f"\n📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({days_back} days)")
    print(f"🔬 Explosive Database: {len(EXPLOSIVE_TYPES)} types integrated")
    
    # Show explosive type distribution
    explosive_counts = df['Explosive_Type'].value_counts().head(10)
    print(f"\n💣 Top 10 Detected Explosive Types:")
    for exp_type, count in explosive_counts.items():
        print(f"   {exp_type}: {count} detections")
    
    # Show danger level distribution
    danger_dist = df['Danger_Level'].value_counts()
    print(f"\n⚠️ Explosive Danger Levels:")
    for danger, count in danger_dist.items():
        print(f"   {danger}: {count} ({count/num_records*100:.1f}%)")
    
    return df

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    num_records = 1000
    days_back = 60
    
    if len(sys.argv) > 1:
        try:
            num_records = int(sys.argv[1])
        except:
            print(f"⚠️ Invalid record count, using default: 1000")
    
    if len(sys.argv) > 2:
        try:
            days_back = int(sys.argv[2])
        except:
            print(f"⚠️ Invalid days count, using default: 60")
    
    print(f"🚀 Generating {num_records} records over {days_back} days...")
    df = generate_enhanced_threats(num_records=num_records, days_back=days_back)
    print("\n🎉 Data generation complete!")
    print(f"\n💡 Tip: Run with custom parameters: python generate_enhanced_data.py 1500 90")
