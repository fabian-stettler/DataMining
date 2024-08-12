from transformers import AutoModel
from keybert import KeyBERT
from collections import defaultdict

def weighted_keywords(keywords, weight):
    return [(kw, score * weight) for kw, score in keywords]

def getBERTKeywords(lead, title, subtitles, paragraphs, model=AutoModel.from_pretrained("dbmdz/bert-base-german-cased")):
    # Initialisieren von KeyBERT mit dem geladenen Modell
    kw_model = KeyBERT(model)

    # Debug statement to check 'lead'
    print("Lead before extract_keywords:", lead)
    print("Subtitles before extract_keywords:", subtitles)
    print("Title before extract_keywords:", title)
    print("Paragraphs before extract_keywords:", paragraphs)

    # Gewichtung der Textteile
    lead_weight = 2
    title_weight = 1.5
    subtitle_weight = 0.7
    paragraph_weight = 0.5

    # Anzahl an Keywords für return
    anzahl_an_return_keywords = 10

    all_keywords = []

    # Keywords extrahieren und gewichten
    if lead:
        lead_keywords = kw_model.extract_keywords(lead, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
        weighted_lead_keywords = weighted_keywords(lead_keywords, lead_weight)
        all_keywords.extend(weighted_lead_keywords)

    if title:
        title_keywords = kw_model.extract_keywords(title, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
        weighted_title_keywords = weighted_keywords(title_keywords, title_weight)
        all_keywords.extend(weighted_title_keywords)

    if subtitles:
        for sub in subtitles:
            if sub:
                sub_keywords = kw_model.extract_keywords(sub, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
                weighted_subtitle_keywords = weighted_keywords(sub_keywords, subtitle_weight)
                all_keywords.extend(weighted_subtitle_keywords)

    if paragraphs:
        for p in paragraphs:
            if p:
                p_keywords = kw_model.extract_keywords(p, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=5)
                weighted_paragraph_keywords = weighted_keywords(p_keywords, paragraph_weight)
                all_keywords.extend(weighted_paragraph_keywords)

    # Deduplizieren und nach Gewicht sortieren
    keyword_dict = defaultdict(float)
    for kw, score in all_keywords:
        keyword_dict[kw] += score

    # Sortieren der Keywords nach Gewicht
    sorted_keywords = sorted(keyword_dict.items(), key=lambda item: item[1], reverse=True)

    # Nur die Keywords extrahieren
    relevant_keywords = [kw for kw, score in sorted_keywords[:anzahl_an_return_keywords]]

    return relevant_keywords
