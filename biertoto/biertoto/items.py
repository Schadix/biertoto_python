# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_tipps(value):
    return [i for sub in value for i in sub]


class BiertotoItem(scrapy.Item):
    matchday = scrapy.Field()
    match_date = scrapy.Field()
    home_team = scrapy.Field()
    guest_team = scrapy.Field()
    home_goals = scrapy.Field()
    guest_goals = scrapy.Field()
    tipps = scrapy.Field(serializer=serialize_tipps)
