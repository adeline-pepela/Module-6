import pandas as pd
import sqlite3

def create_sample_csv():
    # Connect to the backend database
    conn = sqlite3.connect('backend/churn_prediction.db')
    
    # Get 10 random customers
    query = """
    SELECT pid, crm_pid_value_segment, effective_segment, billing_zip, ka_name,
           active_subscribers, not_active_subscribers, suspended_subscribers, 
           total_subs, avg_mobile_revenue, avg_fix_revenue, arpu
    FROM customers
    ORDER BY RANDOM()
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    
    # Rename columns to match expected format
    df = df.rename(columns={
        'pid': 'PID',
        'crm_pid_value_segment': 'CRM_PID_Value_Segment',
        'effective_segment': 'EffectiveSegment',
        'billing_zip': 'Billing_ZIP',
        'ka_name': 'KA_name',
        'active_subscribers': 'Active_subscribers',
        'not_active_subscribers': 'Not_Active_subscribers',
        'suspended_subscribers': 'Suspended_subscribers',
        'total_subs': 'Total_Subscribers',
        'avg_mobile_revenue': 'Average_Mobile_Revenue',
        'avg_fix_revenue': 'Average_Fix_Revenue',
        'arpu': 'ARPU'
    })
    
    # Convert Billing_ZIP to int
    df['Billing_ZIP'] = df['Billing_ZIP'].fillna(0).astype(int)
    df.to_csv('bulk_prediction_template.csv', index=False)
    print(f"✓ Created template with {len(df)} real customers")
    print(f"✓ File: bulk_prediction_template.csv")
    
    conn.close()

if __name__ == "__main__":
    create_sample_csv()
