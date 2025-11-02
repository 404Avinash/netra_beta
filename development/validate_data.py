"""
Data Validation Tool for N.E.T.R.A. System
Validates CSV data quality before deployment
"""

import pandas as pd
import os
from datetime import datetime

def validate_threat_log(file_path='../netra_threat_log.csv'):
    """
    Validate netra_threat_log.csv for quality and integrity
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    print("📊 Validating netra_threat_log.csv...")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    try:
        df = pd.read_csv(file_path)
        issues = []
        
        # Check required columns
        required_cols = [
            'Timestamp', 'Location', 'State', 'Threat_Level', 'Threat_Probability',
            'Fume_Detection', 'Metal_Detection', 'GPR_Reading',
            'Ground_CV', 'Drone_CV', 'Disturbance', 'Thermal',
            'Explosive_Type', 'Fume_Signature', 'Danger_Level', 'Action'
        ]
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing columns: {missing_cols}")
        
        # Check record count
        print(f"   Total records: {len(df)}")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate records")
        
        # Validate date range
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        date_range = (df['Timestamp'].max() - df['Timestamp'].min()).days
        print(f"   Date range: {date_range} days ({df['Timestamp'].min()} to {df['Timestamp'].max()})")
        
        # Check threat level distribution
        threat_dist = df['Threat_Level'].value_counts()
        print(f"   Threat distribution:")
        for level, count in threat_dist.items():
            pct = (count / len(df)) * 100
            print(f"      {level}: {count} ({pct:.1f}%)")
        
        # Validate sensor readings (should be 0-100)
        sensor_cols = ['Fume_Detection', 'Metal_Detection', 'GPR_Reading', 
                      'Ground_CV', 'Drone_CV', 'Disturbance', 'Thermal']
        
        for col in sensor_cols:
            if col in df.columns:
                out_of_range = ((df[col] < 0) | (df[col] > 100)).sum()
                if out_of_range > 0:
                    issues.append(f"{col}: {out_of_range} values out of range (0-100)")
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            critical_nulls = null_counts[null_counts > 0]
            if len(critical_nulls) > 0:
                issues.append(f"Null values found: {dict(critical_nulls)}")
        
        # Validate confidence scores
        if 'Confidence' in df.columns:
            avg_confidence = df['Confidence'].mean()
            print(f"   Average confidence: {avg_confidence:.2f}")
            
            if avg_confidence < 30:
                issues.append(f"Low average confidence: {avg_confidence:.2f}")
        
        # Print results
        if issues:
            print(f"\n❌ Validation failed with {len(issues)} issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("   ✅ All validation checks passed!")
            return True
            
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False

def validate_locations(file_path='../locations_northeast_india.csv'):
    """
    Validate locations_northeast_india.csv
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    print("\n📍 Validating locations_northeast_india.csv...")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    try:
        df = pd.read_csv(file_path)
        issues = []
        
        # Check required columns
        required_cols = ['Location', 'State', 'Type', 'Latitude', 'Longitude']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {missing_cols}")
        
        print(f"   Total locations: {len(df)}")
        
        # Check for duplicates
        duplicates = df['Location'].duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate location names")
        
        # Validate coordinates
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            invalid_lat = ((df['Latitude'] < -90) | (df['Latitude'] > 90)).sum()
            invalid_lon = ((df['Longitude'] < -180) | (df['Longitude'] > 180)).sum()
            
            if invalid_lat > 0:
                issues.append(f"{invalid_lat} invalid latitude values")
            if invalid_lon > 0:
                issues.append(f"{invalid_lon} invalid longitude values")
        
        # Check state distribution
        if 'State' in df.columns:
            state_dist = df['State'].value_counts()
            print(f"   States covered: {len(state_dist)}")
            for state, count in state_dist.items():
                print(f"      {state}: {count}")
        
        # Print results
        if issues:
            print(f"\n❌ Validation failed with {len(issues)} issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("   ✅ All validation checks passed!")
            return True
            
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False

def validate_sensor_readings(file_path='../sensor_readings_live.csv'):
    """
    Validate sensor_readings_live.csv
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    print("\n🔬 Validating sensor_readings_live.csv...")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    try:
        df = pd.read_csv(file_path)
        issues = []
        
        # Check required columns
        required_cols = ['Timestamp', 'Location', 'Fume_Detection', 
                        'Metal_Detection', 'GPR_Reading']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing columns: {missing_cols}")
        
        print(f"   Total readings: {len(df)}")
        
        # Validate sensor values
        sensor_cols = [col for col in df.columns if col not in ['Timestamp', 'Location']]
        
        for col in sensor_cols:
            if col in df.columns:
                out_of_range = ((df[col] < 0) | (df[col] > 100)).sum()
                if out_of_range > 0:
                    issues.append(f"{col}: {out_of_range} values out of range (0-100)")
        
        # Print results
        if issues:
            print(f"\n❌ Validation failed with {len(issues)} issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("   ✅ All validation checks passed!")
            return True
            
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False

def validate_explosive_database(file_path='../explosive_database.csv'):
    """
    Validate explosive_database.csv
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    print("\n💣 Validating explosive_database.csv...")
    
    if not os.path.exists(file_path):
        print("   ⚠️ Warning: explosive_database.csv not found (optional file)")
        return True  # Not critical
    
    try:
        df = pd.read_csv(file_path)
        issues = []
        
        print(f"   Total explosive types: {len(df)}")
        
        # Check required columns
        required_cols = ['Name', 'Fume_Color', 'Danger_Level']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {missing_cols}")
        
        # Check for empty names
        if 'Name' in df.columns:
            empty_names = df['Name'].isna().sum()
            if empty_names > 0:
                issues.append(f"{empty_names} explosives with missing names")
        
        # Print results
        if issues:
            print(f"\n❌ Validation failed with {len(issues)} issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("   ✅ All validation checks passed!")
            return True
            
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False

def run_full_validation():
    """
    Run complete validation suite
    
    Returns:
        bool: True if all validations pass
    """
    print("🔍 N.E.T.R.A. Data Validation Suite")
    print("=" * 60)
    
    results = {
        'Threat Log': validate_threat_log(),
        'Locations': validate_locations(),
        'Sensor Readings': validate_sensor_readings(),
        'Explosive Database': validate_explosive_database()
    }
    
    print("\n" + "=" * 60)
    print("📋 Validation Summary:")
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All validation checks passed! Data is ready for deployment.")
        return True
    else:
        print("\n❌ Some validation checks failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_full_validation()
    exit(0 if success else 1)
