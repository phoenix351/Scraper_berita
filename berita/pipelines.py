# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from  berita import NER_processing 

class BeritaPipeline(object):
    def process_item(self, item, spider):

        if len(item.get('isi_artikel'))<10:
            raise  DropItem("Missing isi_artikel %s" % item)
        

        #doing ner modeling
        ner_result = NER_processing.ner_modeling(item['isi_artikel'])

        ner_result[3] = NER_processing.filter_indikator(ner_result[3])[0]
        
        query_ner = "INSERT INTO ner_tmp (tanggal,tokoh,organisasi,posisi,indikator,lokasi,kutipan) VALUES (%s,%s,%s,%s,%s,%s,%s)" 
        
        parameter = (
            item['tanggal'],
            ner_result[0],
            ner_result[1],
            ner_result[2],
            ner_result[3],
            ner_result[4],
            ner_result[5]
            )
        try:
            spider.cursor.execute(query_ner, parameter)
            spider.connection.commit()
            print(spider.cursor.rowcount, "record inserted.")

        except Exception as ex:
            spider.connection.rollback()
            print(ex)




        kelas = NER_processing.filter_indikator(ner_result[3])[1]

        query = "INSERT INTO berita (judul, penulis,tanggal,isi,tag,sumber,kelas) VALUES (%s, %s, %s, %s,%s,%s,%s)"
        params = (
            item['judul'],
            item['penulis'],
            item['tanggal'],
            item['isi_artikel'],
            item['tag'],
            item['sumber'],
            kelas
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
