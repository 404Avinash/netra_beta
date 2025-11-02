"""
Excel Explosive Database Integration Tool
Parses DOC-20251102-WA0083.xlsx and creates explosive_database.csv
"""

import pandas as pd
import os

def parse_excel_explosives(excel_file='DOC-20251102-WA0083.xlsx'):
    """
    Parse Excel file with 47 explosive types from 3 sheets
    
    Args:
        excel_file: Path to Excel file (default in development/ folder)
    """
    print(f"📖 Reading explosive database from: {excel_file}")
    
    if not os.path.exists(excel_file):
        print(f"❌ Error: File not found: {excel_file}")
        print("   Please ensure the Excel file is in the development/ folder")
        return None
    
    all_explosives = []
    
    # Read all sheets
    try:
        sheet_names = ['Sheet1', 'Sheet2', 'Sheet3']  # Military/Common, Improvised, Additional IED
        sheet_descriptions = ['Military/Common Explosives', 'Improvised/Homemade Explosives', 'Additional IED Materials']
        
        for sheet_name, description in zip(sheet_names, sheet_descriptions):
            print(f"\n📄 Processing {description} ({sheet_name})...")
            
            try:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                print(f"   ✓ Found {len(df)} explosive types")
                
                # Process each explosive
                for idx, row in df.iterrows():
                    explosive_entry = {
                        'Name': str(row.get('Name', 'Unknown')).strip(),
                        'Synonyms': str(row.get('Synonyms', '')).strip() if pd.notna(row.get('Synonyms')) else '',
                        'Composition': str(row.get('Composition', '')).strip() if pd.notna(row.get('Composition')) else '',
                        'Physical_Appearance': str(row.get('Physical Appearance', '')).strip() if pd.notna(row.get('Physical Appearance')) else '',
                        'Density_g_cm3': float(row.get('Density', 0)) if pd.notna(row.get('Density')) and row.get('Density') != '' else 0.0,
                        'Detonation_Velocity_m_s': int(row.get('Detonation Velocity', 0)) if pd.notna(row.get('Detonation Velocity')) and row.get('Detonation Velocity') != '' else 0,
                        'Brisance': str(row.get('Brisance', 'Medium')).strip() if pd.notna(row.get('Brisance')) else 'Medium',
                        'RE_Factor': float(row.get('RE Factor', 1.0)) if pd.notna(row.get('RE Factor')) and row.get('RE Factor') != '' else 1.0,
                        'Fume_Color': str(row.get('Fume Color', 'Unknown')).strip() if pd.notna(row.get('Fume Color')) else 'Unknown',
                        'Notes': str(row.get('Notes', '')).strip() if pd.notna(row.get('Notes')) else '',
                        'Category': description
                    }
                    
                    all_explosives.append(explosive_entry)
                
            except Exception as e:
                print(f"   ⚠️ Warning: Could not read {sheet_name}: {str(e)}")
                continue
        
        # Create DataFrame
        explosives_df = pd.DataFrame(all_explosives)
        
        # Add danger classification based on detonation velocity and brisance
        def classify_danger(row):
            velocity = row['Detonation_Velocity_m_s']
            brisance = str(row['Brisance']).lower()
            
            if velocity > 7000 or 'very high' in brisance or 'high' in brisance:
                return 'Very High'
            elif velocity > 5000 or 'medium' in brisance:
                return 'High'
            elif velocity > 3000:
                return 'Medium'
            else:
                return 'Low'
        
        explosives_df['Danger_Level'] = explosives_df.apply(classify_danger, axis=1)
        
        # Save to CSV
        output_file = '../explosive_database.csv'  # Save to root, not development/
        explosives_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Successfully processed {len(explosives_df)} explosive types!")
        print(f"📁 Saved to: explosive_database.csv")
        
        # Statistics
        print(f"\n📊 Database Statistics:")
        print(f"   Total Explosives: {len(explosives_df)}")
        print(f"   Categories:")
        for category in explosives_df['Category'].unique():
            count = len(explosives_df[explosives_df['Category'] == category])
            print(f"      - {category}: {count}")
        
        print(f"\n   Danger Levels:")
        for danger in ['Very High', 'High', 'Medium', 'Low']:
            count = len(explosives_df[explosives_df['Danger_Level'] == danger])
            print(f"      - {danger}: {count}")
        
        print(f"\n   Fume Signatures:")
        fume_colors = explosives_df['Fume_Color'].unique()
        print(f"      - {len(fume_colors)} unique fume signatures detected")
        
        return explosives_df
        
    except Exception as e:
        print(f"❌ Error processing Excel file: {str(e)}")
        return None

def validate_integration():
    """
    Validate that explosive_database.csv aligns with data flow
    """
    print("\n🔍 Validating explosive database integration...")
    
    try:
        # Check if file exists
        if not os.path.exists('../explosive_database.csv'):
            print("❌ Error: explosive_database.csv not found")
            return False
        
        # Load database
        db = pd.read_csv('../explosive_database.csv')
        
        # Check required columns
        required_cols = ['Name', 'Fume_Color', 'Danger_Level', 'Detonation_Velocity_m_s']
        missing_cols = [col for col in required_cols if col not in db.columns]
        
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
            return False
        
        print(f"✅ All required columns present")
        print(f"✅ {len(db)} explosive types ready for use")
        
        # Check for empty critical fields
        empty_names = db['Name'].isna().sum()
        if empty_names > 0:
            print(f"⚠️ Warning: {empty_names} explosives with missing names")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔬 N.E.T.R.A. Explosive Database Integration")
    print("=" * 60)
    
    # Parse Excel file
    df = parse_excel_explosives('DOC-20251102-WA0083.xlsx')
    
    if df is not None:
        # Validate integration
        validate_integration()
        print("\n🎉 Integration complete!")
    else:
        print("\n❌ Integration failed. Please check the Excel file.")
