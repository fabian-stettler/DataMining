from transformers import AutoTokenizer, AutoModel
from keybert import KeyBERT

def weighted_keywords(keywords, weight):
    return [(kw, score * weight) for kw, score in keywords]

def getBERTKeywords(lead, title, subtitles, paragraphs, model = AutoModel.from_pretrained("dbmdz/bert-base-german-cased")):



    # Initialisieren von KeyBERT mit dem geladenen Modell
    kw_model = KeyBERT(model)

    # Beispieltexte
    lead = lead
    title = title
    subtitles = subtitles
    paragraphs = paragraphs

    # Gewichtung der Textteile
    lead_weight = 2
    title_weight = 1.5
    subtitle_weight = 0.7
    paragraph_weight = 0.5

    #Anzahl an Keywords für return
    anzahl_an_return_keywords = 4

    # Keywords extrahieren und gewichten
    lead_keywords = kw_model.extract_keywords(lead, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
    title_keywords = kw_model.extract_keywords(title, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
    subtitle_keywords = [kw_model.extract_keywords(sub, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5) for sub in subtitles]
    paragraph_keywords = [kw_model.extract_keywords(p, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5) for p in paragraphs]

    # Gewichtete Keywords zusammenführen
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

    # Nur die Keywords extrahieren
    relevant_keywords = [kw for kw, score in sorted_keywords[:anzahl_an_return_keywords]]

    return relevant_keywords


