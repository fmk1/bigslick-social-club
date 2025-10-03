with open('/home/ifeanyi/bigslick/app.py', 'r') as f:
    content = f.read()

old_main = """def main():
	# Layout: main content
	with st.container():
		df = load_schedule('https://docs.google.com/spreadsheets/d/e/2PACX-1vSeHdpSUFfU2_Lh0dGgWUc9O8lAD_wn0K_jLCoHoQh4JXWsKDGh4A6tI47YnpHMD-vDdNEWYNgmFLxy/pub?output=csv&gid=1579199027')
		# if we loaded from CSV, try normalizing columns to the app's expected schema
		try:
			df = normalize_schedule_df(df)
		except Exception:
			# if normalize fails, keep original df
			pass

		if df.empty:
			st.info("No schedule found. Add a `schedule.csv` in the project root or provide a SCHEDULE_CSV_URL in settings.")
			st.stop()
		# normalize day ordering
		days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		df["day"] = df["day"].astype(str)
		df["day_order"] = df["day"].apply(lambda d: days_order.index(d) if d in days_order else 7)
		df = df.sort_values(["day_order", "time"]).drop(columns=["day_order"])

		st.header("Weekly Poker Schedule")

		# ensure every day appears once (even if empty)
		grouped = {day: group for day, group in df.groupby("day")}
		today_name = datetime.now(timezone.utc).strftime("%A")
		for day in days_order:
			if day in grouped:
				group = grouped[day]
				# Day header
				st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:700; color:#FFD700; margin:20px 0 10px 0; padding-bottom:8px;'>{day}</div>", unsafe_allow_html=True)
				for _, row in group.iterrows():
					tournament_title = f"{row.get('notes','')}"
					with st.expander(tournament_title, expanded=(day == today_name)):
						# Tournament card layout with badges and a fun register button
						st.markdown(f"<div style='font-size:18px; font-weight:700'>🎴 {row.get('time', '')} — {row.get('notes','')}</div>", unsafe_allow_html=True)
						st.markdown(f"<div style='margin-top:6px; color:#000000 !important; line-height:1.6;'>Buy-in: <strong>{row.get('buy_in','')}</strong><br>Starting chips: <strong>{row.get('starting_chips','N/A')}</strong><br>Re-buy: <strong>{row.get('rebuy','No')}</strong><br>Cutoff: <strong>{row.get('cutoff','N/A')}</strong></div>", unsafe_allow_html=True)

						# Show Pre-register link only on the actual tournament day
						if day == today_name and GOOGLE_FORM_URL:
							st.markdown(f'<a href="{GOOGLE_FORM_URL}" target="_blank"><button style="background: linear-gradient(90deg,#003366,#004080); color: #ffffff; border: 2px solid #FFD700; padding: 10px 20px; border-radius: 20px; font-weight:700; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s ease; position: relative; overflow: hidden;">Pre-register</button></a>', unsafe_allow_html=True)
				# st.markdown('<div class="tournament-separator"></div>', unsafe_allow_html=True)

		st.markdown("---")
		st.write("Follow us on:")
		cols = st.columns(4)
		cols[0].markdown('<a href="https://www.facebook.com/p/Big-Slick-Social-Club-61571086161193/" target="_blank"><button style="background:#4267B2; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📘 Facebook</button></a>', unsafe_allow_html=True)
		cols[1].markdown('<a href="https://www.instagram.com/bigslicksocialclub/" target="_blank"><button style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📷 Instagram</button></a>', unsafe_allow_html=True)
		cols[2].markdown('<a href="tel:(419) 360-3003" style="color:#FFD700; text-decoration:none;">📞 Call: (419) 360-3003</a>', unsafe_allow_html=True)
		cols[3].markdown('<a href="https://maps.google.com/?q=5825 Jackman Rd, Toledo, OH 43613" target="_blank" style="color:#FFD700; text-decoration:none;">📍 5825 Jackman Rd, Toledo, OH 43613</a>', unsafe_allow_html=True)"""

