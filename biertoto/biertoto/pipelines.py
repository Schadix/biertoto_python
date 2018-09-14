# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BiertotoPipeline(object):
    def process_item(self, item, spider):
        logger.info('from pipeline, item: {}'.format(item))
        return item
