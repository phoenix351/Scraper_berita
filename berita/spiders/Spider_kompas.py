import scrapy
from re import findall 
from datetime import datetime,timedelta
import sys
from berita.items import BeritaItem
from berita.kirim_notif import kirim_notif

class Kompas_spider(scrapy.Spider):
    #tanggal = "2020-3-19"
    name = "kompas_spider"
    download_delay = 0.3
    tanggal=''
    total_scraped = 0
    dropped_count = 0
    hal = 1
    def __init__(self,tanggal='',*args,**kwargs):
      
      super(Kompas_spider, self).__init__(*args, **kwargs)
      
      try:
        self.tanggal=datetime.strftime((datetime.now()-timedelta(1)),'%Y-%m-%d')
      except:
        self.tanggal=datetime.strptime(tanggal,'%d-%m-%Y')
        self.tanggal = datetime.strftime(self.tanggal,'%Y-%m-%d')

      
      
      self.start_urls = [('https://indeks.kompas.com/?site=news&date='+self.tanggal)]

    def parse(self,response):
      konten_selektor = 'div.article__list.clearfix'
      #menghitung jumlah berita di halaman
      jumlah_berita = 0
      for konten in response.css(konten_selektor):
        #crawl on each url 
        link_selector = 'a.article__link ::attr(href)'
        link = konten.css(link_selector).extract_first()+ "?page=all"
        self.total_scraped += 1
        jumlah_berita = jumlah_berita + 1
        
        req = scrapy.Request(link, callback=self.parse_artikel)
        yield req
                
      
      print("jumlah berita  =",jumlah_berita,"----halaman =",self.hal)
      #find next page if any.
      if jumlah_berita>14:
        self.hal = self.hal+1
        next_page = 'https://indeks.kompas.com/?site=news&date='+self.tanggal+'&page='+str(self.hal)
        req = scrapy.Request(next_page, callback=self.parse)
        yield req
      else:
        if self.total_scraped//self.dropped_count <2:
          kirim_notif()
        print("scraping ---- Selesai Total halaman = ",self.hal)
        print("jumlah berita  =",jumlah_berita,"----halaman =",self.hal)
      
      
      
      
      
    def parse_artikel(self,response):
      
      judul_selector = 'h1.read__title ::text'
      waktu_selector = 'div.read__time ::text'
      isi_selector = 'div.read__content p ::text'
      tag_selector = 'a.tag__article__link ::text'
            
     
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
      item['waktu'] = waktu_ob
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      item['sumber'] = 'Kompas'
      yield item