new_main = """def main():
	page = st.sidebar.radio("Navigation", ["Home", "About", "Contact"])

	if page == "Home":
		# Layout: main content
		with st.container():
			df = load_schedule('https://docs.google.com/spreadsheets/d/e/2PACX-1vSeHdpSUFfU2_Lh0dGgWUc9O8lAD_wn0K_jLCoHoQh4JXWsKDGh4A6tI47YnpHMD-vDdNEWYNgmFLxy/pub?output=csv&gid=1579199027')
			# if we loaded from CSV, try normalizing columns to the app's expected schema
			try:
				df = normalize_schedule_df(df)
			except Exception:
				# if normalize fails, keep original df
				pass

			if df.empty:
				st.info("No schedule found. Add a `schedule.csv` in the project root or provide a SCHEDULE_CSV_URL in settings.")
				st.stop()
			# normalize day ordering
			days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			df["day"] = df["day"].astype(str)
			df["day_order"] = df["day"].apply(lambda d: days_order.index(d) if d in days_order else 7)
			df = df.sort_values(["day_order", "time"]).drop(columns=["day_order"])

			st.header("Weekly Poker Schedule")

			# ensure every day appears once (even if empty)
			grouped = {day: group for day, group in df.groupby("day")}
			today_name = datetime.now(timezone.utc).strftime("%A")
			for day in days_order:
				if day in grouped:
					group = grouped[day]
					# Day header
					st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:700; color:#FFD700; margin:20px 0 10px 0; padding-bottom:8px;'>{day}</div>", unsafe_allow_html=True)
					for _, row in group.iterrows():
						tournament_title = f"{row.get('notes','')}"
						with st.expander(tournament_title, expanded=(day == today_name)):
							# Tournament card layout with badges and a fun register button
							st.markdown(f"<div style='font-size:18px; font-weight:700'>🎴 {row.get('time', '')} — {row.get('notes','')}</div>", unsafe_allow_html=True)
							st.markdown(f"<div style='margin-top:6px; color:#000000 !important; line-height:1.6;'>Buy-in: <strong>{row.get('buy_in','')}</strong><br>Starting chips: <strong>{row.get('starting_chips','N/A')}</strong><br>Re-buy: <strong>{row.get('rebuy','No')}</strong><br>Cutoff: <strong>{row.get('cutoff','N/A')}</strong></div>", unsafe_allow_html=True)

							# Show Pre-register link only on the actual tournament day
							if day == today_name and GOOGLE_FORM_URL:
								st.markdown(f'<a href="{GOOGLE_FORM_URL}" target="_blank"><button style="background: linear-gradient(90deg,#003366,#004080); color: #ffffff; border: 2px solid #FFD700; padding: 10px 20px; border-radius: 20px; font-weight:700; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.2s ease; position: relative; overflow: hidden;">Pre-register</button></a>', unsafe_allow_html=True)
					# st.markdown('<div class="tournament-separator"></div>', unsafe_allow_html=True)

	elif page == "About":
		st.header("About Big Slick Social Club")
		st.write("Big Slick Social Club is an exciting new live poker venue, featuring both tournaments and cash games. We offer a fun and welcoming environment for poker enthusiasts of all levels.")
		st.write("Our weekly tournament schedule includes a variety of events to keep things interesting. Join us for some great poker action!")

	elif page == "Contact":
		st.header("Contact Us")
		st.markdown('<a href="https://maps.google.com/?q=5825 Jackman Rd, Toledo, OH 43613" target="_blank" style="color:#FFD700; text-decoration:none;">📍 5825 Jackman Rd, Toledo, OH 43613</a>', unsafe_allow_html=True)
		st.write("Follow us on:")
		cols = st.columns(3)
		cols[0].markdown('<a href="https://www.facebook.com/p/Big-Slick-Social-Club-61571086161193/" target="_blank"><button style="background:#4267B2; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📘 Facebook</button></a>', unsafe_allow_html=True)
		cols[1].markdown('<a href="https://www.instagram.com/bigslicksocialclub/" target="_blank"><button style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold;">📷 Instagram</button></a>', unsafe_allow_html=True)
		cols[2].markdown('<a href="tel:(419) 360-3003" style="color:#FFD700; text-decoration:none;">📞 Call: (419) 360-3003</a>', unsafe_allow_html=True)"""

content = content.replace(old_main, new_main)

with open('/home/ifeanyi/bigslick/app.py', 'w') as f:
    f.write(content)