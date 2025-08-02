import pandas as pd
from pathlib import Path

def save_expenses_to_csv(parsed_result, csv_path="expenses.csv") -> pd.DataFrame:
    if hasattr(parsed_result, 'expense'):
        expense_data = [e.model_dump() for e in parsed_result.expense]
    elif isinstance(parsed_result, dict) and "expense" in parsed_result:
        expense_data = [e.model_dump() if hasattr(e, "model_dump") else e for e in parsed_result["expense"]]
    else:
        raise ValueError("Invalid parsed result format")

    new_df = pd.DataFrame(expense_data)
    csv_file = Path(csv_path)

    if csv_file.exists() and csv_file.stat().st_size > 0:
        existing_df = pd.read_csv(csv_file, parse_dates=["date"])
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    updated_df["date"] = pd.to_datetime(updated_df["date"], format='mixed', dayfirst=True)
    updated_df = updated_df.sort_values(by="date").reset_index(drop=True)
    updated_df.to_csv(csv_file, index=False)

    return updated_df
