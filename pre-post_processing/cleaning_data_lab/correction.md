# Exercise Correction: Data Cleaning Lab
**Student:** Blanca Faura  
**Exercise:** E-commerce Customer Orders Data Cleaning  
**Date:** December 12, 2025

---

## Overall Assessment

**Grade: 9.2/10**

This is an excellent data cleaning exercise with professional structure, comprehensive data quality testing, and well-implemented cleaning strategies. The code demonstrates understanding of pandas operations, data quality principles, and software engineering best practices.

The minor issues identified are nitpicks rather than fundamental problems. The code runs successfully, produces reliable results, and includes comprehensive validation metrics.

---

## Strengths

### 1. **Outstanding Code Structure** 
- Clean, professional organization with clear sections.
- Excellent use of docstrings and comments.
- Consistent formatting and naming conventions.
- Proper separation of concerns with dedicated quality test functions.

### 2. **Comprehensive Data Quality Framework**
- **Exceptional:** Implemented dedicated test functions for each quality dimension:
  - `completeness()` - Email & Phone coverage
  - `accuracy_age()` - Age validation within realistic range
  - `validity_email()` - Email format validation with regex
  - `consistency_country()` - Country name standardization
  - `uniqueness_order()` - OrderID uniqueness check
- Before/after quality metrics comparison
- Professional use of percentage-based quality scores

### 3. **Robust Data Cleaning Implementation** 
- **Type conversion:** Proper use of `pd.to_datetime()` and `pd.to_numeric()` with error handling
- **Text normalization:** Consistent `.strip()`, `.title()`, `.lower()`, `.upper()` usage
- **Country standardization:** Comprehensive mapping for US/UK variations
- **Missing value handling:** Intelligent use of median for numeric fields
- **Validation functions:** Custom regex-based email and phone validation
- **Duplicate removal:** Proper handling of duplicate OrderIDs

---

## Minor Issues Found

### 1. **Unused Import** (-0.2 points)
```python
import os  # This is imported but never used
```

**Recommendation:** Remove unused imports to keep code clean:
```python
# Remove
import os
```

---

### 2. **Age Validation Logic Inconsistency** (-0.3 points)

**Issue:** The accuracy test allows ages 0-120, but the cleaning logic uses different range:

```python
# In accuracy_age() function
age.between(0, 120, inclusive="both")  # 0-120 is valid

# But in cleaning:
df.loc[(df['CustomerAge'] < 0) | (df['CustomerAge'] > 120), 'CustomerAge'] = median_age
# This allows age = 120 but rejects age = 0
```

**Recommendation:** Be consistent in both places:
```python
# In accuracy test (more realistic)
def accuracy_age(df):
    age = pd.to_numeric(df['CustomerAge'], errors='coerce')
    return 100 * age.between(1, 120, inclusive="both").mean()

# In cleaning (match the test)
df.loc[(df['CustomerAge'] <= 0) | (df['CustomerAge'] > 120), 'CustomerAge'] = median_age
```

---

### 3. **Completeness Test Logic** (-0.3 points)

**Issue:** The completeness test checks for both Email AND Phone before cleaning, but after cleaning both are filled, making the test less meaningful:

```python
def completeness(df):
    return 100 * df[['Email', 'Phone']].notnull().all(axis=1).mean()
    # all(axis=1) means BOTH must be non-null

# But in cleaning, you fill missing values:
df['Phone'] = df['Phone'].fillna('UNKNOWN')
df['Email'] = df['Email'].fillna('unknown@email.com')
```

**Recommendation:** Either:
1. Test completeness BEFORE imputation, or
2. Change the test to check for meaningful values (not 'UNKNOWN' or 'unknown@email.com')

```python
def completeness(df):
    # Check for meaningful values, not just non-null
    valid_phone = df['Phone'].notna() & (df['Phone'] != 'UNKNOWN') & (df['Phone'] != 'invalid_phone')
    valid_email = df['Email'].notna() & (~df['Email'].isin(['unknown@email.com', 'invalid@email.com']))
    return 100 * (valid_phone | valid_email).mean()  # At least one is valid
```

---

### 4. **Phone Validation Pattern** (-0.2 points)

**Issue:** The phone validation pattern might be too permissive:

```python
pattern = r'^\+?\d[\d\s-]{6,}$'
# This matches: "+1234567", "1 2 3 4 5 6 7", "1-------"
```

**Recommendation:** Use a more robust pattern:
```python
def validate_phone(phone):
    if pd.isna(phone) or phone == 'UNKNOWN':
        return phone
    # Remove spaces and dashes, then check if 7-15 digits
    cleaned = re.sub(r'[\s-]', '', str(phone))
    pattern = r'^\+?\d{7,15}$'
    return phone if re.match(pattern, cleaned) else 'invalid_phone'
```

---

## Suggestions for Improvement

### 1. **Add Data Type Validation in Summary**
```python
# Add to summary section
print("\nData Type Validation:")
print(f"OrderDate is datetime: {pd.api.types.is_datetime64_any_dtype(df['OrderDate'])}")
print(f"CustomerAge is numeric: {pd.api.types.is_numeric_dtype(df['CustomerAge'])}")
print(f"Price is numeric: {pd.api.types.is_numeric_dtype(df['Price'])}")
```

### 2. **Add Statistical Summary**
```python
# After cleaning
print("\nNumerical Columns Summary:")
print(df[['CustomerAge', 'Quantity', 'Price']].describe())

print("\nCategorical Columns Summary:")
print(f"Unique Countries: {df['Country'].nunique()} - {df['Country'].unique()}")
print(f"Order Status Distribution:\n{df['OrderStatus'].value_counts()}")
```

### 3. **Improve Date Imputation Documentation**
```python
# Nulls for OrderDate - explain the strategy
try:
    mode_date = df['OrderDate'].mode()[0]
    df['OrderDate'] = df['OrderDate'].fillna(mode_date)
    print(f"  Filled {df_raw['OrderDate'].isna().sum()} missing dates with mode: {mode_date}")
except IndexError:
    # Fallback if all dates are null
    df['OrderDate'] = df['OrderDate'].fillna(pd.to_datetime('1900-01-01'))
    print(f"  Warning: No valid dates found, using default date")
```

### 4. **Add Timeliness Dimension**
Many data quality frameworks include timeliness. Consider adding:
```python
def timeliness_orders(df):
    # Check if orders are from expected timeframe (e.g., last 2 years)
    recent_date = pd.Timestamp.now() - pd.DateOffset(years=2)
    valid_dates = df['OrderDate'] >= recent_date
    return 100 * valid_dates.mean()
```

---

