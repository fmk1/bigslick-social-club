import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timezone, timedelta

import pandas as pd
try:
	import gspread
	from gspread import get_as_dataframe, set_with_dataframe
	GSPREAD_AVAILABLE = True
except Exception:
	GSPREAD_AVAILABLE = False
import streamlit as st
try:
	from PIL import Image
	PIL_AVAILABLE = True
except Exception:
	PIL_AVAILABLE = False


st.set_page_config(page_title="Bigslick Social Club", layout="wide")

LOGO_PATH = "images/logo.png"
HEADER_PATH = "images/header.jpg"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSePm_b1oBvdNfM67ZvrDJJjH0qibHVboS0yEJ1ON6VnRj-h6A/viewform?usp=dialog"

# --- Styling: dark poker themed background with blue accents and symbols
st.markdown(
		"""
			<style>
				/* Page background and global text color - dark blue theme with lighter radial gradient pattern */
				.stApp, .reportview-container .main, section.main { 
					background: radial-gradient(ellipse at center, #0055AA 0%, #004477 50%, #003355 100%), 
						radial-gradient(circle at 20% 30%, rgba(255,215,0,0.05) 0%, transparent 40%), 
						radial-gradient(circle at 80% 70%, rgba(0,85,170,0.05) 0%, transparent 40%),
						url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Ctext x='20' y='30' font-size='24' fill='rgba(255,215,0,0.1)' text-anchor='middle'%3E♠%3C/text%3E%3C/svg%3E"); 
					background-size: 100% 100%, 200px 200px, 150px 150px, 40px 40px;
					background-position: center, 20% 30%, 80% 70%, 0 0;
					background-repeat: no-repeat, repeat, repeat, repeat;
					animation: backgroundShift 10s ease-in-out infinite;
					color: #ffffff; 
					font-family: 'Arial', sans-serif;
				}
				@keyframes backgroundShift {
					0% { background-position: center, 20% 30%, 80% 70%, 0 0; }
					50% { background-position: center, 25% 35%, 85% 75%, 5px 5px; }
					100% { background-position: center, 20% 30%, 80% 70%, 0 0; }
				}
				.stApp, .stApp * { color: #ffffff !important; }

			/* Header - Casino neon sign effect */
			.club-header { display:flex; align-items:center; gap:16px; }
			.club-title {
				font-size:32px;
				font-weight:700;
				color:#ffffff;
				font-family: 'Playfair Display', serif;
				text-shadow:
					0 0 5px #ff0000,
					0 0 10px #ff0000,
					0 0 15px #ff0000,
					0 0 20px #ff0000,
					0 0 35px #ff0000,
					0 0 40px #ff0000;
				animation: neonFlicker 2s infinite alternate;
			}
			@keyframes neonFlicker {
				0%, 18%, 22%, 25%, 53%, 57%, 100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000, 0 0 15px #ff0000, 0 0 20px #ff0000, 0 0 35px #ff0000, 0 0 40px #ff0000; }
				20%, 24%, 55% { text-shadow: none; }
			}
			.club-sub { color:#cccccc; margin-top:-6px }

			/* Tournament card - enhanced poker card with dealing animation */
			.tournament-card {
				background: linear-gradient(180deg,#003366,#004080);
				border-radius:16px;
				padding:16px;
				margin-bottom:16px;
				box-shadow: 0 8px 24px rgba(0,0,0,0.6), 0 0 12px rgba(0,85,170,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
				position: relative;
				transition: transform 0.3s ease, box-shadow 0.3s ease;
				animation: cardDeal 0.8s ease-out;
				border: 2px solid transparent;
				background-clip: padding-box;
			}
			@keyframes cardDeal {
				0% { transform: rotateY(180deg) scale(0.8); opacity: 0; }
				50% { transform: rotateY(90deg) scale(1.05); opacity: 0.7; }
				100% { transform: rotateY(0deg) scale(1); opacity: 1; }
			}
			.tournament-card:hover {
				transform: translateY(-4px) scale(1.02);
				box-shadow: 0 12px 32px rgba(0,0,0,0.8), 0 0 16px rgba(0,85,170,0.6), inset 0 1px 0 rgba(255,255,255,0.2);
				border-color: #FFD700;
			}

			.tournament-meta { color:#ffffff; font-weight:600 }
			.badge { display:inline-block; background:#87CEEB; color:#000000 !important; padding:6px 10px; border-radius:999px; margin-right:8px; font-weight:700; }

			/* Expander styling - rounded, with poker theme */
			.stExpander {
				border-radius: 12px !important;
				border: 1px solid #0055aa !important;
				background: rgba(0,51,102,0.1) !important;
				margin-bottom: 12px !important;
				transition: all 0.3s ease !important;
			}
			.stExpander:hover {
				border-color: #FFD700 !important;
				box-shadow: 0 4px 12px rgba(255,215,0,0.2) !important;
			}
			.stExpander > div:first-child {
				border-radius: 12px 12px 0 0 !important;
				background: linear-gradient(90deg, #003366, #004080) !important;
				color: #ffffff !important;
				font-weight: 700 !important;
				padding: 12px 16px !important;
			}

			/* Make the Streamlit default buttons look more fun and poker-like with gold accents */
			.stButton>button {
				background: linear-gradient(90deg,#003366,#004080);
				color: #ffffff;
				border: 2px solid #FFD700;
				padding: 10px 20px;
				border-radius: 20px;
				font-weight:700;
				box-shadow: 0 4px 12px rgba(0,0,0,0.3);
				transition: all 0.2s ease;
				position: relative;
				overflow: hidden;
			}
			.stButton>button::before {
				content: '';
				position: absolute;
				top: 0;
				left: -100%;
				width: 100%;
				height: 100%;
				background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
				transition: left 0.5s;
			}
			.stButton>button:hover::before {
				left: 100%;
			}
			.stButton>button:hover {
				transform: translateY(-2px);
				box-shadow: 0 6px 16px rgba(0,0,0,0.4);
				border-color: #FFA500;
			}

			/* Subtle separators between tournaments */
			.tournament-separator {
				height: 2px;
				background: linear-gradient(90deg, transparent, #FFD700, transparent);
				margin: 20px 0;
				border-radius: 1px;
			}

				/* Small responsive tweaks for mobile */
					@media (max-width: 600px) {
						.club-title { font-size:28px; }
						.tournament-card {
							padding: 20px;
							border-radius: 20px;
							margin-bottom: 20px;
							box-shadow: 0 10px 30px rgba(0,0,0,0.7), 0 0 15px rgba(0,85,170,0.5);
						}
						.tournament-card div { font-size:16px; }
						.stExpander > div:first-child {
							padding: 16px 20px !important;
							font-size: 18px !important;
						}
						.stButton>button {
							width: 100%;
							padding: 14px 20px;
							font-size: 16px;
							border-radius: 24px;
						}
						.stApp { font-size: 16px; }
					}
				.header-title { text-align: center; }
				@media (max-width: 600px) { .header-title { font-size: 22px !important; } .stMarkdown h1 { text-align: center !important; } }

				/* Royal Flush Jackpot styling */
				.jackpot {
					text-align: center;
					margin: 20px 0;
					padding: 20px;
					background: linear-gradient(180deg, #003366, #004080);
					border-radius: 16px;
					box-shadow: 0 8px 24px rgba(0,0,0,0.6), 0 0 12px rgba(0,85,170,0.4);
					border: 2px solid transparent;
					background-clip: padding-box;
					animation: jackpotGlow 2s ease-in-out infinite alternate;
				}
				.jackpot h2 {
					color: #FFD700;
					font-family: 'Playfair Display', serif;
					text-shadow: 0 0 10px #FFD700;
					margin-bottom: 10px;
				}
				.jackpot-amount {
					font-size: 48px;
					font-weight: bold;
					color: #FFD700;
					text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700;
				}
				@keyframes jackpotGlow {
					0% { box-shadow: 0 8px 24px rgba(0,0,0,0.6), 0 0 12px rgba(0,85,170,0.4), 0 0 20px rgba(255,215,0,0.3); }
					100% { box-shadow: 0 8px 24px rgba(0,0,0,0.6), 0 0 12px rgba(0,85,170,0.4), 0 0 40px rgba(255,215,0,0.6); }
				}
		</style>
		""",
		unsafe_allow_html=True,
)# Note: header and title are rendered above (near the top) using the header image block; no additional large emoji title here.


