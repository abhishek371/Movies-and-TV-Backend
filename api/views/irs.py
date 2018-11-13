import codecs
import json
from django.http import JsonResponse
from ..models import Director


NUM_KEYWORDS = 25
BETA = 0.5
IGNORED_WORDS = ["and", "the", "a", "of", "an", "with", "on", "in", "for", "to", "but", "his",
                 "it", "her", "they", "their", "us", "we", "you", "i", "because", "though", "while",
                 "when", "what", "how", "its", "by", "he", "him", "she", "is", "are", "at",
                 "were", "was", "from", "he's", "as", "this", "not", "that"]


def query_director(request, query):
    try:
        director = Director.objects.filter(name=query)
        if not director:
            raise Director.DoesNotExist
        director = director[0]
    except Director.DoesNotExist:
        JsonResponse({"message": "Director with name={} does not exist".format(query)}, status=400)
    movies = director.movie_set.all()
    vocab_vals = {}
    for movie in movies:
        movie_word = {}
        for word in movie.title.lower().split(" ") + movie.plot.lower().split(" "):
            if word in IGNORED_WORDS:
                continue
            if word not in vocab_vals:
                vocab_vals[word] = [1, 1]
            else:
                if word not in movie_word:
                    movie_word[word] = True
                    vocab_vals[word][0] += 1
                vocab_vals[word][1] += 1
    ranking = []
    max_val = 0
    for key, val in vocab_vals.items():
        ranking.append((key, val[0] * val[1]))
        max_val = max(max_val, val[0] * val[1])
    ranking.sort(key=lambda x: x[1], reverse=True)
    print(ranking)
    print("\n\n")
    ranking = ranking[:NUM_KEYWORDS]
    ranks = {}
    for entry in ranking:
        ranks[entry[0]] = (BETA * entry[1]) / max_val
    # for word in query.lower().split(" "):
    #     ranks[word] = 1
    print(ranks)
    print("\n\n\n")
    movie_collection = codecs.open("api/data/movie_collection.json", encoding="utf_8", errors="ignore").read()
    collection = json.loads(movie_collection)
    # tv_collection = codecs.open("api/data/tv_collection.json", encoding="utf_8", errors="ignore").read()
    # collection += json.loads(tv_collection)
    results = []
    for index, doc in enumerate(collection):
        score = 0
        data = []
        for key, val in doc.items():
            if key == "seasons":
                continue
            if key in ["languages", "origin_country"]:
                data += val
                continue
            if isinstance(val, list):
                for item in val:
                    for k, v in item.items():
                        data += str(v).lower().split(" ")
            else:
                data += str(val).lower().split(" ")
        # data = " ".join(data)
        # data = " ".join([str(doc[key]) for key in doc.keys()])
        if index == 1:
            print(data)
            print("\n\n\n")
        for word in data:
            if word in ranks:
                score += ranks[word]
        results.append((index, score))
    results.sort(key=lambda x: x[1], reverse=True)
    results = results[:15]
    response = []
    for result in results:
        response.append(collection[result[0]])
    print(json.dumps(response[0], indent=4))
    return JsonResponse({"response": response}, status=200)
