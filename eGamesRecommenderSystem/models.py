from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=120)
    platform = models.ForeignKey("Platform")
    genres = models.ManyToManyField("Genre", through="GameGenre")
    publisher = models.CharField(max_length=120)
    summary = models.TextField(null=True)
    story_line = models.TextField(null=True)
    time_to_beat = models.IntegerField(null=True)
    game_modes = models.ManyToManyField("GameMode", through="GameGameMode")
    keywords = models.ManyToManyField("Keyword",through="GameKeyword")
    first_release_date = models.DateField(null=True)
    cover_url = models.URLField(null=True)

    class Meta:
        db_table = 'game'

    def __unicode__(self):
        return self.id.__str__()


class Platform(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'platform'

    def __unicode__(self):
        return self.name.__str__()


class GameMode(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'game_mode'

    def __unicode__(self):
        return self.name.__str__()


class Keyword(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'keyword'

    def __unicode__(self):
        return self.name.__str__()


class Genre(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'genre'

    def __unicode__(self):
        return self.name.__str__()

class GameGenre(models.Model):
    game = models.ForeignKey(Game)
    genres = models.ForeignKey(Genre)

    class Meta:
        db_table = 'game_genres'

    def __unicode__(self):
        return self.id.__str__()


class GameGameMode(models.Model):
    game = models.ForeignKey(Game)
    game_modes = models.ForeignKey(GameMode)

    class Meta:
        db_table = 'game_game_modes'

    def __unicode__(self):
        return self.id.__str__()


class GameKeyword(models.Model):
    game = models.ForeignKey(Game)
    keywords = models.ForeignKey(Keyword)

    class Meta:
        db_table = 'game_keywords'

    def __unicode__(self):
        return self.id.__str__()
