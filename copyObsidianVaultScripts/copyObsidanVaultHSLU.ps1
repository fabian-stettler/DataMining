# Pfade definieren
$sourcePath = "C:\Users\fabia\Documents\HSLU\VaultObsidianHSLU\*"
$destinationPath = "C:\Users\fabia\iCloudDrive\iCloud~md~obsidian\VaultObsidianHSLU"

# Ordner kopieren
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

# Zeitintervall für die Ausführung des Skripts definieren (hier: alle 24 Stunden)
$trigger = New-JobTrigger -Once -At (Get-Date).AddDays(1).Date -RepetitionInterval (New-TimeSpan -Hours 24)

# Aktion, die beim Auslösen des Triggers ausgeführt wird
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File 'C:\Users\fabia\Documents\Coding_Projekte\copyObsidianVaultScripts\copyObsidanVaultHSLU.ps1'"

# Trigger und Aktion zum Erstellen des geplanten Tasks verwenden
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Obsidian Kopier Script" -Description "Kopiert den Obsidian Vault in das ICloud Drive."

# Logging
$logFile = "C:\Users\fabia\Documents\Coding_Projekte\loggingFileForObsidianVaultCopy.txt"
$meldung = "Das Script für den HSLU vault wurde getriggert und ist durchgelaufen."
Add-Content -Path $logFile -Value $meldung
