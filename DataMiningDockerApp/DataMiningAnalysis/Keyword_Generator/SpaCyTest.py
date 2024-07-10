import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Lade das englische Modell von SpaCy
nlp = spacy.load("de_core_news_lg")

# Beispieltext (ersetze dies mit deinem Zeitungsartikel)
text = """
Suns Lauf von Vekic gestoppt
Heute, 16:57 Uhr

Klicken, um die Teilen-Funktion zu öffnen.
Scheiterte im Viertelfinal
Lulu Sun.

Lulu Sun (NZL/WTA 123) hat in Wimbledon den Einzug in die Halbfinals verpasst.
Die Neuseeländerin muss sich der Kroatin Donna Vekic mit 7:5, 4:6, 1:6 geschlagen geben.
Der Höhenflug von Lulu Sun in Wimbledon ist im Viertelfinal zu Ende gegangen. Die 23-jährige neuseeländische Qualifikantin, die im Waadtland aufgewachsen ist und bis im Vorjahr für die Schweiz spielte, unterlag der ungesetzten Kroatin Donna Vekic in etwas mehr als zwei Stunden 7:5, 4:6, 1:6. Nach drei Siegen in der Qualifikation und vier im Haupttableau ging Sun gegen Vekic nach gewonnenem Startsatz etwas die Kraft aus. Zwar schaffte sie im zweiten Satz beim Stand von 3:5 noch einmal das Rebreak, danach gewann sie aber nur noch ein Game (zum 1:5 im dritten Satz).

Hier endet Suns Wimbledon-Märchen – jenes von Vekic geht weiter
«Sie spielte unglaublich gut und pushte mich ans Limit», anerkannte die 28-jährige Vekic nach ihrem erstmaligen Einzug in einen Grand-Slam-Halbfinal. Dank des Exploits auf dem Londoner Rasen wird Sun im WTA-Ranking einen grossen Sprung nach vorne machen und sich in die Top 60 verbessern. Zudem bringt ihr der Viertelfinal-Vorstoss ein Preisgeld von 375'000 Pfund (430'000 Franken) ein. Die einstige Top-20-Spielerin Vekic kehrt unabhängig des weiteren Turnierverlaufs in die Top 30 zurück.
"""

# Verarbeite den Text mit SpaCy
doc = nlp(text)

# Extrahiere die Nomen aus dem Text
nouns = [token.text for token in doc if token.pos_ == "NOUN"]

# Wende TF-IDF auf die Nomen an
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([" ".join(nouns)])
df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names_out(), columns=["TF-IDF"])
df = df.sort_values(by=["TF-IDF"], ascending=False)

# Ausgabe der 3 wichtigsten Schlüsselwörter
keywords = df.head(10).index.tolist()
print("Top 10 Keywords:", keywords)

