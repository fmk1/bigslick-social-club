"""
Utility to create a Google Sheet for the Royal Flush Jackpot amount using a service account JSON.

Usage:
  1. Create a Google Cloud service account and download the JSON key file.
  2. Run: python create_jackpot_gsheet.py --credentials /path/to/service-account.json --initial_amount 1000

This script uses `gspread`.
"""
import argparse
import os

try:
    import gspread
except Exception:
    print("Please install gspread: pip install gspread")
    raise


def create_jackpot_sheet(credentials: str, initial_amount: str = "1000") -> str:
    """Create a Google Sheet for jackpot and set initial amount in A1. Returns the Sheet ID."""
    gc = gspread.service_account(filename=credentials)
    # create a new spreadsheet
    sh = gc.create("Royal Flush Jackpot")
    # open the first worksheet
    ws = sh.get_worksheet(0)
    # set initial amount in A1
    ws.update_cell(1, 1, initial_amount)
    # make the sheet readable by anyone with link (optional)
    sh.share(None, perm_type='anyone', role='reader')
    print(f"Created jackpot sheet: {sh.url}")
    return sh.id


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--credentials', '-c', required=True, help='Path to service account JSON')
    parser.add_argument('--initial_amount', '-a', default='1000', help='Initial jackpot amount')
    args = parser.parse_args()
    if not os.path.exists(args.credentials):
        raise SystemExit('Credentials file not found')
    sid = create_jackpot_sheet(args.credentials, args.initial_amount)
    print('Jackpot Sheet ID:', sid)