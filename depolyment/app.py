import nltk
import pickle
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Download NLTK resources
nltk.download('punkt')

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Load the dataset
csv_path = 'C:\\Users\\aarud\\Downloads\\fastapi_app\\netflix\\NETFLIX.csv'
df = pd.read_csv(csv_path)
print(df)  # Print the dataframe to check if it's loaded correctly

df.dropna(inplace=True)

# Preprocess the data
df[['director', 'country']] = df[['director', 'country']].fillna('Unknown')
df['cast'] = df['cast'].fillna('No Cast')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df.dropna(axis=0, inplace=True)

# Preprocessing text data
def identity_tokenizer_func(text):
    return text.split()

# Combine all the clustering attributes into a single column
df['clustering'] = (df['director'] + ' ' + df['cast'] + ' ' + df['country'] + ' ' + df['listed_in'] + ' ' + df['description'])

# Vectorize the text data using TF-IDF
tfidf = TfidfVectorizer(tokenizer=identity_tokenizer_func, lowercase=False, max_features=20000, token_pattern=None)
X = tfidf.fit_transform(df['clustering'])
converted_matrix = X.toarray()

# Calculate the cosine similarity matrix
cosine_similarity_matrix = cosine_similarity(converted_matrix)

# Get the indices and titles of the shows
indices = pd.Series(df.index)
titles = pd.Series(df['title'])

# Load the pre-trained model and related data from pickle file
with open('C:\\Users\\aarud\\Downloads\\fastapi_app\\netflix\\model.pkl', 'rb') as f:
    saved_data = pickle.load(f)
    kmeans = saved_data['kmeans']
    converted_matrix = saved_data['converted_matrix']
  
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommendations/")
def get_recommendations(request: Request, title: str = Form(...)):
    try:
        # Find the index of the requested title
        idx = indices[indices == title].index[0]

        # Get the cosine similarity scores for the requested title
        series = pd.Series(cosine_similarity_matrix[idx]).sort_values(ascending=False)
        top10 = list(series.iloc[1:11].index)

        # Get the titles of the top 10 matching shows
        recommend_content = titles[top10].tolist()

        return templates.TemplateResponse("recommendations.html", {"request": request, "title": title, "recommendations": recommend_content})
    except:
        return templates.TemplateResponse("invalid.html", {"request": request, "title": title})
    import nltk
    from fastapi import FastAPI, Request, Form
    from fastapi.templating import Jinja2Templates
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import pandas as pd


    # Download NLTK resources
    nltk.download('punkt')


    app = FastAPI()
    templates = Jinja2Templates(directory="templates")


    # Load the dataset
    csv_path = 'C:\\Users\\aarud\\Downloads\\fastapi_app\\netflix\\NETFLIX.csv'
    df = pd.read_csv(csv_path)
    print(df)  # Print the dataframe to check if it's loaded correctly


    df.dropna(inplace=True)


    # Preprocess the data
    df[['director', 'country']] = df[['director', 'country']].fillna('Unknown')
    df['cast'] = df['cast'].fillna('No Cast')
    df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
    df.dropna(axis=0, inplace=True)


    # Preprocessing text data
    def identity_tokenizer_func(text):
        return text.split()


    # Combine all the clustering attributes into a single column
    df['clustering'] = (df['director'] + ' ' + df['cast'] + ' ' + df['country'] + ' ' + df['listed_in'] + ' ' + df['description'])


    # Vectorize the text data using TF-IDF
    tfidf = TfidfVectorizer(tokenizer=identity_tokenizer_func, lowercase=False, max_features=20000, token_pattern=None)
    X = tfidf.fit_transform(df['clustering'])
    converted_matrix = X.toarray()


    # Calculate the cosine similarity matrix
    cosine_similarity_matrix = cosine_similarity(converted_matrix)


    # Get the indices and titles of the shows
    indices = pd.Series(df.index)
    titles = pd.Series(df['title'])


    @app.get("/")
    def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})


    @app.post("/recommendations/")
    def get_recommendations(request: Request, title: str = Form(...)):
        try:
            # Find the index of the requested title
            idx = indices[indices == title].index[0]


            # Get the cosine similarity scores for the requested title
            series = pd.Series(cosine_similarity_matrix[idx]).sort_values(ascending=False)
            top10 = list(series.iloc[1:11].index)


            # Get the titles of the top 10 matching shows
            recommend_content = titles[top10].tolist()


            return templates.TemplateResponse("recommendations.html", {"request": request, "title": title, "recommendations": recommend_content})
        except:
            return templates.TemplateResponse("invalid.html", {"request": request, "title": title})



