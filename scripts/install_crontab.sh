#!/bin/bash
# MSTR Engine Crontab Installation
# Run as: sudo -u openclaw bash /home/openclaw/mstr-engine/scripts/install_crontab.sh

RUNNER="/usr/bin/python3 /home/openclaw/mstr-engine/scripts/cron_runner.py"
LOGDIR="/home/openclaw/mstr-engine/logs"

mkdir -p "$LOGDIR"

# Write crontab
crontab -l 2>/dev/null | grep -v "mstr-engine" > /tmp/crontab_clean 2>/dev/null || true

cat >> /tmp/crontab_clean << 'EOF'
# === MSTR Engine Data Pipeline ===
# All times in ET (America/New_York)
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
CRON_TZ=America/New_York

# --- Market Hours (9:30 AM - 4:00 PM ET, Mon-Fri) ---
# ORATS: every 5 min during market hours
*/5 9-15 * * 1-5 $RUNNER collect_orats.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1
30-59/5 9 * * 1-5 $RUNNER collect_orats.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# Unusual Whales flow: every 15 min during market hours
*/15 9-15 * * 1-5 $RUNNER collect_flow.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1
30,45 9 * * 1-5 $RUNNER collect_flow.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# --- Daily Schedules ---
# FRED macro data: 6:00 AM ET
0 6 * * 1-5 $RUNNER collect_fred.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# EDGAR filings: every 30 min during business hours (8 AM - 6 PM ET)
*/30 8-17 * * 1-5 $RUNNER collect_edgar.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# GLI proxy calculation: 6:15 AM ET (after FRED pull)
15 6 * * 1-5 $RUNNER calc_gli_proxy.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# SRI stage calculation: 4:30 PM ET (after market close + OHLCV final)
30 16 * * 1-5 $RUNNER calc_sri.py >> /home/openclaw/mstr-engine/logs/cron.log 2>&1

# --- Signal Engine & Reports ---
# Morning Brief: 7:00 AM ET — pre-market summary before open
0 7 * * 1-5 /usr/bin/python3 /home/openclaw/mstr-engine/scripts/morning_brief.py >> /home/openclaw/mstr-engine/logs/morning_brief.log 2>&1

# Daily Engine Run (primary): 10:30 AM ET — after Gavin's morning CSV push
30 10 * * 1-5 /usr/bin/python3 /home/openclaw/mstr-engine/scripts/daily_engine_run.py >> /home/openclaw/mstr-engine/logs/daily_engine.log 2>&1

# EOD Recap: 4:15 PM ET — just after market close
15 16 * * 1-5 /usr/bin/python3 /home/openclaw/mstr-engine/scripts/eod_recap.py >> /home/openclaw/mstr-engine/logs/eod_recap.log 2>&1

# Daily Engine Run (second pass): 5:00 PM ET — after all EOD data settles; catches late CSV updates
0 17 * * 1-5 /usr/bin/python3 /home/openclaw/mstr-engine/scripts/daily_engine_run.py >> /home/openclaw/mstr-engine/logs/daily_engine.log 2>&1

# --- End MSTR Engine ---
EOF

# Replace $RUNNER with actual path
sed -i "s|\$RUNNER|$RUNNER|g" /tmp/crontab_clean

crontab /tmp/crontab_clean
rm /tmp/crontab_clean

echo "Crontab installed. Current entries:"
crontab -l | grep -A1 "mstr-engine\|MSTR\|collect_\|calc_"
