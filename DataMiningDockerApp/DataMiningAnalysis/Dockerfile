FROM python:3.9-slim

# Installiere pymongo
RUN pip install pymongo beautifulsoup4 
RUN pip install transformers pandas keybert

# Setze das Arbeitsverzeichnis
WORKDIR /usr/src/scripts

# Kopiere deine Anwendung in das Image
COPY . .

# Debugging: Zeige den Inhalt des Verzeichnisses nach dem Kopieren
RUN ls -la /usr/src/scripts

# Starte das Python-Skript
ENTRYPOINT ["python", "controlAnalysis.py"]



