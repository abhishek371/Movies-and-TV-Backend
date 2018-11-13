from django.http import Http404, HttpResponse
from ..models import Director
NUM_KEYWORDS = 10
BETA = 0.5
def irs(request):
    try:
        query = str(request.GET['query'])
    except KeyError:
        raise Http404('Incomplete Data')
    
    director = Director.objects.get(name=query)
    movies = director.movies_set.all()
    vocab_vals = {}
    for movie in movies:
        movie_word = {}
        for word in movie.title.lower().split(" ") + movie.plot.lower().split(" "):
            if not vocab_vals[word]:
                vocab_vals[word] = (1, 1)
            else:
                if not movie_word[word]:
                    movie_word[word] = True
                    vocab_vals[word][0] += 1
                vocab_vals[word] += 1
    ranking = []
    max_val = 0
    for key in vocab_vals.keys():
        ranking.append((key, vocab_vals[key][0] * vocab_vals[key][1]))
        max_val = max(max_val, vocab_vals[key][0] * vocab_vals[key][1])
    ranking.sort(key=lambda x: x[1])
    ranking = ranking[:10]
    ranks = {}
    for entry in ranking:
        ranks[entry[0]] = (BETA * entry[1]) / max_val
    for word in query.lower().split(" "):
        ranks[word] = 1
    doc_store = []
    results = []
    for index, doc in enumerate(doc_store):
        score = 0
        data = " ".join([doc[key] for key in doc.keys()])
        for word in data.lower().split():
            if ranks[word]:
                score += ranks[word]
        results.append((index, score))
    results = results[:15]
    results.sort(key=lambda x: x[1])
        