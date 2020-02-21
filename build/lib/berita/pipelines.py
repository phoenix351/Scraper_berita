# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BeritaPipeline(object):
    def process_item(self, item, spider):
        query = "INSERT INTO berita (judul, penulis,tanggal,isi) VALUES (%s, %s, %s, %s)"
        params = (
            item['judul'],
            item['penulis'],
            ''.join(item['tanggal']),
            ''.join(item['isi_artikel'])
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
