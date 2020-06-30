# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from  berita import NER_processing 
from berita.sentimen import sentiment
import re
import Database_connection.Database_connection as db

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
def update_beritasum(item,indikator,id_indikator):
    """
    item : item hasil scraping
    indikator : string indikator
    id_indikator : string id indikator
    """
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
        print(ex)
    database.tutup()

    #insert summary berita by indikator
    qind = """
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
    param = ('%'+id_indikator+'%',)
    database = db()
    try:
        database.kursor.execute(qind,param)
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
    #preparing insert 
    querysent = """
    insert into sentimen 
    values(%s,%s,%s,%s,%s)
    """
    #parameter sentimen isi
    par_isi = (id_berita,id_indikator,indikator,hasil_sentimen['sentimen_isi'],'isi')
    #parameter sentimen kutipan
    par_kutipan = (id_berita,id_indikator,indikator,hasil_sentimen['kutipan'],'kutipan')
    #prepare  database connection
    database = db()
    #execute 
    try:
        database.kursor.execute(querysent,par)
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
        database.kursor.execute(querysent,par2)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def simpan_ner(ner_result,id_berita):
    query_ner = """
    INSERT INTO ner_output (id_berita,indikator,tokoh,organisasi,posisi,lokasi,kutipan) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """ 
    parameter = (
        id_berita,
        ner_result[3],
        ner_result[0],
        ner_result[1],
        ner_result[2],
        ner_result[4],
        ner_result[5])
    
    database = db()
    try:
        database.kursor.execute(query_ner,parameter)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def proses_ner(item,id_berita):
    ner_result = NER_processing.ner_modeling(item['isi_artikel'])
    
    #ubah hasil NER kategori NER indikator menjadi id_indikator dan indikator 
    id_indikator = NER_processing.filter_indikator(ner_result[3])[1]
    indikator = NER_processing.filter_indikator(ner_result[3])[0]
    if len(id_indikator)>4:
        print("update_beritasum...")
        update_beritasum(item,indikator)
        print("simpan_ner...")
        simpan_ner(ner_result,id_berita)
        kutipan = ' '.join(kata2list(ner_result[5]))
        konten = item['isi_artikel']
        print("proses_sentimen...")
        proses_sentimen(id_berita,id_indikator,indikator,konten,kutipan)
        
    return kelas

def insert_berita(item):
    query = """INSERT INTO berita (judul,waktu,tag,isi,sumber) 
        VALUES (%s, %s, %s, %s,%s,%s,%s)
        """
    params = (
        item['judul'],
        item['tanggal'],
        item['tag'],
        item['isi_artikel'],
        item['sumber'],
        )
    # debug
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
            raise  DropItem("Missing isi_artikel %s" % item)
        if isJS(item['isi_artikel']):
            raise  DropItem("artikel adalah kode javaScript %s" % item)
        #doing ner modeling
        print('insert berita...')
        #insert berita
        id_berita = insert_berita(item)
        if id_berita==0:
            return 0
        print('proses ner...')
        kelas = proses_ner(item,id_berita)

        return item
