from connectToMongoDBCollection import connectToMongoDBCollection


def sentimentAnalysis(aspect, filter):
    '''
    Analyzes sentiment objects, concerning one aspect (keyword), which already exist in sentiment DB.
    Lists all negative positve and neutral sentiment to one aspect
    :param aspect: Aspekt to find biases or sentiments in MongoDB
    :param filter: level of confidence (0 - 1) for one sentiment to be included as a sentiment object
    :return: None
    '''
    with connectToMongoDBCollection("Datamining_Srf", "Sentiment") as collectionSentiment:
        mongoDBAnswer = collectionSentiment.find({
            'aspect': aspect
        });

        sentimentArray = []
        connectingArticlesNegative = []
        connectingArticlesPositive = []

        #empty array und 'Unknown sind Standartwerte falls die Werte nicht existieren würden'
        for sentimentObject in mongoDBAnswer:
            for sample in sentimentObject.get('samples', []):
                sentiment = sample.get('sentiment', 'Unknown')
                score = sample.get('score', -1)
                if score > filter:
                    sentimentArray.append(sentiment)
                if (sentiment == 'negative'):
                    connectingArticlesNegative.append(sample.get('title'))
                if (sentiment == 'positive'):
                    connectingArticlesPositive.append(sample.get('title'))
        print("Negative Sentiments: " + str(sentimentArray.count("negative")))
        print("Neutrale Sentiments: " + str(sentimentArray.count("neutral")))
        print("Positive Sentiments: " + str(sentimentArray.count("positive")))
        print("Articles related to sentiments negative" + str(connectingArticlesNegative))
        print("Articles related to sentiments positive" + str(connectingArticlesPositive))

sentimentAnalysis("Trump", 0.9)