@echo off
setlocal enabledelayedexpansion
REM python
call C:\Users\30744\anaconda3\Scripts\activate.bat cv
:roundstart
cd C:\Users\30744\Desktop\ComputerVision
set PY1=main.py
set PY2=gene_window.py
python main.py
python write_into_mcu.py
cd C:\Keil9.6.1\UV4
UV4 C:\Keil9.6.1\UV4 -b  C:\CodeFiles\MCU_C51\code.uvproj -o C:\CodeFiles\MCU_C51\Objects1

echo Press 'Q' to quit the round.
echo Any other key to continue...
choice /C YQ /N /M "Do you want to continue? [Y/Q]"

if errorlevel 2 (
    echo You chose Quit.
    goto roundend
) 
else (
    echo You chose Yes.
    goto roundstart
)
:roundend
echo ALL DONE
cd C:\Users\30744\Desktop\ComputerVision
python gene_window.py
