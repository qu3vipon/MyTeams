import calendar
import datetime

from django.db.models import Q

from .models import Match


# calendar 테이블 생성을 위해 [[(날짜, 경기 정보), ...], ... ] 형태로 데이터 전달
def make_calendar(user):
    today = datetime.datetime.today()
    cal_dict = dict()
    cal_dict['title'] = f'{calendar.month_name[today.month]} {today.year}'
    cal_dict['weekheader'] = calendar.weekheader(3).split()

    cal_dict['body'] = body_init(cal_dict, today.year, today.month)
    match_list = matches_this_month(user, today.year, today.month)

    for idx_match, match in enumerate(match_list):
        if match != []:
            for idx_week, week in enumerate(cal_dict['body']):
                for idx_day, day in enumerate(week):
                    if day[0] == idx_match + 1:
                        cal_dict['body'][idx_week][idx_day] = (idx_match + 1, match)

    return cal_dict


# 해당 달에 있는 경기를 검색해서 반환
def matches_this_month(user, year, month):
    teams = user.teams.all()
    matches = Match.objects.none()
    for team in teams:
        matches |= Match.objects.filter(Q(team_left_id=team.pk) | Q(team_right_id=team.pk)).filter(datetime__year=year,
                                                                                                   datetime__month=month)

    _, days = calendar.monthrange(year, month)
    match_list = [[] for _ in range(days)]

    for match in matches:
        match_list[match.datetime.day - 1].append(match)

    return match_list


def matches_today(user):
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day

    teams = user.teams.all()
    matches = Match.objects.none()
    for team in teams:
        matches |= Match.objects.filter(Q(team_left_id=team.pk) | Q(team_right_id=team.pk)).filter(datetime__year=year,
                                                                                                   datetime__month=month,
                                                                                                   datetime__day=day)
    return matches


# cal_dict['body']를 (0, 0)으로 초기화
def body_init(cal_dict, year, month):
    cal = calendar.monthcalendar(year, month)
    n_row = len(cal)
    cal_dict['body'] = []
    for _ in range(n_row):
        cal_dict['body'].append([(0, 0) for _ in range(7)])

    for i in range(n_row):
        for j in range(7):
            if cal[i][j] != 0:
                cal_dict['body'][i][j] = (cal[i][j], 0)

    return cal_dict['body']
