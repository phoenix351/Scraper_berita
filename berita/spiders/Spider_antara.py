# isi file scraper kompas

# -*- coding: utf-8 -*-
"""scraper_kompas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10b2Q7XpYpERjQzDlWI1XhTda5LVYUbPU
"""

import scrapy
from re import findall 
from datetime import datetime,timedelta
import sys
from berita.pipelines import isBerita
from berita.items import BeritaItem
class Antara_spider(scrapy.Spider):
    #tanggal = "2020-3-19"
    name = "antara_spider"
    download_delay = 0.3
    tanggal=''
    costum_settings = {
      'LOG_LEVEL':'ERROR'
    }
    url_seen = []
    
    hal = 0
    def __init__(self,tanggal='',*args,**kwargs):
      super(Antara_spider, self).__init__(*args, **kwargs)
      if len(str(tanggal))<2:
        kemarin = (datetime.now() - timedelta(1))
        self.tanggal=datetime.strftime(kemarin,'%d-%m-%Y')
      else:
        tanggal = datetime.strptime(tanggal,"%d-%m-%Y")
        self.tanggal=datetime.strftime(tanggal,'%d-%m-%Y')

      
      
      self.start_urls = [(
        'https://www.antaranews.com/indeks/'+
        self.tanggal+
        '/1')]

    def parse(self,response):
      konten_selektor = 'article.simple-post'
      #menghitung jumlah berita di halaman
      jumlah_berita = 0
      for konten in response.css(konten_selektor):
        #crawl on each url 
        link_selector = 'a ::attr(href)'
        link = konten.css(link_selector).extract_first()
        if (link in self.url_seen):
          sys.exit()
        if (not isBerita(link)):
          continue

        jumlah_berita = jumlah_berita +1
        
        req = scrapy.Request(link, callback=self.parse_artikel)
        self.url_seen.append(link)
        yield req
        sys.exit()
     
      #find next page if any.
      if jumlah_berita>9:
        self.hal = self.hal+1
        next_page = (
          'https://www.antaranews.com/indeks/'+
          self.tanggal+
          '/'+str(self.hal))
        req = scrapy.Request(next_page, callback=self.parse)
        yield req
      else:
        print("scraping ---- Selesai Total halaman = ",self.hal)
        print("jumlah berita  =",jumlah_berita,"----halaman =",self.hal)
      
      
      
      
      
    def parse_artikel(self,response):
      
      
      judul_selector = '.post-title ::text'
      waktu_selector = 'header.post-header .article-date ::text'
      isi_selector = '.post-content ::text'
      tag_selector = '.tags-wrapper li a ::text'
      
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

      waktu = ''.join(findall('\d+\s+[a-zA-Z]+\s+\d{4}',waktu))

      beda = {
        'Januari':'January',
        'Februari':'February',
        'Maret':'March',
        'Mei':'May',
        'Juni':'June',
        'Juli':'July',
        'Agustus':'August',
        'Oktober':'October',
        'Desember':'December'
      }
      bulan = ''.join(findall('[a-zA-Z]+',waktu))
      
      try:
        waktu = waktu.replace(bulan,beda[bulan])
      except:
        print('already same')
      
      waktu = datetime.strptime(waktu,'%d %B %Y')


      
      # masukkan ke item pipeline
      item = BeritaItem()
      item['tanggal'] = waktu
      item['sumber'] = 'Antara'
      item['judul'] = judul
      item['isi'] = isi
      item['tag']=tag
      yield item