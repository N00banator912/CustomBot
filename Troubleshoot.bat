@echo off
setlocal enabledelayedexpansion

:: Read the Kat.data file and store its contents in an array
set "file=Kat.data"
set "i=0"

for /f "tokens=*" %%a in ('type "%file%"') do (
    set /a i+=1
    set "line[!i!]=%%a"
)

:: Check IP addresses and hostnames
echo Checking IP addresses and hostnames...

for /l %%i in (5,1,%i%) do (
    set "entry=!line[%%i]!"
    echo Entry !entry!

    :: Split the entry by commas
    for /f "delims=," %%e in ("!entry!") do (
        set "ip_or_hostname=%%e"
        
        :: Check if it's an IP address
        ping -n 1 !ip_or_hostname! >nul 2>nul
        if !errorlevel! equ 0 (
            echo !ip_or_hostname! is a valid IP address.
        ) else (
            :: Try resolving as a hostname
            nslookup !ip_or_hostname! >nul 2>nul
            if !errorlevel! equ 0 (
                echo !ip_or_hostname! is a valid hostname.
            ) else (
                echo !ip_or_hostname! is neither a valid IP address nor a valid hostname.
            )
        )
    )
)

:: Pause to view results
pause