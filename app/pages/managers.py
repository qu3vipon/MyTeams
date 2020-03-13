from django.db import models
from django.db.models import Func


class TeamManager(models.Manager):
    def get_queryset(self):
        name_kr = Func(
            'name',
            function='C',
            template='(%(expressions)s) COLLATE "%(function)s"')
        return super().get_queryset().order_by('league_id', name_kr.asc())
