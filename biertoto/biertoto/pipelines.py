# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from biertoto_exporter import CsvBiertotoItemExporter
from scrapy.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Pipeline is actually not used, just left here for reference
class BiertotoPipeline(object):

    def open_spider(self, spider):
        output_csv_file = "{}-{}-{}.csv".format(spider.name, spider.tipprunde, spider.matchday) if not settings.get('FEED_URI') else settings.get('FEED_URI')
        self.output_csv = open(output_csv_file, 'w')
        self.exporter = CsvBiertotoItemExporter(
            self.output_csv,
            fields_to_export=settings.getlist('FEED_EXPORT_FIELDS'))

    def process_item(self, item, spider):
        logger.info('from pipeline, item: {}'.format(item))
        self.exporter.export_item(item=item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.output_csv.close()
