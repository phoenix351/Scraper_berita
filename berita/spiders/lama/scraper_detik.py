

import scrapy
try:
    from urllib.parse import urljoin
except ImportError:
     from urlparse import urljoin
from re import search
from berita.items import BeritaItem
from datetime import  date

class Detik_scraper(scrapy.Spider):
    name = "detik_spider"
    tanggal = date.today().strftime("%m/%d/%Y")
    start_urls = [('https://news.detik.com/indeks?date='+tanggal)]
    ihal = 2
    @staticmethod
    def clean(s):
      ax = ""
      for a in s.split(" "):
        try :
          ax = ax + " " + search(r'\w+', a).group() 
        except AttributeError:
          continue
      return ax  
    def parse(self,response):
      konten_selektor = 'article.list-content__item'
      sd = 'a.pagination__item ::text'
      maks = int(response.css(sd)[-2].extract())
      
      for konten in response.css(konten_selektor):
        link_selector = 'h3.media__title a ::attr(href)'
        link = konten.css(link_selector).extract_first()
        print(link)
        url = urljoin(response.url, link)
        yield scrapy.Request(url, callback=self.parse_artikel)
      
      while self.ihal <= maks :
        next_page = 'https://news.detik.com/indeks/'+str(self.ihal)+'?date='+self.tanggal
        self.ihal = self.ihal + 1
        request = scrapy.Request(url=next_page)
        yield request
        
    def parse_artikel(self,response):
      
      penulis_selector = 'div.detail__author ::text'
      judul_selector = 'h1.detail__title ::text'
      tanggal_selector = 'div.detail__date ::text'
      isi_selector = 'div.detail__body-text ::text'
      penulis = ' '.join(response.css(penulis_selector).getall())
      judul = ' '.join(response.css(judul_selector).getall())
      tanggal = response.css(tanggal_selector).extract_first()
      isi = ' '.join(response.css(isi_selector).getall())
      penulis = self.clean(penulis)
      judul = self.clean(judul)
      isi = self.clean(isi)

      berita = BeritaItem()
      berita['judul'] = judul
      berita['penulis'] = penulis
      berita['isi_artikel'] = isi
      berita['tanggal'] = tanggal

      yield berita

