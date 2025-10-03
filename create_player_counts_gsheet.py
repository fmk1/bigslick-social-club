"""
Utility to create a Google Sheet for player counts and populate it from the local `player_counts_template.csv` using a service account JSON.

Usage:
  1. Create a Google Cloud service account and download the JSON key file.
  2. Share the created Google Sheet with the service account email (or let the script create a new sheet under the service account's Drive).
  3. Run: python create_player_counts_gsheet.py --credentials /path/to/service-account.json --title "Bigslick Player Counts"

This script uses `gspread` and `gspread-dataframe`.
"""
import argparse
import os
import pandas as pd

try:
    import gspread
    from gspread_dataframe import set_with_dataframe
except Exception:
    print("Please install gspread and gspread-dataframe: pip install gspread gspread-dataframe")
    raise


def create_sheet(credentials: str, title: str = "Bigslick Player Counts") -> str:
    """Create a Google Sheet and populate it with player_counts_template.csv. Returns the Sheet ID."""
    gc = gspread.service_account(filename=credentials)
    # create a new spreadsheet
    sh = gc.create(title)
    # open the first worksheet
    ws = sh.get_worksheet(0)
    # load template CSV
    df = pd.read_csv('player_counts_template.csv')
    set_with_dataframe(ws, df)
    # make the sheet readable by anyone with link (optional)
    sh.share(None, perm_type='anyone', role='reader')
    print(f"Created sheet: {sh.url}")
    return sh.id


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--credentials', '-c', required=True, help='Path to service account JSON')
    parser.add_argument('--title', '-t', default='Bigslick Player Counts', help='Google Sheet title')
    args = parser.parse_args()
    if not os.path.exists(args.credentials):
        raise SystemExit('Credentials file not found')
    sid = create_sheet(args.credentials, args.title)
    print('Sheet ID:', sid)