def load_schedule(csv_url: str | None = None) -> pd.DataFrame:
	"""Load schedule from a CSV URL or local `schedule.csv`.

	Expected columns: day,time,buy_in,rebuy,starting_chips,cutoff,notes
	"""
	if csv_url:
		try:
			df = pd.read_csv(csv_url)
			return df
		except Exception as e:
			st.error(f"Failed loading schedule from URL: {e}")
	# fallback to local file
	local = "schedule.csv"
	if os.path.exists(local):
		return pd.read_csv(local)
	# empty frame with expected columns
	cols = ["day", "time", "buy_in", "rebuy", "starting_chips", "cutoff", "notes"]
	return pd.DataFrame(columns=cols)


def normalize_schedule_df(df: pd.DataFrame) -> pd.DataFrame:
	"""Normalize column names and produce the expected columns.

	This handles common column names from published sheets (case-insensitive) and
	maps them to: day,time,buy_in,rebuy,starting_chips,cutoff,notes
	"""
	if df is None or df.empty:
		return df
	# normalize column names to simple lowercase keys
	cols = {c: c.strip() for c in df.columns}
	lower_map = {c.lower().strip(): c for c in df.columns}

	def find(col_names):
		for name in col_names:
			k = name.lower()
			if k in lower_map:
				return lower_map[k]
		return None

	# mapping heuristics
	day_col = find(["day", "dayofweek", "weekday"]) or find(["Day"]) 
	time_col = find(["time", "start time", "start_time", "starttime", "start"]) or find(["Start Time"]) 
	buy_col = find(["buy_in", "buy-in", "buyin", "buy-in (usd)", "buy-in (usd)", "buy-in (amount)", "buy-in amount"]) or find(["Buy-in", "Buyin"]) 
	rebuy_col = find(["rebuy", "re-buy", "re buy"]) or find(["Rebuy"]) 
	chips_col = find(["starting_chips", "starting chips", "startingchips", "starting stack", "starting chips"]) or find(["Starting Chips"]) 
	cutoff_col = find(["cutoff", "cut-off", "cut off"]) or find(["Cut-off"]) 
	notes_col = find(["notes", "note"]) or find(["Notes"]) 
	# tournament name often exists; use it as primary note if present
	tname_col = find(["tournament name", "name", "event"]) or find(["Tournament Name"]) 

	out = pd.DataFrame()
	out['day'] = df[day_col] if day_col in df.columns else df.get('Day', df.get('day', ''))
	# use Start Time or Start
	if time_col and time_col in df.columns:
		out['time'] = df[time_col]
	else:
		out['time'] = df.get('Start Time', df.get('time', ''))
	# buy_in
	if buy_col and buy_col in df.columns:
		out['buy_in'] = df[buy_col]
	else:
		out['buy_in'] = df.get('Buy-in', df.get('Buyin', df.get('buy_in', '')))
	# rebuy
	out['rebuy'] = df[rebuy_col] if rebuy_col in df.columns else df.get('Rebuy', df.get('rebuy', ''))
	# starting chips
	out['starting_chips'] = df[chips_col] if chips_col in df.columns else df.get('Starting Chips', df.get('starting_chips', ''))
	# cutoff
	out['cutoff'] = df[cutoff_col] if cutoff_col in df.columns else df.get('Cut-off', df.get('cutoff', ''))
	# notes: combine Tournament Name and Notes if both exist
	notes_parts = []
	if tname_col and tname_col in df.columns:
		notes_parts.append(df[tname_col].astype(str))
	if notes_col and notes_col in df.columns:
		notes_parts.append(df[notes_col].astype(str))
	if notes_parts:
		# join columns with separator
		out['notes'] = notes_parts[0].fillna('')
		for part in notes_parts[1:]:
			out['notes'] = out['notes'].str.strip() + ' — ' + part.fillna('').str.strip()
	else:
		out['notes'] = df.get('Notes', df.get('notes', ''))

	# ensure columns exist
	expected = ["day", "time", "buy_in", "rebuy", "starting_chips", "cutoff", "notes"]
	for c in expected:
		if c not in out.columns:
			out[c] = ''
	return out[expected]


