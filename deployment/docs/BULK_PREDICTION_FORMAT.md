# Bulk Prediction CSV Format Guide

## Required Columns

Your CSV file must contain the following 12 columns in this exact order:

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `PID` | String | Customer Personal ID (unique identifier) | CUST001 |
| `CRM_PID_Value_Segment` | String | Customer value segment | High Value, Medium Value, Low Value |
| `EffectiveSegment` | String | Business segment | SME, SOHO, VSE |
| `Billing_ZIP` | Integer | Billing ZIP code | 100, 200, 300 |
| `KA_name` | String | Key Account Manager name | John Kamau, Mary Wanjiku |
| `Active_subscribers` | Integer | Number of active subscribers | 45, 12, 8 |
| `Not_Active_subscribers` | Float | Number of inactive subscribers | 5, 3, 2 |
| `Suspended_subscribers` | Float | Number of suspended subscribers | 2, 1, 0 |
| `Total_Subscribers` | Integer | Total number of subscribers | 50, 15, 10 |
| `Average_Mobile_Revenue` | Float | Average mobile revenue (KES) | 125000.50 |
| `Average_Fix_Revenue` | Float | Average fixed line revenue (KES) | 35000.00 |
| `ARPU` | Float | Average Revenue Per User (KES) | 3200.00 |

## Important Notes

1. **Header Row Required**: First row must contain column names exactly as shown above
2. **No Missing Values**: All fields must have values (no empty cells)
3. **Unique PIDs**: Each PID must be unique in the file
4. **Numeric Formats**: Use decimal point (.) for floats, no commas in numbers
5. **File Encoding**: UTF-8 encoding recommended
6. **File Size**: Maximum 10,000 rows per upload

## Value Segment Options
- High Value
- Medium Value  
- Low Value

## Effective Segment Options
- SME (Small and Medium Enterprises)
- SOHO (Small Office Home Office)
- VSE (Very Small Enterprises)

## Sample CSV Content

```csv
PID,CRM_PID_Value_Segment,EffectiveSegment,Billing_ZIP,KA_name,Active_subscribers,Not_Active_subscribers,Suspended_subscribers,Total_Subscribers,Average_Mobile_Revenue,Average_Fix_Revenue,ARPU
CUST001,High Value,SME,100,John Kamau,45,5,2,50,125000.50,35000.00,3200.00
CUST002,Medium Value,SOHO,200,Mary Wanjiku,12,3,1,15,45000.00,12000.00,3800.00
CUST003,Low Value,VSE,300,Peter Omondi,8,2,0,10,28000.00,8000.00,3600.00
```

## Output Format

After processing, you'll receive a CSV file with these additional columns:

- `Churn_Probability`: Predicted probability of churn (0.0 to 1.0)
- `Risk_Level`: Risk category (Low, Medium, High, Ultra High)
- `Top_Driver_1`: Most important churn factor
- `Top_Driver_2`: Second most important churn factor
- `Top_Driver_3`: Third most important churn factor
- `Recommended_Action`: Suggested retention strategy

## How to Use

1. Download the template file: `bulk_prediction_template.csv`
2. Fill in your customer data following the format
3. Upload the file in the "Predict" page
4. Click "Process Bulk Predictions"
5. Download the results with predictions and recommendations
