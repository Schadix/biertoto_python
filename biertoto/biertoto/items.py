# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# TODO: get rid of hardcoded tipper names and use a list of dicts instead
class BiertotoItem(scrapy.Item):
    matchday = scrapy.Field()
    match_date = scrapy.Field()
    home_team = scrapy.Field()
    guest_team = scrapy.Field()
    home_goals = scrapy.Field()
    guest_goals = scrapy.Field()
    tipp_uwe_home = scrapy.Field()
    tipp_uwe_guest = scrapy.Field()
    tipp_schadix_home = scrapy.Field()
    tipp_schadix_guest = scrapy.Field()
    tipp_torstenfg_home = scrapy.Field()
    tipp_torstenfg_guest = scrapy.Field()
