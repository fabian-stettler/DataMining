# Pfade definieren
$sourcePath = "C:\Users\fabia\Documents\secondBrain1\*"
$destinationPath = "C:\Users\fabia\iCloudDrive\iCloud~md~obsidian\secondBrain"

# Ordner kopieren
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

# Zeitintervall für die Ausführung des Skripts definieren (hier: alle 24 Stunden)
$trigger = New-JobTrigger -Once -At (Get-Date).AddDays(1).Date -RepetitionInterval (New-TimeSpan -Hours 24)

# Aktion, die beim Auslösen des Triggers ausgeführt wird
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File 'C:\Users\fabia\Documents\Coding_Projekte\copyObsidianVaultScripts\copyObsidianVaultsecondBrain.ps1'"

# Trigger und Aktion zum Erstellen des geplanten Tasks verwenden
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Obsidian Kopier Script" -Description "Kopiert den Obsidian Vault second Brain in das ICloud Drive."

$logFile = "C:\Users\fabia\Documents\Coding_Projekte\loggingFileForObsidianVaultCopy.txt"
$meldung = "Das Skript für das Kopieren des second Brains ist durchgelaufen."
Add-Content -Path $logFile -Value $meldung