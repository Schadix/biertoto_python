# -*- coding: utf-8 -*-
import logging
import scrapy
from scrapy.exceptions import CloseSpider
from items import BiertotoItem


class BiertotoSpider(scrapy.Spider):
    name = 'biertoto'
    matchday = 1

    def __init__(self, *args, **kwargs):
        scrapy_logger = logging.getLogger('scrapy')
        scrapy_logger.setLevel(logging.WARNING)
        self.players = []
        self.username = ""
        self.password = ""
        self.tipprunde = ""

        super(BiertotoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        matchday = getattr(self, 'spieltag', None)
        self.username = getattr(self, 'username', None)
        self.password = getattr(self, 'password', None)
        self.tipprunde = getattr(self, 'tipprunde', None)

        if not (self.username and self.password):
            raise CloseSpider("username or password missing")

        if not (self.tipprunde):
            raise CloseSpider("no tipprunde defined")

        if not (getattr(self, 'tipper', None)):
            raise CloseSpider("to tipper defined")
        else:
            self.players = str(getattr(self, 'tipper', None)).split(',')

        url = 'https://www.kicktipp.de/{}/tippuebersicht?'.format(self.tipprunde)

        self.matchday = matchday if matchday is not None else 1
        url = url + '&spieltagIndex=' + matchday
        self.logger.info('requesting url: {}'.format(url))
        self.logger.debug('players: {}'.format(self.players))

        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'kennung': self.username, 'passwort': self.password},
            callback=self.after_login
        )

    def after_login(self, response):
        if response.status != 200:
            raise CloseSpider("Login failed.")

        games = []

        game_base_xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div/table/tbody/'
        game_xpath = game_base_xpath + 'tr[{}]/td[{}]/text()'

        goals_base_xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[4]/table/thead/tr[3]/'
        goals_xpath = goals_base_xpath + 'th[{}]/span/span[{}]/text()'

        player_base_xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[4]/table/tbody/'
        player_xpath = player_base_xpath + 'tr[{}]/td[3]/div/text()'
        player_goals_xpath = player_base_xpath + 'tr[{}]/td[{}]/text()'

        players_on_page = response.selector.xpath(
            '/html/body/div[1]/div[2]/div[2]/div[2]/div[4]/table/tbody/tr[*]/td[3]/div/text()').extract()

        for i in range(0, 9):

            home_team = response.selector.xpath(game_xpath.format(i + 1, 2)).extract_first()
            guest_team = response.selector.xpath(game_xpath.format(i + 1, 3)).extract_first()
            game_date = response.selector.xpath(game_xpath.format(i + 1, 1)).extract_first()
            home_goals = response.selector.xpath(goals_xpath.format(4 + i, 1)).extract_first()
            guest_goals = response.selector.xpath(goals_xpath.format(4 + i, 3)).extract_first()

            home_goals = "" if home_goals == '-' else home_goals
            guest_goals = "" if guest_goals == '-' else guest_goals
            tipps = [('', '')]*len(self.players)

            for nr, player in enumerate(players_on_page):
                player_name = response.selector.xpath(player_xpath.format(nr + 1)).extract_first()
                try:
                    pos_in_index = self.players.index(player_name)
                except ValueError as ve:
                    self.logger.error("didn't find player name: {} in list. Will not be output in csv.".format(player_name))
                    continue

                player_goals_extracted = response.xpath(player_goals_xpath.format(nr + 1, 4 + i)).extract_first()
                player_goals_home, player_goals_guest = [""] * 2
                if player_goals_extracted and not "-" in player_goals_extracted:
                    player_goals_home, player_goals_guest = player_goals_extracted.split(':')
                else:
                    self.logger.warning('no player goals found for player: {} and game: {}-{}: '
                                        .format(player_name, home_team.encode('utf-8'), guest_team.encode('utf-8')))
                tipps[pos_in_index] = (player_goals_home, player_goals_guest)

            # ideal for players dict: [{playername: {home_goals: x, guest_goals: y}}, ]
            biertoto_item = BiertotoItem(
                matchday=self.matchday,
                match_date=game_date,
                home_team=home_team,
                guest_team=guest_team,
                home_goals=home_goals,
                guest_goals=guest_goals,
                tipps=tipps
            )
            games.append(biertoto_item)
            self.logger.debug(biertoto_item)
            yield biertoto_item

        # self.loggerinfo("spiele: {}".format(games))
        # print("response: {}".format(dir(response)))
        # print("response.body: {}".format(response.body))
        # continue scraping with authenticated session...
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
