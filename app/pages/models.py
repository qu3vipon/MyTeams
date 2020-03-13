from django.contrib.auth import get_user_model
from django.db import models

from pages.managers import TeamManager

User = get_user_model()


class League(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sports = models.CharField(max_length=50)
    nation = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    league = models.ForeignKey('League', related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    supporter = models.ManyToManyField(User, blank=True, related_name='teams')

    objects = TeamManager()

    def __str__(self):
        return self.name


class Match(models.Model):
    datetime = models.DateTimeField()
    place = models.CharField(max_length=50)
    team_left = models.ForeignKey('Team', related_name='match_left', on_delete=models.CASCADE)
    team_right = models.ForeignKey('Team', related_name='match_right', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'match'
        verbose_name_plural = 'matches'
        ordering = ['datetime']
        indexes = [
            models.Index(fields=['datetime']),
        ]

    def __str__(self):
        return f'{self.datetime.strftime("%y/%m/%d %H:%M")} {self.team_left} vs. {self.team_right} '
