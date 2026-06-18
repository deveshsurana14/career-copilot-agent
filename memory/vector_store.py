from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:

    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer()


    def add_text(self, text):

        self.documents.append(text)



    def search(self, query):

        corpus = self.documents + [query]

        vectors = self.vectorizer.fit_transform(corpus)


        sims = cosine_similarity(

            vectors[-1],

            vectors[:-1]

        )[0]


        idx = sims.argmax()


        return self.documents[idx]