def load_schedule_from_gsheet(sheet_id: str, service_account_path: str | None = None) -> pd.DataFrame:
	"""Load the first worksheet of a Google Sheet into a DataFrame.

	Expects the sheet to have the same columns as `load_schedule` expects.
	If gspread isn't available or any error occurs, returns an empty DataFrame.
	"""
	if not GSPREAD_AVAILABLE:
		st.warning("gspread not available in environment — install gspread and google-auth to enable Google Sheets integration.")
		return load_schedule(None)
	try:
		# authorize
		if service_account_path:
			gc = gspread.service_account(filename=service_account_path)
		else:
			gc = gspread.oauth()
		sh = gc.open_by_key(sheet_id)
		ws = sh.get_worksheet(0)
		df = get_as_dataframe(ws, evaluate_formulas=True, skip_blank_rows=True)
		# drop fully-empty columns that gspread may create
		df = df.dropna(axis=1, how='all')
		# normalize expected columns
		expected = ["day", "time", "buy_in", "rebuy", "starting_chips", "cutoff", "notes"]
		cols = [c for c in df.columns if str(c).strip()]
		df.columns = [str(c).strip() for c in cols]
		# ensure expected columns exist (fill missing)
		for c in expected:
			if c not in df.columns:
				df[c] = ""
		return df[expected]
	except Exception as e:
		st.error(f"Failed loading Google Sheet: {e}")
		return load_schedule(None)


