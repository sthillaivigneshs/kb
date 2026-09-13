# ============================================
# DATA CLEANING & REPORTING AUTOMATION
# Automate data cleaning and reporting workflows
# ============================================

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================
# 1. CREATE MESSY SAMPLE DATA
# ============================================

def create_messy_data():
    print("\n" + "="*60)
    print("📊 STEP 1: CREATING MESSY DATA")
    print("="*60)
    
    np.random.seed(42)
    n = 200
    
    data = {
        'Customer_ID': range(1, n + 1),
        'Name': [f'Customer_{i}' for i in range(1, n + 1)],
        'Age': np.random.randint(18, 80, n).astype(float),
        'Email': [f'customer{i}@email.com' for i in range(1, n + 1)],
        'Country': np.random.choice(['USA', 'UK', 'Canada', 'Australia', 'India'], n),
        'Purchase_Amount': np.random.uniform(10, 1000, n).round(2),
        'Quantity': np.random.randint(1, 20, n),
        'Rating': np.random.choice([1, 2, 3, 4, 5, np.nan], n).astype(float),
        'Signup_Date': pd.date_range(start='2023-01-01', periods=n, freq='D'),
    }
    
    df = pd.DataFrame(data)
    
    # INTRODUCE ISSUES
    df.loc[5:15, 'Age'] = np.nan
    df.loc[20:30, 'Email'] = np.nan
    df.loc[40:45, 'Country'] = np.nan
    
    duplicate_rows = df.iloc[50:55].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    df.loc[60:70, 'Country'] = 'usa'
    df.loc[80:90, 'Country'] = ' USA '
    df.loc[100:110, 'Country'] = 'U.S.A'
    
    df.loc[120, 'Age'] = 200
    df.loc[130, 'Purchase_Amount'] = -50
    df.loc[140, 'Quantity'] = 0
    
    df.loc[150:155, 'Email'] = 'invalid-email'
    df.loc[160:165, 'Email'] = 'CAPS@EMAIL.COM'
    
    os.makedirs('../data/raw', exist_ok=True)
    df.to_csv('../data/raw/messy_data.csv', index=False)
    
    print(f"✅ Created {len(df)} rows with intentional issues")
    print(f"✅ Missing values: {df.isnull().sum().sum()}")
    print(f"✅ Duplicates: {df.duplicated().sum()}")
    print(f"✅ Saved: data/raw/messy_data.csv")
    
    return df

# ============================================
# 2. DATA PROFILING
# ============================================

def profile_data(df):
    print("\n" + "="*60)
    print("🔍 STEP 2: DATA PROFILING")
    print("="*60)
    
    print(f"\n📌 Shape: {df.shape}")
    print(f"📌 Rows: {len(df)}")
    print(f"📌 Columns: {len(df.columns)}")
    
    print(f"\n📊 Missing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing_Count': missing,
        'Missing_Percent': missing_pct
    })
    print(missing_df[missing_df['Missing_Count'] > 0])
    
    print(f"\n📊 Duplicates: {df.duplicated().sum()}")
    
    print(f"\n📊 Data Types:")
    print(df.dtypes)
    
    print(f"\n📊 Statistical Summary:")
    print(df.describe().round(2))
    
    return df

# ============================================
# 3. CLEAN DATA
# ============================================

