@echo on
echo "welcome To OSMOS software"

if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

REM path setup to environment
set envProject=OSMOS_CB
set root=%USERPROFILE%\Anaconda3
set env1=%USERPROFILE%\Anaconda3\envs\%envProject%

REM environment activation
call %root%\Scripts\activate.bat %env1%

python "App.py"

exit 0

