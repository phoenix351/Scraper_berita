# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from  berita import NER_processing 
from  berita.NER_processing import kata2list
from berita.sentimen import sentiment
import re
from berita.Database_connection import Database_connection as db
import ast
from concurrent.futures import ThreadPoolExecutor
Thread = ThreadPoolExecutor(max_workers=7)
def justAlphaNum(kata):
    alphanumeric = re.compile(r'[^A-Z0-9]')
    kata = alphanumeric.sub('',kata)
    return kata
def isBerita(url):
    site_berita = re.compile(r'https\:\/\/[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+\/berita\S*\/')
    logika = bool(site_berita.search(url))
    return logika

def isJS(kalimat):
    a = re.compile(r'var\s*[a-zA-Z_]*\s*=\s*[\S]*;')
    b = re.compile(r'let\s*\S*\s*=\s*[\S]*;*')
    c = re.compile(r'function \S+\(\S*\)\s*\{[\s\s]*\}')
    x = bool(a.search(kalimat))
    y = bool(b.search(kalimat))
    z = bool(c.search(kalimat))
    if x or y or z:
        return True
    else:
        return False
def update_indikatorsum(item,indikator,id_indikator):
    """
    item : item hasil scraping
    indikator : string indikator
    id_indikator : string id indikator
    """
    

    #insert summary berita by indikator
    qsum = """
    insert into beritasum_indikator
    values(%s,%s,1)
    on duplicate key update jumlah = jumlah + 1
    """
    param = (item['waktu'],indikator)
    database = db()
    try:
        database.kursor.execute(qsum,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()

    #insert summary indikator
    qind = """
    update indikator_sum 
    set jumlah = jumlah + 1 
    where id_indikator like %s    
    """
    param1 = ('%'+id_indikator+'%',)
    database = db()
    try:
        database.kursor.execute(qind,param1)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def simpan_tag(waktu,tag):
    """
    tag : string tag berita
    waktu : string dengan format %Y-%m-%d atau python datetime.datetime
    """
    query = """
    insert into sum_tags
    values(%s,%s,1)
    on duplicate key update jumlah = jumlah + 1
    """
    param = (waktu,tag)
    database = db()
    try:
        database.kursor.execute(query,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def proses_tags(waktu,tags):
    """
    waktu : string dengan format %Y-%m-%d atau python datetime.datetime
    tags : string representation of list 
    """
    non_alphanumeric = re.compile(r'[^a-zA-Z0-9\s]')
    space = re.compile(r'\s+')
    tags = kata2list(tags)
    for tag in tags:
        #remove non alphanumeric
        tag = non_alphanumeric.sub('',tag)
        #remove unnecesry space / tab
        tag = space.sub(' ',tag)
        #cek valid tag jika lebih dari 3
        if len(tag) > 3:
            #simpan pada sum tag table
            simpan_tag(tag)


def simpan_sentimen(id_berita,id_indikator,sentimen_isi,sentimen_kutipan):

    querysent = """
    insert into sentimen 
    values(%s,%s,%s,%s,%s)
    on duplicate key update 
    id_indikator = %s,
    indikator= %s,
    sentimen = %s 
    """
    #parameter sentimen isi
    par_isi = (id_berita,id_indikator,indikator,sentimen_isi,'isi',
        id_indikator,indikator,sentimen_isi)
    #parameter sentimen kutipan
    par_kutipan = (id_berita,id_indikator,indikator,sentimen_kutipan,'kutipan',
        id_indikator,indikator,sentimen_kutipan)
    #prepare  database connection
    database = db()
    #execute 
    try:
        database.kursor.execute(querysent,par_isi)
        database.koneksi.commit()
    #catch if any error is occurred
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    #close connection
    database.tutup()

    #prepare  database connection
    database = db()
    try:
        database.kursor.execute(querysent,par_kutipan)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def proses_sentimen(id_berita,id_indikator,indikator,konten,kutipan):
    """
    id_berita : int id_berita
    id_indikator : string id_indikator
    indikator : string indikator
    konten : isi artikel dari item hasil scraping
    kutipan : kutipan tokoh hasil modeling NER
    """
    #lakukan klasifikasi Sentimen
    hasil_sentimen = sentiment(id_berita,konten,kutipan,indikator)
    #preparing for save data
    sentimen_isi = hasil_sentimen['sentimen_isi']
    sentimen_kutipan = hasil_sentimen['sentimen_kutipan']
    #simpan
    Thread.submit(simpan_sentimen,id_berita,id_indikator,indikator,sentimen_isi,sentimen_kutipan) 
    
def simpan_ner(ner_result,id_berita):
    query_ner = """
    INSERT INTO ner_output (id_berita,indikator,tokoh,organisasi,posisi,lokasi,kutipan) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """ 
    parameter = (
        id_berita,
        ner_result['indikator'],
        ner_result['tokoh'],
        ner_result['organisasi'],
        ner_result['posisi'],
        ner_result['lokasi'],
        ner_result['kutipan'])
    
    database = db()
    try:
        database.kursor.execute(query_ner,parameter)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def proses_ner(item,id_berita):
    ner_result = NER_processing.ner_modeling(item['isi_artikel'],id_berita)
    
    #ubah hasil NER kategori NER indikator menjadi id_indikator dan indikator 
    indikator_list = ast.literal_eval(ner_result['indikator'])
    for row in indikator_list:
        id_indikator = row['id_indikator']
        id_indikator = justAlphaNum(id_indikator)
        indikator = row['indikator']
        indikator = justAlphaNum(indikator)
        if len(id_indikator) < 3:
            continue

        print("indikator terdeteksi ! = ",id_indikator)
        print("update indikator sum...")
        Thread.submit(update_indikatorsum,item,indikator,id_indikator)    
        print("simpan_ner...")
        Thread.submit(simpan_ner,ner_result,id_berita)
        kutipan = ' '.join(kata2list(ner_result['kutipan']))
        konten = item['isi_artikel']
        print("proses_sentimen...")
        proses_sentimen(id_berita,id_indikator,indikator,konten,kutipan)
    
    return True
def insert_sum_sumber(waktu,sumber):
    #insert summary berita by sumber
    qsum = """
    insert into beritasum_sumber
    values(%s,%s,1)
    on duplicate key update jumlah = jumlah + 1 
    """
    param = (item['waktu'],item['sumber'])
    database = db()
    try:
        database.kursor.execute(qsum,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
    database.tutup()

def insert_berita(item):
    
    waktu = item['waktu']
    sumber = item['sumber']
    #insert summary waktu dan sumber
    Thread.submit(insert_sum_sumber,waktu,sumber)

    query = """INSERT INTO berita_detail (judul,waktu,tag,isi,sumber) 
        VALUES (%s, %s, %s, %s,%s)
        """
    params = (
        item['judul'],
        item['waktu'],
        item['tag'],
        item['isi_artikel'],
        item['sumber'],
        )
    # open
    database = db()
    try:
        database.kursor.execute(query, params)
        database.koneksi.commit()
        print(database.kursor.rowcount, "berita berhasil di simpan!")
        id_generated = database.kursor.lastrowid
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
        return 0
    database.tutup()
    return id_generated
class BeritaPipeline(object):
    def process_item(self, item, spider):


        if len(item.get('isi_artikel'))<10:
            spider.dropped_count = + 1
            raise  DropItem("Missing isi_artikel %s" % item)
        if isJS(item['isi_artikel']):
            spider.dropped_count = + 1
            raise  DropItem("artikel adalah kode javaScript %s" % item)
        

        #insert berita
        id_berita = insert_berita(item)
        #if any duplicate items
        if id_berita==0:
            spider.dropped_count = + 1
            print("duplicate news!")
            raise  DropItem("artikel duplikat %s" % item)
        
        #doing ner modeling
        print('proses ner...')
        proses_ner(item,id_berita)

        return item