# Launch the first command in a new PowerShell window
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "python src/server/main.py"

# Launch the second command in another new PowerShell window
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "open-webui serve"

# Pause the current script to keep the window open
Pause
