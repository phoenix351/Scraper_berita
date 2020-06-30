# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import remove_tags
import re


def clear_mr(teks):
    teks = re.sub(r'\\\w+', '', teks)
    return teks


class BeritaItem(scrapy.Item):
    judul = scrapy.Field(
        input_processor=MapCompose(remove_tags, clear_mr),
        output_processor=Join()
    )
    tanggal = scrapy.Field(

    )
    isi_artikel = scrapy.Field(
        input_processor=MapCompose(remove_tags, clear_mr),
        output_processor=Join()
    )
    tag = scrapy.Field()
    sumber = scrapy.Field()
