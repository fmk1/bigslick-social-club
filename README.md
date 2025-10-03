# Bigslick

This is a minimal Streamlit app meant to run on Heroku or locally.

## Run locally

1. Create a virtual environment and activate it (example using venv):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Google Sheets Integration

The app can load the poker schedule from a Google Sheet and display player counts.

### Schedule Sheet

To create the schedule sheet:

1. Create a Google Cloud service account and download the JSON key file.
2. Run: `python create_gsheet.py --credentials /path/to/service-account.json --title "Bigslick Schedule"`
3. Set environment variable `GSHEET_ID` to the sheet ID returned.
4. Optionally set `GSHEET_SERVICE_ACCOUNT` to the path of the service account JSON.

## Deploy to Heroku

The repository includes a `Procfile` configured for Heroku. Make sure you:

- Pin a Python runtime using `runtime.txt` (optional but recommended).
- Commit `requirements.txt` with pinned versions.

Then push to a Heroku app using Git.

## Notes

- Logo image is in `images/logo.jpg`.
- To change Streamlit settings, edit `app.py` or provide a `.streamlit/config.toml` file.
