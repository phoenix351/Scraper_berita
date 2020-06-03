import scrapy
from re import findall 
from datetime import datetime,timedelta
import sys
from berita.items import BeritaItem
import mysql.connector as MySQLdb
from berita.Database_connection import Database_connection
class Kompas_spider(scrapy.Spider):
    #tanggal = "2020-3-19"
    name = "kompas_spider"
    download_delay = 0.3
    tanggal=''
    
    
    hal = 1
    def __init__(self,tanggal='',*args,**kwargs):
      db = Database_connection()
      self.connection = db.connection
      self.cursor = db.cursor

      super(Kompas_spider, self).__init__(*args, **kwargs)
      
      if len(str(tanggal))<2:
        tanggal=datetime.strftime((datetime.now()-timedelta(1)),'%Y-%m-%d')
      else:
        self.tanggal=tanggal

      
      
      self.start_urls = [('https://indeks.kompas.com/?site=news&date='+tanggal)]

    def parse(self,response):
      konten_selektor = 'div.article__list.clearfix'
      #menghitung jumlah berita di halaman
      jumlah_berita = 0
      for konten in response.css(konten_selektor):
        #crawl on each url 
        link_selector = 'a.article__link ::attr(href)'
        link = konten.css(link_selector).extract_first()+ "?page=all"
        jumlah_berita = jumlah_berita +1
        
        req = scrapy.Request(link, callback=self.parse_artikel)
        yield req
        sys.exit()
        
      
      print("jumlah berita  =",jumlah_berita,"----halaman =",self.hal)
      #find next page if any.
      if jumlah_berita>14:
        self.hal = self.hal+1
        next_page = 'https://indeks.kompas.com/?site=news&date='+self.tanggal+'&page='+str(self.hal)
        req = scrapy.Request(next_page, callback=self.parse)
        yield req
      else:
        print("scraping ---- Selesai Total halaman = ",self.hal)
        print("jumlah berita  =",jumlah_berita,"----halaman =",self.hal)
      
      
      
      
      
    def parse_artikel(self,response):
      
      penulis_selector = 'div#penulis ::text'
      judul_selector = 'h1.read__title ::text'
      waktu_selector = 'div.read__time ::text'
      isi_selector = 'div.read__content p ::text'
      tag_selector = 'a.tag__article__link ::text'
            
      try:
        penulis = response.css(penulis_selector).getall()[-1]
      except:
        penulis="Anonim"
      judul = response.css(judul_selector).get()
      waktu = response.css(waktu_selector).get()
      isi = response.css(isi_selector).getall()
      tag = '[' +','.join(response.css(tag_selector).getall())+']'

      isi_fix = []
      tanda=False
      for kalimat in isi:
        if tanda:
          tanda=False
          continue
        kalimatx= ''.join(findall('[a-z]',kalimat.lower()))
        logikal = kalimatx=='bacajuga'
        if logikal:
          tanda=True
          continue
        isi_fix.append(kalimat)
        
      isi = ' '.join(isi_fix)
      w_re = '\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2}'
      waktu = ''.join(findall(w_re,waktu))
      waktu_ob = datetime.strptime(waktu,'%d/%m/%Y, %H:%M')
      
      # masukkan ke item pipeline
      item = BeritaItem()
      item['tanggal'] = waktu_ob
      item['penulis'] = penulis
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      item['sumber'] = 'Kompas'
      yield item