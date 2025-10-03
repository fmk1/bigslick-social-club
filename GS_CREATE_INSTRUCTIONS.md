# Create Google Sheet and connect service account

This guide shows how to create a Google Cloud service account, get credentials, and run the provided `create_gsheet.py` script to create a new Google Sheet populated with the schedule template.

1. Create a Google Cloud project (or use an existing one).
2. Enable the Google Drive API and Google Sheets API in the project.
3. Create a service account and download the JSON key file.
   - In Cloud Console: IAM & Admin -> Service accounts -> Create service account -> Grant roles: 'Editor' (or specific Drive/Sheets roles)
   - Create key -> JSON -> download file.
4. Save the JSON to your machine (e.g. `~/Downloads/bigslick-sa.json`).
5. Install Python deps in your venv: `pip install -r requirements.txt` (the repo `requirements.txt` contains gspread and google-auth).
6. Run the script to create and populate a sheet:

```bash
python create_gsheet.py --credentials ~/Downloads/bigslick-sa.json --title "Bigslick Schedule"
```

7. Script output will include the sheet URL and the Sheet ID. Copy the Sheet ID into the app Settings panel in the `Google Sheet ID` field.
8. Optionally share the sheet with the service account email (if you created the sheet manually) or let the script create the sheet under the service account's Drive.

Security notes
- Do not commit the service account JSON into the repository.
- Keep the credentials safe and rotate keys periodically.
