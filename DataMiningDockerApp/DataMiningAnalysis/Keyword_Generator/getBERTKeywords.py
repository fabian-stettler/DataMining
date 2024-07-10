from transformers import AutoTokenizer, AutoModel
from keybert import KeyBERT

# Laden des deutschen BERT-Modells und des Tokenizers
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-german-cased")
model = AutoModel.from_pretrained("dbmdz/bert-base-german-cased")

# Initialisieren von KeyBERT mit dem geladenen Modell
kw_model = KeyBERT(model)

# Beispieltexte
lead = "Wimbledon: Viertelfinal Frauen"
title = "Suns Lauf von Vekic gestoppt – Paolini ohne Probleme"
subtitles = [
    "Paolini sorgt für italienische Premiere",
]  # Füge hier alle Untertitel hinzu
paragraphs = [
    "Lulu Sun (NZL/WTA 123) hat in Wimbledon den Einzug in die Halbfinals verpasst. Die Neuseeländerin muss sich Donna Vekic (CRO/WTA 37) mit 7:5, 4:6, 1:6 geschlagen geben.Vekic trifft im Halbfinal auf Jasmine Paolini (ITA/WTA 7), die Emma Navarro (USA/WTA 17) mit 6:2, 6:1 besiegt.Der Höhenflug von Lulu Sun in Wimbledon ist im Viertelfinal zu Ende gegangen. Die 23-jährige neuseeländische Qualifikantin, die im Waadtland aufgewachsen ist und bis im Vorjahr für die Schweiz spielte, unterlag der ungesetzten Kroatin Donna Vekic in etwas mehr als zwei Stunden 7:5, 4:6, 1:6. Nach drei Siegen in der Qualifikation und vier im Haupttableau ging Sun gegen Vekic nach gewonnenem Startsatz etwas die Kraft aus. Zwar schaffte sie im zweiten Satz beim Stand von 3:5 noch einmal das Rebreak, danach gewann sie aber nur noch ein Game (zum 1:5 im dritten Satz).",
    "Sie spielte unglaublich gut und pushte mich ans Limit», anerkannte die 28-jährige Vekic nach ihrem erstmaligen Einzug in einen Grand-Slam-Halbfinal. Dank des Exploits auf dem Londoner Rasen wird Sun im WTA-Ranking einen grossen Sprung nach vorne machen und sich in die Top 60 verbessern. Zudem bringt ihr der Viertelfinal-Vorstoss ein Preisgeld von 375'000 Pfund (430'000 Franken) ein. Die einstige Top-20-Spielerin Vekic kehrt unabhängig des weiteren Turnierverlaufs in die Top 30 zurück.Paolini sorgt für italienische Premiere Vekics Gegnerin im Halbfinal ist Jasmine Paolini. Die Italienerin, die zuletzt an den French Open bis in den Final vorgestossen war, bewies ihre starke Form auch im Viertelfinal gegen Emma Navarro. Dank ihrem souveränen 6:2, 6:1-Erfolg gegen die US-Amerikanerin zog Paolini in Wimbledon als erste Spielerin ihres Landes in die Runde der letzten Vier ein.Die 1,63 m grosse Toskanerin, die vor 2024 nie über die 2. Runde eines Grand-Slam-Turniers hinausgekommen war, liess Navarro nicht den Hauch einer Chance. In 58 Minuten entschied sie die Partie mit einem Punkteverhältnis von 54:31 überlegen für sich."
]

# Gewichtung der Textteile
lead_weight = 1.3
title_weight = 1.5
subtitle_weight = 1.2
paragraph_weight = 1.0

# Keywords extrahieren und gewichten
lead_keywords = kw_model.extract_keywords(lead, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
title_keywords = kw_model.extract_keywords(title, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
subtitle_keywords = [kw_model.extract_keywords(sub, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5) for sub in subtitles]
paragraph_keywords = [kw_model.extract_keywords(p, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5) for p in paragraphs]

# Gewichtete Keywords zusammenführen
def weighted_keywords(keywords, weight):
    return [(kw, score * weight) for kw, score in keywords]

weighted_lead_keywords = weighted_keywords(lead_keywords, lead_weight)
weighted_title_keywords = weighted_keywords(title_keywords, title_weight)
weighted_subtitle_keywords = [weighted_keywords(sub_keywords, subtitle_weight) for sub_keywords in subtitle_keywords]
weighted_paragraph_keywords = [weighted_keywords(p_keywords, paragraph_weight) for p_keywords in paragraph_keywords]

# Alle gewichteten Keywords zusammenführen
all_keywords = weighted_lead_keywords + weighted_title_keywords + [kw for sublist in weighted_subtitle_keywords for kw in sublist] + [kw for sublist in weighted_paragraph_keywords for kw in sublist]

# Deduplizieren und nach Gewicht sortieren
from collections import defaultdict
keyword_dict = defaultdict(float)
for kw, score in all_keywords:
    keyword_dict[kw] += score

# Sortieren der Keywords nach Gewicht
sorted_keywords = sorted(keyword_dict.items(), key=lambda item: item[1], reverse=True)

# Relevante Keywords ausgeben
print("Relevante gewichtete Keywords:", sorted_keywords[:10])
