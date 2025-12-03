import pandas as pd

# Define data
data = {
    "Column Name": ["referral_id", "referrer_id", "referee_id", "is_valid_referral", "rejection_reason", "reward_amount", "transaction_status"],
    "Data Type": ["String", "Integer", "Integer", "Boolean", "String", "Float", "String"],
    "Description": [
        "Unique identifier for the referral record",
        "Unique ID of the referrer",
        "Unique ID of the referee",
        "True if referral meets valid criteria, else False",
        "Reason why referral is invalid (if applicable)",
        "Reward value",
        "Transaction status (e.g., PAID)"
    ]
}

# Create DataFrame and Save
df = pd.DataFrame(data)
df.to_excel("data_dictionary.xlsx", index=False)
print("✅ Data Dictionary created: data_dictionary.xlsx")
