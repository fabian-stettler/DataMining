# log_resources.ps1

# Specify the path for the log file
$logFilePath = "C:\Users\fabia\Desktop\htmlFiles\logFileRessources.txt"

while ($true) {
    # Get the current date and time
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # Get the Node.js process (control.js)
    $controlProcess = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.MainModule.FileName -like "*control.js*" }

    # Check if the control.js process is running
    if ($controlProcess) {
        # Log the timestamp and memory usage to the specified file
        Add-Content -Path $logFilePath -Value ("Timestamp: $timestamp")
        Add-Content -Path $logFilePath -Value ("Memory Usage (Working Set): $($controlProcess.WorkingSet64 / 1MB) MB")
        Add-Content -Path $logFilePath -Value ("Memory Usage (Private Memory): $($controlProcess.PrivateMemorySize64 / 1MB) MB")
        Add-Content -Path $logFilePath -Value ("Memory Usage (Virtual Memory): $($controlProcess.VirtualMemorySize64 / 1MB) MB")
        Add-Content -Path $logFilePath -Value ("-----------------------")
    } else {
        # Control.js process not found, exit the loop
        break
    }

    # Sleep for a specified interval (e.g., 60 seconds)
    Start-Sleep -Seconds 20
}

