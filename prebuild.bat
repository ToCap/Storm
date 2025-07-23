@echo OFF
setlocal enabledelayedexpansion enableextensions


set PROJECT_PATH=%~dp0

REM Create _build directory
set OUTPUT_PATH=%PROJECT_PATH%\\_build
mkdir "%OUTPUT_PATH%"

set OUTPUT_PATH=%PROJECT_PATH%\\_build\\proto
rmdir "%OUTPUT_PATH%" /s/q
mkdir "%OUTPUT_PATH%"



protoc --proto_path=%PROJECT_PATH% --python_out=%OUTPUT_PATH% %PROJECT_PATH%/infrared_sensor.proto
protoc --proto_path=%PROJECT_PATH% --python_out=%OUTPUT_PATH% %PROJECT_PATH%/touch_sensor.proto