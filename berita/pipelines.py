# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class BeritaPipeline(object):
    def process_item(self, item, spider):
        if len(item.get('isi_artikel'))<10:
            raise  DropItem("Missing isi_artikel %s" % item)
        

        query = "INSERT INTO berita (judul, penulis,tanggal,isi,tag,sumber) VALUES (%s, %s, %s, %s,%s,%s)"
        params = (
            item['judul'],
            item['penulis'],
            item['tanggal'],
            item['isi_artikel'],
            item['tag'],
            item['sumber']
        )

# debug
        try:
            spider.cursor.execute(query, params)
            spider.connection.commit()
            print(spider.cursor.rowcount, "record inserted.")

        except Exception as ex:
            spider.connection.rollback()
            print(ex)
        return item
