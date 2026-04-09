import pandas as pd
import numpy as np
pune_df = pd.read_csv("input/")

# 2. Flag the "Guard Present" days
pune_df['date_only'] = pd.to_datetime(pune_df['date created']).dt.date
pune_df['is_wednesday'] = pd.to_datetime(pune_df['date created']).dt.weekday == 2

# List of specific leave dates
leave_dates = [pd.to_datetime('2026-03-07').date(), pd.to_datetime('2026-03-17').date()]
start_date = pd.to_datetime('2026-03-04').date()

def is_guard_present(row):
    if row['date_only'] < start_date: return False
    if row['is_wednesday']: return False
    if row['date_only'] in leave_dates: return False
    return True

pune_df['guard_present'] = pune_df.apply(is_guard_present, axis=1)

# 3. Compare the metrics!
daily_stats = pune_df.groupby(['date_only', 'guard_present']).agg(
    daily_revenue=('Completed_Amount', 'sum'),
    total_initiated=('Is_Initiated', 'sum'),
    total_completed=('Is_Completed', 'sum')
).reset_index()

daily_stats['completion_rate'] = daily_stats['total_completed'] / daily_stats['total_initiated'].replace(0, 1)

# 4. Final Aggregation
print(daily_stats.groupby('guard_present')[['daily_revenue', 'completion_rate']].mean())