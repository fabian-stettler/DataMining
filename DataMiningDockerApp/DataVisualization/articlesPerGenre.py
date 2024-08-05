import pandas as pd
import plotly.express as px

from connectToMongoDBCollection import connectToMongoDBCollection


def articlesPerGenre():
    '''
    Generates a histogram of amounts of articles per genre (base keywords) and includes all articles
    :return:
    '''
    with connectToMongoDBCollection("Datamining_Srf", "Articles") as collection:
        # Retrieve documents from the collection
        data = list(collection.find({}, {'_id': 0, 'base_keywords': 1}))

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Check the first few rows of the dataframe
    print(df.head())

    # Total number of articles
    total_articles = len(df)

    # Filter out the articles with non-null 'base_keywords'
    df_valid = df.dropna(subset=['base_keywords'])
    valid_articles = len(df_valid)

    # Calculate the ratio of valid articles to total articles
    if total_articles > 0:
        valid_ratio = valid_articles / total_articles
    else:
        valid_ratio = 0

    # Print the total number of articles, valid articles, and the ratio
    print(f"Total articles: {total_articles}")
    print(f"Valid articles with non-null genres: {valid_articles}")
    print(f"Ratio of valid articles: {valid_ratio:.2%}")  # Display as percentage

    # Explode the 'base_keywords' list into separate rows, if it's a list of genres
    df_exploded = df.explode('base_keywords')

    # Drop rows where 'base_keywords' is NaN (if there are any)
    df_exploded = df_exploded.dropna(subset=['base_keywords'])

    # Count the number of articles per genre
    genre_counts = df_exploded['base_keywords'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    # Check the aggregated data
    print(genre_counts)


    # Plotting the histogram
    fig = px.bar(genre_counts, x='Genre', y='Count', title='Number of Articles per Base Keyword')
    fig.show()

articlesPerGenre()