def load_jackpot_from_csv(csv_url: str) -> str:
	"""Load the jackpot amount from the first cell of a published Google Sheet CSV.

	Returns the value as a string, or empty string on failure.
	"""
	try:
		df = pd.read_csv(csv_url)
		if not df.empty:
			return str(df.iloc[0, 0])
		return ""
	except Exception as e:
		st.error(f"Failed loading jackpot from CSV: {e}")
		return ""


def create_sheet_from_template(service_account_path: str, title: str = "Bigslick Schedule") -> tuple[str, str]:
	"""Create a new Google Sheet under the service account, populate it with schedule_template.csv,
	and return (sheet_url, sheet_id).
	"""
	if not GSPREAD_AVAILABLE:
		raise RuntimeError("gspread not available — install gspread and google-auth")
	gc = gspread.service_account(filename=service_account_path)
	sh = gc.create(title)
	ws = sh.get_worksheet(0)
	df = pd.read_csv('schedule_template.csv')
	set_with_dataframe(ws, df)
	# make it readable by link so owner can open it quickly
	sh.share(None, perm_type='anyone', role='reader')
	return sh.url, sh.id


def append_registration_to_gsheet(sheet_id: str, registration: dict, tab_name: str = "registrations", service_account_path: str | None = None) -> bool:
	"""Append a registration dict as a new row into the specified tab in the Google Sheet.

	Returns True on success, False on failure.
	"""
	if not GSPREAD_AVAILABLE:
		st.error("gspread is not installed in the environment. Cannot append to Google Sheets.")
		return False
	try:
		if service_account_path:
			gc = gspread.service_account(filename=service_account_path)
		else:
			gc = gspread.oauth()
		sh = gc.open_by_key(sheet_id)
		try:
			ws = sh.worksheet(tab_name)
		except Exception:
			ws = sh.add_worksheet(title=tab_name, rows=1000, cols=20)
		headers = [h for h in ["timestamp", "day", "time", "name", "phone"]]
		row = [registration.get(h, "") for h in headers]
		ws.append_row(row)
		return True
	except Exception as e:
		st.error(f"Failed to append registration to Google Sheet: {e}")
		return False


