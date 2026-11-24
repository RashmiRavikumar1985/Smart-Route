@echo off
set "SUMO_HOME=C:\Program Files (x86)\SUMO"
set "PATH=C:\Program Files (x86)\SUMO\bin;%PATH%"
cd /d "E:\Traffic_Signal_Optimization_using_Reinforcement_Learning-main\Traffic_Signal_Optimization_using_Reinforcement_Learning-main"
python evaluate_gui.py
pause
