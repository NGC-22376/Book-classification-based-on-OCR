@echo off
setlocal enabledelayedexpansion
REM python
call C:\Users\30744\anaconda3\Scripts\activate.bat bookclassify
:roundstart
cd C:\Users\30744\Desktop\CodeFiles\Python\Book-classification-based-on-OCR
set PY1=src/main.py
set PY2=src/gene_window.py
python src/main.py
python src/write_into_mcu.py
cd C:\Keil9.6.1\UV4
UV4 C:\Keil9.6.1\UV4 -b  C:\Users\30744\Desktop\CodeFiles\MCU_C51\code.uvproj -o C:\Users\30744\Desktop\CodeFiles\MCU_C51\Objects

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
cd C:\Users\30744\Desktop\CodeFiles\Python\Book-classification-based-on-OCR\src
python gene_window.py
