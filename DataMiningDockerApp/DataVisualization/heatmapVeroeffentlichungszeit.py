from pymongo import MongoClient
import pandas as pd
import plotly.express as px

def generateHeatmap():
    '''
    generates a heatmap 7x24 grid, which shows release dates of the articles in a heatmap and includes all articles
    :return:
    '''
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Datamining_Srf']
    collection = db['Articles']

    # Alle Dokumente aus der Sammlung abrufen
    data = list(collection.find({}, {'_id': 0, 'publication_date': 1}))

    # In ein DataFrame umwandeln
    df = pd.DataFrame(data)

    # Konvertierung in datetime
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

    # Überprüfung auf fehlerhafte Konvertierungen
    if df['publication_date'].isnull().any():
        print("Some dates could not be converted. Check the data for irregularities.")
        print(df[df['publication_date'].isnull()])

    # Entfernen von Zeilen mit NaT-Werten
    df = df.dropna(subset=['publication_date'])

    # Berechnung von Wochentagen und Stunden
    # dt is a so called datetime accessor and works only on datetime objects
    df['weekday'] = df['publication_date'].dt.weekday  # Montag=0, Sonntag=6
    df['hour'] = df['publication_date'].dt.hour

    # Leere 7x24-Matrix erstellen
    heatmap_data = pd.DataFrame(0, index=range(7), columns=range(24))

    # Über die DataFrame-Zeilen iterieren und Zählung in der Heatmap erhöhen
    for index, row in df.iterrows():
        weekday = row['weekday']
        hour = row['hour']
        heatmap_data.at[weekday, hour] += 1

    # Optional: Umbenennen der Indexe für eine bessere Lesbarkeit
    heatmap_data.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig = px.imshow(heatmap_data, labels=dict(x="Hour", y="Day", color="Articles"))
    fig.show()
generateHeatmap()