@echo off
cd /d "%~dp0"
python fetch_congress.py
python score_engine.py
python alerts.py
