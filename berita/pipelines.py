# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from  berita.NER_processing import ner_modeling
from  berita.NER_processing import kata2list
from berita.sentimen import sentiment
import re
from berita.Database_connection import Database_connection
import ast
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from berita.NER_processing import justAlphaNum
from berita.NER_processing import get_listkatakunci
from berita.NER_processing import isJS

Thread = ThreadPoolExecutor(max_workers=20)
Process = ProcessPoolExecutor(max_workers=2)


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
    database = Database_connection()
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
    database = Database_connection()
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
    insert into sum_tags (waktu, tag, jumlah)
    values(%s,%s,1)
    on duplicate key update jumlah = jumlah + 1
    """
    param = (waktu,tag)
    database = Database_connection()
    try:
        database.kursor.execute(query,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        return ex
    database.tutup()
def proses_tags(waktu,tags):
    """
    waktu : string dengan format %Y-%m-%d atau python datetime.datetime
    tags : string representation of list 
    """
    non_alphanumeric = re.compile(r'[^a-zA-Z0-9\s]')
    space = re.compile(r'\s+')
    tags = kata2list(tags)
    ft = []
    for tag in tags:
        #remove non alphanumeric
        tag = non_alphanumeric.sub('',tag)
        #remove unnecesry space / tab
        tag = space.sub(' ',tag).strip()
        #cek valid tag jika lebih dari 3
        if len(tag) > 3:
            #simpan pada sum tag table
            f = Thread.submit(simpan_tag,tag)
            ft.append(f)
    ft = [f.result() for f in ft]
    return ft



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
    database = Database_connection()
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
    database = Database_connection()
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
       str( ner_result['indikator']),
        str(ner_result['tokoh']),
        str(ner_result['organisasi']),
        str(ner_result['posisi']),
        str(ner_result['lokasi']),
        str(ner_result['kutipan'])
        )
    
    database = Database_connection()
    try:
        database.kursor.execute(query_ner,parameter)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        print(ex)
    database.tutup()
def insert_sumner(entitas,indikator,jenis_entitas,jumlah=1):
    query = '''insert into sum_ner (entitas,indikator,jenis_entitas,jumlah)
    values (%s,%s,%s,%s)
    on duplicate key update jumlah = jumlah +1
    '''
    database = Database_connection()
    param = (entitas,indikator,jenis_entitas,1)
    try:
        database.kursor.execute(query,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        return str(ex)
    return True

def simpan_sumner(ner_result,indikator):
    
    full_param = []
    tokoh = [(t,indikator,'tokoh') for t in ner_result['tokoh'] if len(t)>3]
    full_param.extend(tokoh)
    posisi = [(t,indikator,'posisi') for t in ner_result['posisi'] if len(t)>3]
    full_param.extend(posisi)
    organisasi = [(t,indikator,'organisasi') for t in ner_result['organisasi'] if len(t)>3]
    full_param.extend(organisasi)
    lokasi = [(t,indikator,'lokasi') for t in ner_result['lokasi'] if len(t)>3]
    full_param.extend(lokasi)
    fl =[]
    for param in full_param:
        entitas = param[0]
        indikator = param[1]
        jenis_entitas = param[2]
        f = Thread.submit(insert_sumner,entitas,indikator,jenis_entitas)
        fl.append(f)
    fl = [f.result() for f in fl]
    return fl



    

def proses_ner(item,id_berita):
    ner_result = ner_modeling(item['isi_artikel'],id_berita)
    
    #ubah hasil NER kategori NER indikator menjadi id_indikator dan indikator 
    indikator_list = ner_result['indikator']
    for row in indikator_list:
        id_indikator = row['id_indikator']
        id_indikator = justAlphaNum(id_indikator)
        indikator = row['indikator']
        indikator = indikator
        if len(id_indikator) < 3:
            continue

        print("indikator terdeteksi = ",indikator)
        print("update indikator sum...")
        Thread.submit(update_indikatorsum,item,indikator,id_indikator)    
        print("simpan_ner...")
        Thread.submit(simpan_ner,ner_result,id_berita)
        print("simpan summary ner ...")
        simpan = Process.submit(simpan_sumner,ner_result,indikator)
        kutipan = ' '.join(ner_result['kutipan'])
        konten = item['isi_artikel']
        print("proses_sentimen...")
        Process.submit(proses_sentimen,id_berita,id_indikator,indikator,konten,kutipan)
        sr = simpan.result()
        for er in sr:
            print(er)
    
    return True
def insert_sum_sumber(waktu,sumber):
    #insert summary berita by sumber
    qsum = """
    insert into beritasum_sumber (waktu, sumber, jumlah)
    values (%s,%s,1)
    on duplicate key update jumlah = jumlah + 1 
    """
    param = (item['waktu'],item['sumber'])
    database = Database_connection()
    try:
        database.kursor.execute(qsum,param)
        database.koneksi.commit()
    except Exception as ex:
        database.koneksi.rollback()
        return ex
    database.tutup()

def simpan_berita(item):
    
    

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
    database = Database_connection()
    try:
        database.kursor.execute(query, params)
        database.koneksi.commit()
        print(database.kursor.rowcount, "berita berhasil di simpan!")
        id_generated = database.kursor.lastrowid
    except Exception as ex:
        database.koneksi.rollback()
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
        
        id_berita = simpan_berita(item)

        #if any duplicate items
        if id_berita==0:
            spider.dropped_count = + 1
            print("duplicate news!")
            raise  DropItem("artikel duplikat %s" % item)
        
        #insert sum tag
        tagf = Process.submit(proses_tags,item['waktu'],item['tag'])
        
        #insert summary waktu dan sumber
        waktu = item['waktu']
        sumber = item['sumber']
        sumsumber = Thread.submit(insert_sum_sumber,waktu,sumber)

        #ner proses
        print('proses ner...')
        proses_ner(item,id_berita)

        tag_warn = [f.result() for f in tagf]
        tag_warn.append(sumsumber.result())
        for f in tag_warn:
            print(f)
        return item