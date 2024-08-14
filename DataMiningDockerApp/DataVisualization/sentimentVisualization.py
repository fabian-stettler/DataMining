import pandas as pd
import plotly.express as px

from DataVisualization.sentimentAnalysis import sentimentAnalysis
from connectToMongoDBCollection import connectToMongoDBCollection
from constants import SCHWELLWERT_SENTIMENT_CONFIDENCE


def generateSentimentVisualization(aspect, filter=0.9):
    '''
    Simple visualization of one aspect and its sentiment
    :param aspect:
    :param filter:
    :return:
    '''
    #MongoDB Query
    with connectToMongoDBCollection("Datamining_Srf", "Sentiment") as collection:
        answerMongoSentiment = collection.find({
            'samples.score': {"$gt": 0.9},
            'aspect': aspect
        })
        #generate df object
        df = generateDF(answerMongoSentiment)
        #Generieren des Plotly Express Outputs
        generatePlotlyExpressImageSimple(aspect, df)




def generateComparitiveSentimentVisualization(aspects, filter=0.9):
    '''
    control script of sentiment Visualization where there is more than one aspect.
    :param aspects:
    :param filter:
    :return:
    '''
    combined_dfs = []

    with connectToMongoDBCollection("Datamining_Srf", "Sentiment") as collection:
        for aspect in aspects:
            answerMongoSentiment = collection.find({
                'samples.score': {"$gt": filter},
                'aspect': aspect
            })
            df = generateDF(answerMongoSentiment)
            df['aspect'] = aspect  # Aspekt als zusätzliche Spalte hinzufügen
            combined_dfs.append(df)

    df_combined = pd.concat(combined_dfs, ignore_index=True)
    generatePlotlyExpressImageComparative(aspects, df_combined)
    
def generateDF(answerMongoSentiment):
    '''
    parses mongoDB answer and creates one dataFrame Object.
    :param answerMongoSentiment: MongoDB Answer from the query
    :return: data frame object
    '''
    # Data Processing und Data Frame Generierung
    results = []
    for sentimentObject in answerMongoSentiment:
        for sampleMongoArray in sentimentObject.get('samples', []):
            if sampleMongoArray['score'] > 0.9:
                results.append(sampleMongoArray)
    df = pd.DataFrame(results)
    return df

def generatePlotlyExpressImageSimple(aspect, df):
    '''
    Generates a simple bar chart with only one aspects its negative and positive occurences
    :param aspect: One Keyword or aspect
    :param df: df with samples array
    :return:
    '''
    # df_neutral = df[df['sentiment'] == 'neutral']
    # mit df['sentiment'] wird eine series erstellt und mit reset_index, wird der zuvor gewählte index 'sentiment' reseted
    # und damit die series in ein dataframe umgewandelt
    sentimentCount = df['sentiment'].value_counts().reset_index()
    # Benennung der columns
    sentimentCount.columns = ['sentiment', 'count']
    titlePlot = f'Sentiment Count for {aspect}'
    # Definition des plotly express Objektes
    fig = px.bar(sentimentCount, x='sentiment', y='count', title=titlePlot)
    fig.show()

def generatePlotlyExpressImageComparative(aspects, df):
    '''
    generates a plotly express diagramm for multiple aspects
    :param aspects: array of aspects
    :param df: dataframe with all indizes of samples[] and additional column for aspect. Aspect colum does not exist in @function ImageSimple
    :return: None
    '''
    sentimentCount = df.groupby(['aspect', 'sentiment']).size().reset_index(name='count')
    titlePlot = f'Sentiment Count for {", ".join(aspects)}'
    fig = px.bar(sentimentCount, x='sentiment', y='count', color='aspect', title=titlePlot)
    fig.show()



#generateSentimentVisualization('Trump', SCHWELLWERT_SENTIMENT_CONFIDENCE)
generateComparitiveSentimentVisualization(['Putin', 'Biden'], SCHWELLWERT_SENTIMENT_CONFIDENCE)