def main():
	# Header rendering
	header_to_show = HEADER_PATH if os.path.exists(HEADER_PATH) else None

	if header_to_show:
		# prefer logo.png in images/, fall back to existing logo files
		logo_candidates = ["images/logo.png", "images/logo.jpg"]
		logo_to_show = next((p for p in logo_candidates if os.path.exists(p)), None)
		max_h = int(os.environ.get("HEADER_MAX_HEIGHT", 260))
		try:
			if PIL_AVAILABLE:
				img = Image.open(header_to_show)
				w, h = img.size
				if h > max_h:
					new_w = int(w * (max_h / h))
					img = img.resize((new_w, max_h), Image.LANCZOS)
				# Save a temporary resized header to a data URI so HTML will render it reliably
				import io, base64
				buf = io.BytesIO()
				img.save(buf, format="JPEG")
				data = base64.b64encode(buf.getvalue()).decode("ascii")
				header_data_uri = f"data:image/jpeg;base64,{data}"
			else:
				header_data_uri = header_to_show

			# Build HTML: show a top bar with the logo (left) and title (right), then the header image below
			import io, base64
			logo_data_uri = None
			if logo_to_show and PIL_AVAILABLE:
				try:
					logo_img = Image.open(logo_to_show)
					# resize logo to sensible height
					lh = 84
					lw, lh_orig = logo_img.size
					if lh_orig != lh:
						new_w = int(lw * (lh / lh_orig))
						logo_img = logo_img.resize((new_w, lh), Image.LANCZOS)
					buf2 = io.BytesIO()
					logo_img.save(buf2, format="PNG")
					logo_data_uri = f"data:image/png;base64,{base64.b64encode(buf2.getvalue()).decode('ascii')}"
				except Exception:
					logo_data_uri = logo_to_show
			else:
				logo_data_uri = logo_to_show

			title_text = "Bigslick Social Club"
			# Build a stacked layout:
			# 1) top bar with logo and title centered
			# 2) header image below
			top_html = ""
			# top bar with logo and title centered with gap
			top_html += "<div style='width:100%; display:flex; align-items:center; justify-content:center; gap:20px; margin-bottom:8px;'>"
			if logo_data_uri:
				top_html += f"<img src='{logo_data_uri}' style='height:60px; object-fit:contain;'/>"
			top_html += f"<div class='header-title' style='font-size:36px; font-weight:800; color:#111;'>{title_text}</div>"
			top_html += "</div>"

			# header image block
			header_html = f"<div style='width:100%; overflow:hidden; border-radius:8px; margin-bottom:16px;'><img src='{header_data_uri}' style='width:100%; max-height:{max_h}px; object-fit:cover; display:block;' /></div>"

			st.markdown(top_html + header_html, unsafe_allow_html=True)
		except Exception:
			st.markdown('<h1 style="margin:0">Bigslick Social Club</h1>', unsafe_allow_html=True)
	else:
		# fallback: display a smaller centered logo (not full-width)
		if os.path.exists(LOGO_PATH):
			st.markdown(
				f"<div style='text-align:center; margin:8px 0;'><img src='{LOGO_PATH}' style='height:84px; object-fit:contain;' /></div>",
				unsafe_allow_html=True,
			)
		else:
			st.markdown('<h1 style="margin:0">Bigslick Social Club</h1>', unsafe_allow_html=True)

	# Load and process schedule data
	df = load_schedule('https://docs.google.com/spreadsheets/d/e/2PACX-1vSeHdpSUFfU2_Lh0dGgWUc9O8lAD_wn0K_jLCoHoQh4JXWsKDGh4A6tI47YnpHMD-vDdNEWYNgmFLxy/pub?output=csv&gid=1579199027')
	# if we loaded from CSV, try normalizing columns to the app's expected schema
	try:
		df = normalize_schedule_df(df)
	except Exception:
		# if normalize fails, keep original df
		pass

	# Load jackpot amount
	jackpot_csv_url = os.getenv("JACKPOT_CSV_URL")
	jackpot = load_jackpot_from_csv(jackpot_csv_url) if jackpot_csv_url else ""

	if df.empty:
		st.info("No schedule found. Add a `schedule.csv` in the project root or provide a SCHEDULE_CSV_URL in settings.")
		st.stop()
	# normalize day ordering
	days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	df["day"] = df["day"].astype(str)
	df["day_order"] = df["day"].apply(lambda d: days_order.index(d) if d in days_order else 7)
	df = df.sort_values(["day_order", "time"]).drop(columns=["day_order"])

	# Calculate actual dates for this week
	today = datetime.now(timezone.utc)
	monday = today - timedelta(days=today.weekday())
	day_dates = {day: monday + timedelta(days=i) for i, day in enumerate(days_order)}

	grouped = {day: group for day, group in df.groupby("day")}
	today_name = datetime.now(timezone.utc).strftime("%A")

	# Navigation tabs below header
	tabs = st.tabs(["Home", "Poker Schedule", "About", "Contact"])

	with tabs[0]:
		# Home: Compact schedule preview
		st.header("Welcome to Big Slick Social Club")
		# Display Royal Flush Jackpot if available
		if jackpot:
			st.markdown(f"""
<div class="jackpot">
<h2>Royal Flush Jackpot</h2>
<div class="jackpot-amount">${jackpot}</div>
</div>
""", unsafe_allow_html=True)
		st.write("Click on any day below to see the tournament schedule for that day.")
		for day in days_order:
			if day in grouped:
				group = grouped[day]
				date_str = day_dates[day].strftime("%B %d, %Y")
				tournament_names = ", ".join(group['notes'].tolist())
				if day == today_name:
					# Today: Show full details directly without expander
					st.subheader(f"🎯 Today's Tournament - {day}, {date_str}")
					# Display tournaments in a 1-column layout
					num_cols = 1
					cols = st.columns(num_cols)
					for i, (_, row) in enumerate(group.iterrows()):
						with cols[i % num_cols]:
							tournament_title = f"{row.get('notes','')}"
							# Calculate status
							status = ""
							target_ts = ""
							try:
								time_parsed = datetime.strptime(row.get('time', ''), "%I:%M %p").time()
								tournament_dt = datetime.combine(day_dates[day], time_parsed).replace(tzinfo=timezone.utc)
								now = datetime.now(timezone.utc)
								if tournament_dt < now:
									status = "Ended"
								elif tournament_dt.date() == now.date():
									if tournament_dt > now:
										delta = tournament_dt - now
										hours, remainder = divmod(delta.seconds, 3600)
										minutes, seconds = divmod(remainder, 60)
										status = f"Starts in {hours:02d}:{minutes:02d}:{seconds:02d}"
										target_ts = str(int(tournament_dt.timestamp()))
									else:
										delta = now - tournament_dt
										hours, remainder = divmod(delta.seconds, 3600)
										minutes, seconds = divmod(remainder, 60)
										status = f"Started {hours:02d}:{minutes:02d} ago"
							except:
								status = ""
							# Tournament card layout
							pre_register_html = ""
							if day == today_name and GOOGLE_FORM_URL:
								pre_register_html = f'<a href="{GOOGLE_FORM_URL}" target="_blank"><button style="background: linear-gradient(90deg,#003366,#004080); color: #ffffff; border: 2px solid #FFD700; padding: 10px 20px; border-radius: 20px; font-weight:700; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s ease; position: relative; overflow: hidden; margin-top: 10px;">Pre-register</button></a>'
							
							st.markdown(f"""
<div class="tournament-card">
<div style='font-size:18px; font-weight:700'>🎴 {row.get('time', '')} — {row.get('notes','')}</div>
<div class='status' style='color:#FFD700; font-weight:600; margin-bottom:6px;' {'data-target="' + target_ts + '"' if target_ts else ''}>Status: {status}</div>
<div style='margin-top:6px; line-height:1.6;'>
Buy-in: <strong>{row.get('buy_in','')}</strong><br>
Starting chips: <strong>{row.get('starting_chips','N/A')}</strong><br>
Re-buy: <strong>{row.get('rebuy','No')}</strong><br>
Cutoff: <strong>{row.get('cutoff','N/A')}</strong>
</div>
{pre_register_html}
</div>
""", unsafe_allow_html=True)
				else:
					# Other days: Use expander
					with st.expander(f"{day}, {date_str} - {tournament_names}"):
						# Display tournaments in a 1-column layout
						num_cols = 1
						cols = st.columns(num_cols)
						for i, (_, row) in enumerate(group.iterrows()):
							with cols[i % num_cols]:
								tournament_title = f"{row.get('notes','')}"
								# Calculate status
								status = ""
								target_ts = ""
								try:
									time_parsed = datetime.strptime(row.get('time', ''), "%I:%M %p").time()
									tournament_dt = datetime.combine(day_dates[day], time_parsed).replace(tzinfo=timezone.utc)
									now = datetime.now(timezone.utc)
									if tournament_dt < now:
										status = "Ended"
									elif tournament_dt.date() == now.date():
										if tournament_dt > now:
											delta = tournament_dt - now
											hours, remainder = divmod(delta.seconds, 3600)
											minutes, seconds = divmod(remainder, 60)
											status = f"Starts in {hours:02d}:{minutes:02d}:{seconds:02d}"
											target_ts = str(int(tournament_dt.timestamp()))
										else:
											delta = now - tournament_dt
											hours, remainder = divmod(delta.seconds, 3600)
											minutes, seconds = divmod(remainder, 60)
											status = f"Started {hours:02d}:{minutes:02d} ago"
								except:
									status = ""
								# Tournament card layout
								pre_register_html = ""
								if day == today_name and GOOGLE_FORM_URL:
									pre_register_html = f'<a href="{GOOGLE_FORM_URL}" target="_blank"><button style="background: linear-gradient(90deg,#003366,#004080); color: #ffffff; border: 2px solid #FFD700; padding: 10px 20px; border-radius: 20px; font-weight:700; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s ease; position: relative; overflow: hidden; margin-top: 10px;">Pre-register</button></a>'
								
								st.markdown(f"""
<div class="tournament-card">
<div style='font-size:18px; font-weight:700'>🎴 {row.get('time', '')} — {row.get('notes','')}</div>
<div class='status' style='color:#FFD700; font-weight:600; margin-bottom:6px;' {'data-target="' + target_ts + '"' if target_ts else ''}>Status: {status}</div>
<div style='margin-top:6px; line-height:1.6;'>
Buy-in: <strong>{row.get('buy_in','')}</strong><br>
Starting chips: <strong>{row.get('starting_chips','N/A')}</strong><br>
Re-buy: <strong>{row.get('rebuy','No')}</strong><br>
Cutoff: <strong>{row.get('cutoff','N/A')}</strong>
</div>
{pre_register_html}
</div>
""", unsafe_allow_html=True)
		st.markdown("""<script>setInterval(function() { var now = Math.floor(Date.now() / 1000); var statuses = document.querySelectorAll('.status'); statuses.forEach(function(el) { var target = el.getAttribute('data-target'); if (target) { var diff = target - now; if (diff > 0) { var hours = Math.floor(diff / 3600); var minutes = Math.floor((diff % 3600) / 60); var seconds = diff % 60; el.textContent = 'Status: Starts in ' + hours.toString().padStart(2,'0') + ':' + minutes.toString().padStart(2,'0') + ':' + seconds.toString().padStart(2,'0'); } else { el.textContent = 'Status: Started'; } } }); }, 1000);</script>""", unsafe_allow_html=True)

	with tabs[1]:
		# Poker Schedule: Full flat list of all tournaments
		st.header("Weekly Poker Schedule")
		for day in days_order:
			if day in grouped:
				group = grouped[day]
				date_str = day_dates[day].strftime("%B %d, %Y")
				for i, (_, row) in enumerate(group.iterrows()):
					with st.container():
						tournament_title = f"{row.get('notes','')}"
						# Calculate status
						status = ""
						target_ts = ""
						try:
							time_parsed = datetime.strptime(row.get('time', ''), "%I:%M %p").time()
							tournament_dt = datetime.combine(day_dates[day], time_parsed).replace(tzinfo=timezone.utc)
							now = datetime.now(timezone.utc)
							if tournament_dt < now:
								status = "Ended"
							elif tournament_dt.date() == now.date():
								if tournament_dt > now:
									delta = tournament_dt - now
									hours, remainder = divmod(delta.seconds, 3600)
									minutes, seconds = divmod(remainder, 60)
									status = f"Starts in {hours:02d}:{minutes:02d}:{seconds:02d}"
									target_ts = str(int(tournament_dt.timestamp()))
								else:
									delta = now - tournament_dt
									hours, remainder = divmod(delta.seconds, 3600)
									minutes, seconds = divmod(remainder, 60)
									status = f"Started {hours:02d}:{minutes:02d} ago"
						except:
							status = ""
						# Tournament card layout
						pre_register_html = ""
						if day == today_name and GOOGLE_FORM_URL:
							pre_register_html = f'<a href="{GOOGLE_FORM_URL}" target="_blank"><button style="background: linear-gradient(90deg,#003366,#004080); color: #ffffff; border: 2px solid #FFD700; padding: 10px 20px; border-radius: 20px; font-weight:700; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s ease; position: relative; overflow: hidden; margin-top: 10px;">Pre-register</button></a>'
						
						st.markdown(f"""
<div class="tournament-card">
<div style='font-size:18px; font-weight:700'>🎴 {day}, {date_str} - {row.get('time', '')} — {row.get('notes','')}</div>
<div class='status' style='color:#FFD700; font-weight:600; margin-bottom:6px;' {'data-target="' + target_ts + '"' if target_ts else ''}>Status: {status}</div>
<div style='margin-top:6px; line-height:1.6;'>
Buy-in: <strong>{row.get('buy_in','')}</strong><br>
Starting chips: <strong>{row.get('starting_chips','N/A')}</strong><br>
Re-buy: <strong>{row.get('rebuy','No')}</strong><br>
Cutoff: <strong>{row.get('cutoff','N/A')}</strong>
</div>
{pre_register_html}
</div>
""", unsafe_allow_html=True)
		st.markdown("""<script>setInterval(function() { var now = Math.floor(Date.now() / 1000); var statuses = document.querySelectorAll('.status'); statuses.forEach(function(el) { var target = el.getAttribute('data-target'); if (target) { var diff = target - now; if (diff > 0) { var hours = Math.floor(diff / 3600); var minutes = Math.floor((diff % 3600) / 60); var seconds = diff % 60; el.textContent = 'Status: Starts in ' + hours.toString().padStart(2,'0') + ':' + minutes.toString().padStart(2,'0') + ':' + seconds.toString().padStart(2,'0'); } else { el.textContent = 'Status: Started'; } } }); }, 1000);</script>""", unsafe_allow_html=True)
	with tabs[2]:
		st.header("About Big Slick Social Club")
		st.write("Big Slick Social Club is an exciting new live poker venue, featuring both tournaments and cash games. We offer a fun and welcoming environment for poker enthusiasts of all levels.")
		st.write("Our weekly tournament schedule includes a variety of events to keep things interesting. Join us for some great poker action!")

	with tabs[3]:
		st.header("Contact Us")
		st.markdown('<a href="https://maps.google.com/?q=5825 Jackman Rd, Toledo, OH 43613" target="_blank" style="color:#FFD700; text-decoration:none;">📍 5825 Jackman Rd, Toledo, OH 43613</a>', unsafe_allow_html=True)
		st.write("Follow us on:")
		cols = st.columns(3)
		cols[0].markdown('<a href="https://www.facebook.com/p/Big-Slick-Social-Club-61571086161193/" target="_blank"><button style="background:#4267B2; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📘 Facebook</button></a>', unsafe_allow_html=True)
		cols[1].markdown('<a href="https://www.instagram.com/bigslicksocialclub/" target="_blank"><button style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📷 Instagram</button></a>', unsafe_allow_html=True)
		cols[2].markdown('<a href="tel:(419) 360-3003" style="color:#FFD700; text-decoration:none;">📞 Call: (419) 360-3003</a>', unsafe_allow_html=True)

if __name__ == "__main__":
	main()
