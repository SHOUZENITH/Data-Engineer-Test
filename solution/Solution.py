import pandas as pd
import json 
import os
from pathlib import Path

def make_table(directory_path: str) -> pd.DataFrame:
    """
    Reconstructs a table's final state from a directory of JSON event logs.
    """
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return pd.DataFrame()

    files = sorted(Path(directory_path).glob('*.json'))
    records = {}

    for file_path in files:
        with open(file_path, 'r') as f:
            event = json.load(f)
        
        record_id = event['id']
        op_type = event['op']

        if op_type == 'c':
            new_record = event['data']
            new_record['id'] = record_id
            records[record_id] = new_record
        elif op_type == 'u':
            if record_id in records:
                records[record_id].update(event['set'])
            else:
                print(f"Warning: Update event for non-existent ID {record_id} in {file_path}")

    if not records:
        return pd.DataFrame()
        
    return pd.DataFrame(list(records.values()))


def find_transactions(directory_path: str, key_field: str, id_field: str, transaction_type: str) -> list:
    """
    Scans event logs to find and extract specific transaction details.
    """
    transactions = []
    files = Path(directory_path).glob('*.json')

    for file_path in files:
        with open(file_path, 'r') as f:
            event = json.load(f)

        value = None
        if event['op'] == 'c' and key_field in event.get('data', {}):
            value = event['data'][key_field]
        elif event['op'] == 'u' and key_field in event.get('set', {}):
            value = event['set'][key_field]

        if value is not None:
            record_id = event['id']
            associated_id = record_id
            for f_inner in Path(directory_path).glob('*.json'):
                with open(f_inner, 'r') as f_read:
                    evt_inner = json.load(f_read)
                    if evt_inner.get('id') == record_id and evt_inner.get('op') == 'c':
                        associated_id = evt_inner['data'].get(id_field, record_id)
                        break
            
            transactions.append({
                "Timestamp": event['ts'],
                "Transaction_Type": transaction_type,
                "Associated_ID": associated_id,
                "Value": value
            })
            
    return transactions



# 1. make each table
print("--- Reconstructing Tables ---")
path_prefix = 'data/'
accounts_df = make_table(f'{path_prefix}accounts')
cards_df = make_table(f'{path_prefix}cards')
savings_df = make_table(f'{path_prefix}savings_accounts')

print("--- Accounts Table ---")
print(accounts_df.to_string())
print("\n" + "="*50 + "\n")
print("--- Cards Table ---")
print(cards_df.to_string())
print("\n" + "="*50 + "\n")
print("--- Saving Accounts Table ---")
print(savings_df.to_string())
print("\n" + "="*50 + "\n")


# 2. Merge tables into a denormalized view
print("--- Merging Tables ---")
merged_df = pd.merge(
    accounts_df,
    cards_df,
    on='card_id',
    how='left',
    suffixes=('_account', '_card')
)
final_df = pd.merge(
    merged_df,
    savings_df,
    on='savings_account_id',
    how='left',
    suffixes=('', '_savings')
)

print("--- Denormalized Joined Table ---")
print(final_df.to_string())
print("\n" + "="*50 + "\n")

# 3. Analyze and display transaction history
print("--- Analyzing Transaction History ---")
card_transactions = find_transactions(
    f'{path_prefix}cards', 'credit_used', 'card_id', 'Card Credit Used Set'
)
savings_transactions = find_transactions(
    f'{path_prefix}saving_accounts', 'balance', 'savings_account_id', 'Savings Balance Set'
)

# Combine, sort, and display the transactions
all_transactions = card_transactions + savings_transactions
if all_transactions:
    transactions_df = pd.DataFrame(all_transactions)
    
    # Convert Unix timestamp (milliseconds) to human-readable datetime
    transactions_df['Timestamp'] = pd.to_datetime(transactions_df['Timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Jakarta')
    
    transactions_df = transactions_df.sort_values(by="Timestamp").reset_index(drop=True)
    
    print(f"Found a total of {len(transactions_df)} transactions.")
    print("--- Transaction Details ---")
    print(transactions_df.to_string())
else:
    print("No transactions found based on the definition.")