import pandas as pd
import os
import sys

# Setup Paths
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def main():
    print("--- Starting ETL Process ---")

    # Load Data safely
    def load(name):
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path): return pd.read_csv(path)
        print(f"Warning: {name} not found.")
        return pd.DataFrame()

    print("1. Loading Data...")
    referrals = load('user_referrals.csv')
    logs = load('user_logs.csv')
    trans = load('paid_transactions.csv')
    rewards = load('referral_rewards.csv')

    if referrals.empty:
        print("❌ Error: No referral data found.")
        return

    # --- THE FIX: FORCE TYPES TO NUMERIC ---
    print("   -> Fixing ID data types...")
    # Convert all ID columns to numeric, turning bad values (like strings) into NaN
    referrals['referrer_id'] = pd.to_numeric(referrals['referrer_id'], errors='coerce')
    referrals['referee_id'] = pd.to_numeric(referrals['referee_id'], errors='coerce')
    referrals['transaction_id'] = pd.to_numeric(referrals['transaction_id'], errors='coerce')
    referrals['referral_reward_id'] = pd.to_numeric(referrals['referral_reward_id'], errors='coerce')
    
    logs['user_id'] = pd.to_numeric(logs['user_id'], errors='coerce')
    trans['transaction_id'] = pd.to_numeric(trans['transaction_id'], errors='coerce')
    rewards['id'] = pd.to_numeric(rewards['id'], errors='coerce')

    # Join Tables
    print("2. Joining tables...")
    # Now that types match, these merges will work
    df = referrals.merge(logs, left_on='referrer_id', right_on='user_id', how='left', suffixes=('', '_referrer'))
    df = df.merge(logs, left_on='referee_id', right_on='user_id', how='left', suffixes=('_referrer', '_referee'))
    df = df.merge(trans, on='transaction_id', how='left')
    df = df.merge(rewards, left_on='referral_reward_id', right_on='id', how='left', suffixes=('', '_reward'))

    # Validation Logic
    print("3. Validating data...")
    def validate(row):
        # 1. Check PAID status
        if str(row.get('transaction_status', '')).upper() != 'PAID': return False, "Not Paid"
        
        # 2. Check Date Order
        try:
            t_date = pd.to_datetime(row.get('transaction_at'))
            r_date = pd.to_datetime(row.get('referral_at'))
            if pd.notna(t_date) and pd.notna(r_date):
                if t_date < r_date: return False, "Transaction before Referral"
        except: pass
        
        # 3. Check Reward
        val = row.get('reward_value') if 'reward_value' in row else row.get('reward_amount')
        if pd.isna(val): return False, "No Reward"
        
        return True, "Valid"

    results = df.apply(validate, axis=1)
    df['is_valid_referral'] = [x[0] for x in results]
    df['rejection_reason'] = [x[1] for x in results]

    # Save Output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'final_marketing_report.csv')
    
    # Fix column name if needed
    if 'reward_value' in df.columns: 
        df.rename(columns={'reward_value': 'reward_amount'}, inplace=True)
    
    cols = ['referral_id', 'referrer_id', 'referee_id', 'is_valid_referral', 'rejection_reason', 'reward_amount', 'transaction_status']
    save_cols = [c for c in cols if c in df.columns]
    
    df[save_cols].to_csv(out_path, index=False)
    print(f"✅ Success! Report saved to: {out_path}")

if __name__ == "__main__":
    main()
