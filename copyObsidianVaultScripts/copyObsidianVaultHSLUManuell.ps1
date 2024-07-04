# Pfade definieren
$sourcePath = "C:\Users\fabia\Documents\HSLU\VaultObsidianHSLU\*"
$destinationPath = "C:\Users\fabia\iCloudDrive\iCloud~md~obsidian\VaultObsidianHSLU"

# Ordner kopieren
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

# Logging
$logFile = "C:\Users\fabia\Documents\Coding_Projekte\loggingFileForObsidianVaultCopy.txt"
$meldung = "Das Script für den HSLU vault wurde getriggert und ist durchgelaufen."
