import os
import re

import django
from bs4 import BeautifulSoup
from django.utils.dateparse import parse_datetime
from selenium import webdriver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pages.models import Match, Team, League

driver = webdriver.Chrome('/Users/dong-hyeonShin/Downloads/Setup/chromedriver')

URL_EPL = ('https://sports.news.naver.com/wfootball/schedule/index.nhn', 'EPL')
URL_PRIMERA = ('https://sports.news.naver.com/wfootball/schedule/index.nhn?category=primera', 'PRIMERA')
URL_MLB = ('https://sports.news.naver.com/wbaseball/schedule/index.nhn', 'MLB')

URLS = [URL_EPL, URL_PRIMERA, URL_MLB]


def parser(url):
    # url을 입력 받아서 soup 객체 생성
    def making_soup(url):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # 경기가 없는 날의 데이터 제외
    def valid_matching_data(soup):
        match_data = []
        for data in soup.select("#_monthlyScheduleList > tr"):
            if "empty" in data.div['class']:
                continue
            else:
                match_data.append(data)
        return match_data

    # 정규표현식으로 불필요한 내용 제거, 팀 이름만 추출
    def pick_up_name_only(text):
        pattern = re.compile(r"^(.*)\n")
        if re.match(pattern, text) is None:
            return text
        else:
            return re.match(pattern, text).group(1)

    # tr 태그를 파싱해서 경기시간, 장소, 팀 정보 반환
    def tr_parser(tr):
        time = tr.find("span", {"class": "time"}).text.strip()
        place = tr.find("span", {"class": "place"}).text.strip()
        team_left = pick_up_name_only(tr.find("span", {"class": "team_left"}).text.strip())
        team_right = pick_up_name_only(tr.find("span", {"class": "team_right"}).text.strip())

        return {"time": time,
                "place": place,
                "team_left": team_left,
                "team_right": team_right}

    # 경기날짜(월, 일) 지정
    def matching_info(valid_data):
        result = []
        for tr in valid_data:
            # tr 태그에 "division" 클래스 기준으로 날짜 분류
            if tr.attrs:
                if "division" in tr['class']:
                    match_date = tr.em.text.strip().split('.')
                    month = match_date[0]
                    day = match_date[1]

                    match_info = tr_parser(tr)
                    match_info["month"] = month
                    match_info["day"] = day
                    result.append(match_info)
            else:
                match_info = tr_parser(tr)
                match_info["month"] = month
                match_info["day"] = day
                result.append(match_info)
        return result

    # 연도 정보 추가
    def add_year(soup, result):
        year = soup.select('#_monthList > li.selected')[0]['data-yearmonth'][:4]
        result.append({'year': year})
        return result

    soup = making_soup(url)
    valid_data = valid_matching_data(soup)
    yearless_data = matching_info(valid_data)
    all_data = add_year(soup, yearless_data)

    return all_data


if __name__ == '__main__':
    for url in URLS:
        data_list = parser(url[0])
        LEAGUE = url[1]
        dct = data_list.pop()
        YEAR = dct['year']

        for data_dict in data_list:
            datetime_str = f"{YEAR}-{data_dict['month']}-{data_dict['day']} {data_dict['time']}"
            datetime = parse_datetime(datetime_str)

            # 리그는 admin에서 직접 생성
            league = League.objects.get(name=LEAGUE)

            team_cnt = 0
            match_cnt = 0

            team_left, created = Team.objects.get_or_create(league=league, name=data_dict['team_left'])
            if created:
                team_cnt += 1
                print(team_left)
            team_right, created = Team.objects.get_or_create(league=league, name=data_dict['team_right'])
            if created:
                team_cnt += 1
                print(team_right)

            match, created = Match.objects.get_or_create(place=data_dict['place'],
                                                         team_left=team_left,
                                                         team_right=team_right,
                                                         datetime=datetime)
            if created:
                match_cnt += 1
                print(match)
        print(league.name)
        print(f"{team_cnt} TEAMS CREATED")
        print(f"{match_cnt} MATCHES CREATED")
