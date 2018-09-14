# -*- coding: utf-8 -*-
import logging
import sys
import scrapy
from scrapy.exceptions import CloseSpider
from items import BiertotoItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BiertotoSpider(scrapy.Spider):
    name = 'biertoto'
    # TODO: get rid of hard coded tipper names
    players = ['Uwe', 'Schadix', 'TorstenFG']
    matchday = 1

    def __init__(self, *args, **kwargs):
        logger_scrapy = logging.getLogger('scrapy')
        logger_scrapy.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        url = 'https://www.kicktipp.de/watweissich/tippuebersicht?'
        matchday = getattr(self, 'spieltag', None)
        self.username = getattr(self, 'username', None)
        self.password = getattr(self, 'password', None)
        if not (self.username and self.password):
            raise CloseSpider("username or password missing")

        self.matchday = matchday if matchday is not None else 1
        url = url + '&spieltagIndex=' + matchday
        logger.debug('requesting url: {}'.format(url))
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

        for i in range(0, 9):
            tipp_torstenfg_guest, tipp_torstenfg_home, tipp_schadix_guest, tipp_schadix_home, tipp_uwe_guest, tipp_uwe_home = [""] * 6
            home_team = response.selector.xpath(game_xpath.format(i + 1, 2)).extract_first()
            guest_team = response.selector.xpath(game_xpath.format(i + 1, 3)).extract_first()
            game_date = response.selector.xpath(game_xpath.format(i + 1, 1)).extract_first()
            home_goals = response.selector.xpath(goals_xpath.format(4 + i, 1)).extract_first()
            guest_goals = response.selector.xpath(goals_xpath.format(4 + i, 3)).extract_first()

            for nr, player in enumerate(self.players):
                player_name = response.selector.xpath(player_xpath.format(nr + 1)).extract_first()
                player_goals_extracted = response.xpath(player_goals_xpath.format(nr + 1, 4 + i)).extract_first()
                player_goals_home, player_goals_guest = [""] * 2
                if player_goals_extracted:
                    player_goals_home, player_goals_guest = player_goals_extracted.split(':')
                else:
                    logger.error('no player goals found for player: {} and game: {}-{}: '
                                 .format(player_name, home_team, guest_team))

                if player_name == 'Uwe':
                    tipp_uwe_home = player_goals_home
                    tipp_uwe_guest = player_goals_guest
                elif player_name == 'Schadix':
                    tipp_schadix_home = player_goals_home
                    tipp_schadix_guest = player_goals_guest
                elif player_name == 'TorstenFG':
                    tipp_torstenfg_home = player_goals_home
                    tipp_torstenfg_guest = player_goals_guest
                else:
                    logger.error("didn't find player name: {}".format(player_name))
                    sys.exit(1)

            # ideal for players dict: [{playername: {home_goals: x, guest_goals: y}}, ]
            biertoto_item = BiertotoItem(
                matchday=self.matchday,
                match_date=game_date,
                home_team=home_team,
                guest_team=guest_team,
                home_goals=home_goals,
                guest_goals=guest_goals,
                tipp_uwe_home=tipp_uwe_home,
                tipp_uwe_guest=tipp_uwe_guest,
                tipp_schadix_home=tipp_schadix_home,
                tipp_schadix_guest=tipp_schadix_guest,
                tipp_torstenfg_home=tipp_torstenfg_home,
                tipp_torstenfg_guest=tipp_torstenfg_guest
            )
            games.append(biertoto_item)
            logger.debug(biertoto_item)
            yield biertoto_item

        # logger.info("spiele: {}".format(games))
        # print("response: {}".format(dir(response)))
        # print("response.body: {}".format(response.body))
        # continue scraping with authenticated session...
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
