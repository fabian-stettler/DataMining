# Pfade definieren
$sourcePath = "C:\Users\fabia\Documents\secondBrain1\*"
$destinationPath = "C:\Users\fabia\iCloudDrive\iCloud~md~obsidian\secondBrain"

# Ordner kopieren
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force


$logFile = "C:\Users\fabia\Documents\Coding_Projekte\loggingFileForObsidianVaultCopy.txt"
$meldung = "Das Skript für das Kopieren des second Brains ist durchgelaufen."
Add-Content -Path $logFile -Value $meldung
