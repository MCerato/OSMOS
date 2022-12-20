@echo on
echo "welcome To OSMOS software"

if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit


set envProject=OSMOS_CB

set root=%USERPROFILE%\Anaconda3
set env1=%USERPROFILE%\Anaconda3\envs\%envProject%

call %root%\Scripts\activate.bat %env1%
python "App.py"

exit 0

