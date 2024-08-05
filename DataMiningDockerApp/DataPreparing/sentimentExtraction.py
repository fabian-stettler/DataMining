
from datetime import datetime
from transformers import pipeline

from connectToMongoDBCollection import connectToMongoDBCollection
from constants import DATE_FORMAT, BEGINNING_DATE

# Laden eines vortrainierten Modells für Sentimentanalyse
sentiment_pipeline = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

def aspect_based_sentiment(text, aspect):
    '''
    :param text: text to analyze sentiment from
    :param aspect: keyword to analyze in text
    :return: label and score of confidence. label is either positive, negative or neutral
    and score which is between 0 and 1. (confident scores are higher than 0.9
    '''
    # Durchsucht den Text nach dem Aspekt und bewertet den Kontext
    results = sentiment_pipeline(text)
    for result in results:
        if aspect.lower() in text.lower():
            return {"label": result['label'], "score": result['score']}
    print("leaving sentiment function")
    return {"label": "neutral", "score": 0.5}

def find_next_sentence_end(text, middle):
    """
    Finds the next sentence end after the middle of the text and splits the text into two pieces.
    Returns the two pieces of the text.
    """
    middle = int(middle)
    # Find the next period after the middle point
    next_period = text.find('.', middle)
    if next_period == -1:
        # If no period is found, return the entire text as the first part and an empty string as the second
        return text, ''

    # Split the text at the period and add 1 to include the period in the first part
    text1 = text[:next_period + 1].strip()
    text2 = text[next_period + 1:].strip()

    return text1, text2


def controlSentimentExtraction(aspect, date_str):
    '''
    analyzes all articles which contain the aspect in its paragraphs and then generates sentiment objects and
    puts them into the Sentiment Collection.
    :param aspect: aspect to analyze and generate sentiments. Can be a name or subject.
    :param date: date indicates the point from which on articles are considered for new sentiment objects.
    this exists to not make work over again, when updating MongoDB with new data.
    :return:
    '''
    documents = []
    date = datetime.strptime(date_str, DATE_FORMAT)
    with connectToMongoDBCollection("Datamining_Srf", "Articles") as collectionArticles:
        answer = collectionArticles.find({
            'paragraphs': {
                '$elemMatch': {
                    '$regex': aspect,
                    '$options': 'i'
                }
            },
            'publication_date': {'$gt': date}
        })
        count = collectionArticles.count_documents({
            'paragraphs': {
                '$elemMatch': {
                    '$regex': aspect,
                    '$options': 'i'
                }
            },
            'publication_date': {'$gt': date}
        })
        print(str(count) + " new articles were found for aspect" + aspect)

        for entry in answer:
            samples = []
            paragraphs = entry['paragraphs']
            paragraph_number = 0
            split_count = 0
            max_splits = 20

            for text in paragraphs:
                paragraph_number += 1


                while len(text) > 511:
                    split_count += 1
                    if split_count > max_splits:
                        print(f"\033[91mSkipping article with content_id {entry['content_id']} due to excessive splits\033[0m")
                        break

                    middle = len(text) // 2
                    text1, text2 = find_next_sentence_end(text, middle)
                    paragraphs.append(text2)
                    text = text1

                if split_count > max_splits:
                    break  # Skip the rest of the paragraphs if max splits reached

                print(f"Sentiments werden jetzt ermittelt für Artikel mit ContentID {entry.get('content_id')} und Titel {entry.get('titles')}")
                sentiment = aspect_based_sentiment(text, aspect)
                print(f"Sentiment für '{aspect}': {sentiment['label']} mit einem Score von {sentiment['score']}")

                if sentiment['score']:
                    samples.append([sentiment['label'], sentiment['score'], paragraph_number, entry['titles']])
                    print("sentiment added")
                else:
                    print("sentiment not added")

            # If splits exceeded, skip to the next article
            if split_count > max_splits:
                continue

            document = {
                'aspect': aspect,
                'samples': []
            }

            for sent in samples:
                try:
                    print(sent[0])
                    print(sent[1])
                    print(sent[2])
                except IndexError:
                    print("IndexError: Sent structure is unexpected")

                currentSentimentScore = float(sent[1])
                #if currentSentimentScore > 0.9:
                document['samples'].append({
                    'sentiment': sent[0],
                    'score': sent[1],
                    'content_id': entry.get('content_id'),
                    'publication_date': entry.get('publication_date'),
                    'paragraph_number': sent[2] if len(sent) > 2 else 'N/A',
                    'title': sent[3]
                })

            if document['samples']:
                documents.append(document)

    if documents:
        with connectToMongoDBCollection('Datamining_Srf', 'Sentiment') as collectionSentiment:
            result = collectionSentiment.insert_many(documents)
            print(f'Documents inserted with IDs: {result.inserted_ids}')
            print(f'{len(documents)} were newly inserted into MongoDB for aspect {aspect}')


controlSentimentExtraction('Berset', BEGINNING_DATE)

