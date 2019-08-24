@echo off

set OMP_NUM_THREADS=2
set PYTHONHASHSEED=0
python time_series.py

pause
