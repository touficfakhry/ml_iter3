import pandas as pd
# from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import multiprocessing as mp

# Initialize the sentiment analysis pipeline
# sentiment_pipeline = pipeline('sentiment-analysis')
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_label_vader(text):
    sentiment_dict = analyzer.polarity_scores(text)
    return sentiment_dict

def apply_sentiment_analysis(texts):
    with mp.Pool() as pool:
        results = pool.map(get_sentiment_label_vader, texts)
    return results

# def get_sentiment_label(text):
#     max_length = 512
#     tokens = sentiment_pipeline.tokenizer(text, max_length=max_length, truncation=True)
#     truncated_text = sentiment_pipeline.tokenizer.decode(tokens['input_ids'], skip_special_tokens=True)
#     result = sentiment_pipeline(truncated_text)[0]
#     return result['label'], result['score']

# def apply_sentiment_analysis(texts, n_jobs=4):
#     with mp.Pool(n_jobs) as pool:
#         results = pool.map(get_sentiment_label, texts)
#     return results


df = pd.read_csv("datasets/Phishing_Email_URLS.csv")
# Apply the function to the DataFrame in parallel
# df[['sentiment_label', 'sentiment_score']] = apply_sentiment_analysis(df["Email Text"].tolist(), n_jobs=4)
texts = df['Email Text'].tolist()
sentiment_results = apply_sentiment_analysis(texts)

sentiment_df = pd.DataFrame(sentiment_results)

df_meta = pd.read_csv("./meta-classifier/meta-classifier-dataset.csv")
# df[['sentiment_score', 'sentiment_dict']] = df['Email Text'].apply(lambda x: pd.Series(get_sentiment_label_vader(x)))
df_meta['sentiment_score'] = df['sentiment_score']
df_meta['sentiment_neg'] = sentiment_df['neg']
df_meta['sentiment_neu'] = sentiment_df['neu']
df_meta['sentiment_pos'] = sentiment_df['pos']
df_meta['sentiment_compound'] = sentiment_df['compound']

# Save the results to a CSV file
df_meta.to_csv('df_meta = pd.read_csv("./meta-classifier/meta-classifier-dataset.csv")', index=False)
print("Sentiment analysis completed and results saved.")