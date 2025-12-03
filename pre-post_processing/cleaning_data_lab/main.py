"""
DATA CLEANING EXERCISE
=====================
Retrieve, explore, and clean an e-commerce customer orders dataset
"""
import os
import requests
from datetime import datetime
import pandas as pd
import io
import re

pd.set_option('future.no_silent_downcasting', True) #solve warning with emails  (boleans and NaN)

print("=" * 70)
print("DATA CLEANING EXERCISE - E-COMMERCE CUSTOMER ORDERS")
print("=" * 70)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================  
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================  
print("STEP 1: RETRIEVING DATA FROM WEB SOURCE")
print("-" * 70)

url = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"

try:
    print(f"Fetching data from: {url}")
    response = requests.get(url, timeout=10)

    print("Data fetched from web source, loading into DataFrame...")
    df_raw = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
   
    print(f"Data retrieved successfully!")
    print(f"Status Code: {response.status_code}")
    print(f"Rows: {len(df_raw)}, Columns: {len(df_raw.columns)}\n")
    print(df_raw.head())
   
except Exception as e:
    print(f"Error: {e}")
    raise e

# ============================================================================  
# STEP 2: INITIAL EXPLORATION
# ============================================================================  
print("STEP 2: INITIAL DATA EXPLORATION")
print("-" * 70)
print(f"\nDataset Shape: {df_raw.shape}")
print(f"\nColumn Names & Types:\n{df_raw.dtypes}")
print(f"\nFirst 5 Rows:\n{df_raw.head()}")
print(f"\nMissing Values:\n{df_raw.isnull().sum()}")
print(f"\nTotal Missing: {df_raw.isnull().sum().sum()}\n")

# ============================================================================  
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================  
print("STEP 3: DATA QUALITY ISSUES")
print("-" * 70)

print(f"Duplicates: {df_raw.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df_raw['OrderID'].duplicated().sum()}")

if df_raw[df_raw.duplicated(subset=['OrderID'], keep=False)].shape[0] > 0:
    print(f"\nDuplicate Records:\n{df_raw[df_raw.duplicated(subset=['OrderID'], keep=False)].sort_values('OrderID')}\n")

# ============================================================================  
# DATA QUALITY TEST FUNCTIONS
# ============================================================================  
def completeness(df):
    return 100 * df[['Email', 'Phone']].notnull().all(axis=1).mean()

def accuracy_age(df):
    # convert to number and check range 0-120
    age = pd.to_numeric(df['CustomerAge'], errors='coerce')
    return 100 * age.between(0,120, inclusive="both").mean()

def validity_email(df):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return 100 * df['Email'].str.match(pattern).fillna(False).infer_objects(copy=False).mean()

def consistency_country(df):
    valid_countries = ['USA','UNITED KINGDOM','CANADA']
    return 100 * df['Country'].isin(valid_countries).mean()

def uniqueness_order(df):
    return 100 * (~df['OrderID'].duplicated()).mean()

print("\nDATA QUALITY TESTS BEFORE CLEANING")
print("-" * 50)
print(f"Completeness (Email & Phone): {completeness(df_raw):.2f}%")
print(f"Accuracy (CustomerAge): {accuracy_age(df_raw):.2f}%")
print(f"Validity (Email format): {validity_email(df_raw):.2f}%")
print(f"Consistency (Country names): {consistency_country(df_raw):.2f}%")
print(f"Uniqueness (OrderID): {uniqueness_order(df_raw):.2f}%\n")

# ============================================================================  
# STEP 4: DATA CLEANING
# ============================================================================  
print("STEP 4: DATA CLEANING")
print("-" * 70)

df = df_raw.copy()

# Standardize column types
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
df['CustomerAge'] = pd.to_numeric(df['CustomerAge'], errors='coerce')

# Nulls for OrderDate 
try:
    mode_date = df['OrderDate'].mode()[0]
    df['OrderDate'] = df['OrderDate'].fillna(mode_date)
except IndexError:
    df['OrderDate'] = df['OrderDate'].fillna(pd.to_datetime('1900-01-01'))

# Normalize text columns
df['CustomerName'] = df['CustomerName'].str.strip().str.title()
df['Email'] = df['Email'].str.strip().str.lower()
df['Country'] = df['Country'].str.strip().str.upper()

# Standardize country names
df['Country'] = df['Country'].replace({
    'US': 'USA',
    'UNITED STATES': 'USA',
    'UNITED STATES OF AMERICA': 'USA',
    'UK': 'UNITED KINGDOM',
    'GB': 'UNITED KINGDOM',
    'CANADA': 'CANADA'
})

# Handle missing values
median_age = df['CustomerAge'].median()
df['CustomerAge'] = df['CustomerAge'].fillna(median_age)

median_price = df['Price'].median()
df['Price'] = df['Price'].fillna(median_price)

df['Phone'] = df['Phone'].fillna('UNKNOWN')
df['Email'] = df['Email'].fillna('unknown@email.com')

# Handle invalid/extreme values
df.loc[df['Quantity'] <= 0, 'Quantity'] = 1
df.loc[(df['CustomerAge'] < 0) | (df['CustomerAge'] > 120), 'CustomerAge'] = median_age
df.loc[df['Price'] <= 0, 'Price'] = median_price

# Validate emails and phone numbers
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return email if re.match(pattern, email) else 'invalid@email.com'

df['Email'] = df['Email'].apply(validate_email)

def validate_phone(phone):
    pattern = r'^\+?\d[\d\s-]{6,}$'
    return phone if re.match(pattern, phone) else 'invalid_phone'

df['Phone'] = df['Phone'].apply(validate_phone)

# Remove duplicates by OrderID
df = df.drop_duplicates(subset=['OrderID'])

print("Data cleaning completed.\n")

# ============================================================================  
# STEP 5: FINAL VALIDATION
# ============================================================================  
print("STEP 5: FINAL VALIDATION")
print("-" * 70)
print(f"Dataset Shape: {df.shape}")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Duplicate OrderIDs: {df['OrderID'].duplicated().sum()}\n")
print(df.head())

print("\nDATA QUALITY TESTS AFTER CLEANING")
print("-" * 50)
print(f"Completeness (Email & Phone): {completeness(df):.2f}%")
print(f"Accuracy (CustomerAge): {accuracy_age(df):.2f}%")
print(f"Validity (Email format): {validity_email(df):.2f}%")
print(f"Consistency (Country names): {consistency_country(df):.2f}%")
print(f"Uniqueness (OrderID): {uniqueness_order(df):.2f}%\n")

# ============================================================================  
# STEP 6: SAVE CLEANED DATA
# ============================================================================  
print("STEP 6: SAVE CLEANED DATA")
print("-" * 70)
output_file = "cleaned_orders.csv"
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to: {output_file}\n")

# ============================================================================  
# SUMMARY
# ============================================================================  
print("SUMMARY")
print("-" * 70)
print(f"Total rows after cleaning: {len(df)}")
print(f"Total missing values after cleaning: {df.isnull().sum().sum()}")
print(f"Data types:\n{df.dtypes}")

print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")