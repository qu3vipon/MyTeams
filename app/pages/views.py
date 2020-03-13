from allauth.account.forms import AddEmailForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, FormView

from config.settings import LEFT_HOME_LEAGUES, RIGHT_HOME_LEAGUES
from .models import League, Team
from .utils import make_calendar, matches_today


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['matches_today'] = matches_today(self.request.user)
        context['home_left'] = LEFT_HOME_LEAGUES
        context['home_right'] = RIGHT_HOME_LEAGUES
        return context


class TeamListView(LoginRequiredMixin, ListView):
    queryset = League.objects.prefetch_related('teams')
    context_object_name = 'leagues'
    template_name = 'pages/team_list.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        team_pk_list = request.POST.getlist('team_pk')

        user.teams.clear()
        for team_pk in team_pk_list:
            team = Team.objects.get(pk=team_pk)
            user.teams.add(team)

        return redirect('team_list')


class CalendarTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = make_calendar(self.request.user)
        return context


class EmailFormView(FormView):
    template_name = 'pages/email.html'
    form_class = AddEmailForm
    success_url = '/email/'
