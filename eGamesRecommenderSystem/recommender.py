from django.db.models import Q
from pattern.vector import Document, distance, Model, TFIDF
from eGamesRecommenderSystem.models import *
import random


def recommendable_games(this_game):
    return Game.objects.all().filter(~Q(title=this_game.title, platform=this_game.platform),
                                     (Q(platform=this_game.platform))).values("title", "platform").distinct()


def recommend_game(this_game):
    games = recommendable_games(this_game)

    total_recommendable = games.count()
    print 'Total recommendable games based on ' + this_game.title + ": " + total_recommendable.__str__()

    document_title = Document(this_game.title)
    document_publisher = Document(this_game.publisher)
    document_summary = Document(this_game.summary,
                                top=None,
                                threshold=0,
                                stemmer=None,
                                exclude=[],
                                stopwords=False,
                                language='en')
    document_keywords = Document(', '.join([x['name'] for x in this_game.keywords.all().values("name")]))
    document_genres = Document(', '.join([x['name'] for x in this_game.genres.all().values("name")]))

    # format: {"id":id, socre:"SUM(dist*pond)"}
    game_similarities = []
    summary_documents = []
    for game in games:
        score = 0
        game = Game.objects.filter(title=game['title'], platform=game['platform'])[0]

        title_similarity = 1 - distance(document_title.vector, Document(game.title).vector)
        publisher_similarity = 1 - distance(document_publisher.vector, Document(game.publisher).vector)
        genre_similarity = 1 - distance(document_genres.vector, Document(
            ', '.join([x['name'] for x in game.genres.all().values("name")])
        ).vector)
        keywords_similarity = 1 - distance(document_keywords.vector, Document(
            ', '.join([x['name'] for x in game.keywords.all().values("name")])
        ).vector)

        score = (0.15 * title_similarity) + (0.2 * genre_similarity) + (0.2 * publisher_similarity) + (
            0.20 * keywords_similarity)

        summary_documents.append(Document(game.summary,
                                          top=None,
                                          threshold=0,
                                          stemmer=None,
                                          exclude=[],
                                          stopwords=False,
                                          language='en',
                                          name=game.id))

        game_similarities.append({"id": game.id, "score": score})

    to_compare = Document(document_summary)

    model = Model(documents=summary_documents, weight=TFIDF)

    neighbours = model.neighbors(to_compare, top=total_recommendable)

    for neighbour in neighbours:
        for rec_game in game_similarities:
            if rec_game['id'] == neighbour[1].name:
                rec_game['score'] = rec_game['score'] + 0.25 * neighbour[0]

    recommended = sorted(game_similarities, key=lambda k: -k['score'])[0:total_recommendable]

    if len(recommended) >= 40:
        random_selection = random.sample(recommended[0:40], 25)
    else:
        random_selection = random.sample(recommended, 25)

    recommended_ids = [g['id'] for g in random_selection]

    return recommended_ids