def clean_data(df):
    print("\n" + "="*60)
    print("🧹 STEP 3: CLEANING DATA")
    print("="*60)
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    cleaning_log = []
    
    duplicates_before = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    duplicates_removed = duplicates_before
    cleaning_log.append(f"Removed {duplicates_removed} duplicate rows")
    print(f"✅ Removed duplicates: {duplicates_removed}")
    
    age_missing = df_clean['Age'].isnull().sum()
    df_clean['Age'] = df_clean['Age'].fillna(df_clean['Age'].median())
    cleaning_log.append(f"Filled {age_missing} missing Age values with median")
    
    email_missing = df_clean['Email'].isnull().sum()
    df_clean['Email'] = df_clean['Email'].fillna('unknown@email.com')
    cleaning_log.append(f"Filled {email_missing} missing Emails with placeholder")
    
    country_missing = df_clean['Country'].isnull().sum()
    df_clean['Country'] = df_clean['Country'].fillna(df_clean['Country'].mode()[0])
    cleaning_log.append(f"Filled {country_missing} missing Country values with mode")
    
    rating_missing = df_clean['Rating'].isnull().sum()
    df_clean['Rating'] = df_clean['Rating'].fillna(df_clean['Rating'].median())
    cleaning_log.append(f"Filled {rating_missing} missing Ratings with median")
    
    print(f"✅ Handled missing values: {age_missing + email_missing + country_missing + rating_missing}")
    
    df_clean['Country'] = df_clean['Country'].str.strip().str.title()
    df_clean['Country'] = df_clean['Country'].replace({
        'U.S.A': 'USA',
        'Usa': 'USA',
        'Uk': 'UK'
    })
    cleaning_log.append("Standardized Country names (trim, title case, fix formats)")
    print(f"✅ Standardized Country: {df_clean['Country'].unique().tolist()}")
    
    invalid_age = (df_clean['Age'] > 100).sum()
    df_clean.loc[df_clean['Age'] > 100, 'Age'] = df_clean['Age'].median()
    cleaning_log.append(f"Fixed {invalid_age} invalid ages (>100)")
    
    negative_purchase = (df_clean['Purchase_Amount'] < 0).sum()
    df_clean.loc[df_clean['Purchase_Amount'] < 0, 'Purchase_Amount'] = df_clean['Purchase_Amount'].median()
    cleaning_log.append(f"Fixed {negative_purchase} negative Purchase amounts")
    
    zero_qty = (df_clean['Quantity'] <= 0).sum()
    df_clean.loc[df_clean['Quantity'] <= 0, 'Quantity'] = 1
    cleaning_log.append(f"Fixed {zero_qty} invalid quantities (<=0)")
    
    print(f"✅ Fixed invalid values: {invalid_age + negative_purchase + zero_qty}")
    
    df_clean['Email'] = df_clean['Email'].str.lower().str.strip()
    df_clean['Email_Valid'] = df_clean['Email'].str.contains('@', na=False)
    invalid_emails = (~df_clean['Email_Valid']).sum()
    cleaning_log.append(f"Standardized emails (lowercase, trim)")
    print(f"✅ Standardized emails: {invalid_emails} invalid flagged")
    
    df_clean['Signup_Month'] = pd.to_datetime(df_clean['Signup_Date']).dt.month_name()
    df_clean['Signup_Year'] = pd.to_datetime(df_clean['Signup_Date']).dt.year
    df_clean['Total_Value'] = (df_clean['Purchase_Amount'] * df_clean['Quantity']).round(2)
    cleaning_log.append("Added derived columns: Signup_Month, Signup_Year, Total_Value")
    
    os.makedirs('../data/cleaned', exist_ok=True)
    df_clean.to_csv('../data/cleaned/cleaned_data.csv', index=False)
    
    print(f"\n📊 Summary:")
    print(f"   Rows BEFORE: {initial_rows}")
    print(f"   Rows AFTER:  {len(df_clean)}")
    print(f"   Columns:     {len(df_clean.columns)}")
    print(f"✅ Saved: data/cleaned/cleaned_data.csv")
    
    return df_clean, cleaning_log

# ============================================
# 4. VISUALIZE CLEANING RESULTS
# ============================================

