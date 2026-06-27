@echo off
echo Starting F.O.C.U.S. Futures Trade Projections on port 8103...
start http://localhost:8103
python -m http.server 8103
pause
