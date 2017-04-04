from django.http import JsonResponse

from eGamesRecommenderSystem import recommender
from eGamesRecommenderSystem.models import *
from django.http import HttpResponse


# Create your views here.
def recommend_game(request, game_id):
    password = "85d46f2d-48b9-4906-bf16-aad9237b79f9"

    token = None
    if request.META["HTTP_AUTHORIZATION"]:
        token = request.META["HTTP_AUTHORIZATION"].strip()
    if token is not None and token==password:
        game = Game.objects.filter(id=game_id)[0]
        if game is not None:
            list_recommended = recommender.recommend_game(game)
        else:
            list_recommended = []
        res = JsonResponse(list_recommended, safe=False)
    else:
        res = HttpResponse('Unauthorized', status=401)
    return res