def visualize_results(df_clean):
    print("\n" + "="*60)
    print("📊 STEP 4: CREATING VISUALIZATIONS")
    print("="*60)
    
    fig = plt.figure(figsize=(18, 12))
    
    ax1 = plt.subplot(3, 3, 1)
    ax1.hist(df_clean['Age'], bins=20, color='#2E86AB', edgecolor='black')
    ax1.set_title('Age Distribution', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    
    ax2 = plt.subplot(3, 3, 2)
    country_counts = df_clean['Country'].value_counts()
    ax2.bar(country_counts.index, country_counts.values, 
            color='#E63946', edgecolor='black')
    ax2.set_title('Country Distribution', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Country')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax3 = plt.subplot(3, 3, 3)
    ax3.hist(df_clean['Purchase_Amount'], bins=20, 
             color='#06A77D', edgecolor='black')
    ax3.set_title('Purchase Amount Distribution', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Purchase Amount ($)')
    ax3.set_ylabel('Frequency')
    ax3.grid(True, alpha=0.3)
    
    ax4 = plt.subplot(3, 3, 4)
    rating_counts = df_clean['Rating'].value_counts().sort_index()
    ax4.bar(rating_counts.index.astype(str), rating_counts.values,
            color='#F18F01', edgecolor='black')
    ax4.set_title('Rating Distribution', fontsize=13, fontweight='bold')
    ax4.set_xlabel('Rating')
    ax4.set_ylabel('Count')
    ax4.grid(True, alpha=0.3, axis='y')
    
    ax5 = plt.subplot(3, 3, 5)
    ax5.hist(df_clean['Quantity'], bins=15, color='#9B5DE5', edgecolor='black')
    ax5.set_title('Quantity Distribution', fontsize=13, fontweight='bold')
    ax5.set_xlabel('Quantity')
    ax5.set_ylabel('Frequency')
    ax5.grid(True, alpha=0.3)
    
    ax6 = plt.subplot(3, 3, 6)
    monthly_signups = df_clean.groupby('Signup_Month').size()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_signups = monthly_signups.reindex([m for m in month_order if m in monthly_signups.index])
    ax6.plot(monthly_signups.index, monthly_signups.values, 
             marker='o', linewidth=2, markersize=8, color='#00BBF9')
    ax6.set_title('Signups by Month', fontsize=13, fontweight='bold')
    ax6.set_xlabel('Month')
    ax6.set_ylabel('Signups')
    ax6.tick_params(axis='x', rotation=45)
    ax6.grid(True, alpha=0.3)
    
    ax7 = plt.subplot(3, 3, 7)
    country_avg = df_clean.groupby('Country')['Purchase_Amount'].mean().sort_values()
    ax7.barh(country_avg.index, country_avg.values, 
             color='#F15BB5', edgecolor='black')
    ax7.set_title('Avg Purchase by Country', fontsize=13, fontweight='bold')
    ax7.set_xlabel('Average Amount ($)')
    ax7.grid(True, alpha=0.3, axis='x')
    
    ax8 = plt.subplot(3, 3, 8)
    ax8.hist(df_clean['Total_Value'], bins=20, 
             color='#00F5D4', edgecolor='black')
    ax8.set_title('Total Transaction Value', fontsize=13, fontweight='bold')
    ax8.set_xlabel('Total Value ($)')
    ax8.set_ylabel('Frequency')
    ax8.grid(True, alpha=0.3)
    
    ax9 = plt.subplot(3, 3, 9)
    corr_cols = ['Age', 'Purchase_Amount', 'Quantity', 'Rating', 'Total_Value']
    corr_matrix = df_clean[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', 
                fmt='.2f', ax=ax9, cbar=True)
    ax9.set_title('Correlation Matrix', fontsize=13, fontweight='bold')
    
    plt.suptitle('Data Cleaning & Reporting Dashboard', 
                 fontsize=18, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    os.makedirs('../reports', exist_ok=True)
    plt.savefig('../reports/summary_charts.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Saved: reports/summary_charts.png")
    
    return fig

# ============================================
# 5. GENERATE EXCEL REPORT
# ============================================

def generate_excel_report(df_raw, df_clean, cleaning_log):
    print("\n" + "="*60)
    print("📄 STEP 5: GENERATING EXCEL REPORT")
    print("="*60)
    
    os.makedirs('../reports', exist_ok=True)
    report_path = '../reports/cleaning_report.xlsx'
    
    with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
        
        log_df = pd.DataFrame({
            'Step': range(1, len(cleaning_log) + 1),
            'Action': cleaning_log
        })
        log_df.to_excel(writer, sheet_name='Cleaning_Log', index=False)
        
        comparison = pd.DataFrame({
            'Metric': ['Rows', 'Columns', 'Missing Values', 'Duplicates'],
            'Before': [
                len(df_raw),
                len(df_raw.columns),
                df_raw.isnull().sum().sum(),
                df_raw.duplicated().sum()
            ],
            'After': [
                len(df_clean),
                len(df_clean.columns),
                df_clean.isnull().sum().sum(),
                df_clean.duplicated().sum()
            ]
        })
        comparison.to_excel(writer, sheet_name='Before_vs_After', index=False)
        
        df_clean.head(100).to_excel(writer, sheet_name='Cleaned_Data', index=False)
        
        summary_stats = df_clean[['Age', 'Purchase_Amount', 'Quantity', 
                                   'Rating', 'Total_Value']].describe().round(2)
        summary_stats.to_excel(writer, sheet_name='Summary_Stats')
        
        country_analysis = df_clean.groupby('Country').agg({
            'Customer_ID': 'count',
            'Purchase_Amount': ['mean', 'sum'],
            'Rating': 'mean'
        }).round(2)
        country_analysis.columns = ['Customers', 'Avg_Purchase', 'Total_Revenue', 'Avg_Rating']
        country_analysis.to_excel(writer, sheet_name='Country_Analysis')
    
    print(f"✅ Report saved: reports/cleaning_report.xlsx")
    print(f"✅ 5 sheets: Cleaning_Log, Before_vs_After, Cleaned_Data, Summary_Stats, Country_Analysis")
    
    return report_path

# ============================================
# 6. PRINT FINAL REPORT
# ============================================

def print_final_report(df_raw, df_clean, cleaning_log):
    print("\n" + "="*70)
    print("📋 FINAL CLEANING REPORT")
    print("="*70)
    
    print(f"\n📊 Data Overview:")
    print(f"   Original rows:  {len(df_raw)}")
    print(f"   Cleaned rows:   {len(df_clean)}")
    print(f"   Rows removed:   {len(df_raw) - len(df_clean)}")
    
    print(f"\n📊 Cleaning Actions:")
    for i, action in enumerate(cleaning_log, 1):
        print(f"   {i}. {action}")
    
    print(f"\n📊 Data Quality:")
    print(f"   Missing values (before): {df_raw.isnull().sum().sum()}")
    print(f"   Missing values (after):  {df_clean.isnull().sum().sum()}")
    print(f"   Duplicates (before):     {df_raw.duplicated().sum()}")
    print(f"   Duplicates (after):      {df_clean.duplicated().sum()}")
    
    print(f"\n📊 Cleaned Data Summary:")
    print(f"   Countries:  {df_clean['Country'].nunique()}")
    print(f"   Avg Age:    {df_clean['Age'].mean():.1f}")
    print(f"   Avg Rating: {df_clean['Rating'].mean():.2f}/5")
    print(f"   Total Revenue: ${df_clean['Total_Value'].sum():,.2f}")

# ============================================
# 7. MAIN EXECUTION
# ============================================

def main():
    print("\n" + "="*70)
    print("🚀 DATA CLEANING & REPORTING AUTOMATION")
    print("="*70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    os.makedirs('../data/raw', exist_ok=True)
    os.makedirs('../data/cleaned', exist_ok=True)
    os.makedirs('../reports', exist_ok=True)
    
    df_raw = create_messy_data()
    profile_data(df_raw)
    df_clean, cleaning_log = clean_data(df_raw)
    visualize_results(df_clean)
    report_path = generate_excel_report(df_raw, df_clean, cleaning_log)
    print_final_report(df_raw, df_clean, cleaning_log)
    
    print("\n" + "="*70)
    print("✅ DATA CLEANING PIPELINE COMPLETE!")
    print("="*70)
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📁 Output Files:")
    print("   📊 data/raw/messy_data.csv")
    print("   📊 data/cleaned/cleaned_data.csv")
    print("   📊 reports/summary_charts.png")
    print("   📄 reports/cleaning_report.xlsx")

if __name__ == "__main__":
    main()