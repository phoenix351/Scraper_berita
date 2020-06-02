
import scrapy
from re import findall
from datetime import datetime,timedelta
from re import sub
from berita.items import BeritaItem
from berita.Database_connection import Database_connection
import sys
class Detik_scraper(scrapy.Spider):
    name = "detik_spider"
    #tanggal = "12/18/2019"
    tanggal = ''
    start_urls = [('https://news.detik.com/indeks?date='+tanggal)]
    hal = 1
    
    def __init__(self,tanggal='',*args,**kwargs):
      db = Database_connection()
      self.connection = db.connection
      self.cursor = db.cursor

      '''
      self.connection = MySQLdb.connect(
                              host=self.host,
                              user=self.user,
                              passwd=self.password,
                              database=self.db
                          )
      self.cursor = self.connection.cursor()
      '''
      super(Detik_scraper, self).__init__(*args, **kwargs)
      #input = dd-mm-yyyy
      kemarin = datetime.now()-timedelta(1)
      kemarin_string = kemarin.strftime("%m/%d/%Y")

      self.tanggal= kemarin_string
      self.start_urls = [('https://news.detik.com/indeks?date='+self.tanggal)]

    def parse(self,response):
      konten_selektor = 'article.list-content__item'
      jumlah_artikel = 0
      for konten in response.css(konten_selektor):
        link_selector = 'h3.media__title a ::attr(href)'
        url = konten.css(link_selector).extract_first()
        url = url+'?single=1'
        jumlah_artikel = jumlah_artikel+1
        yield scrapy.Request(url, callback=self.parse_artikel)
        sys.exit()
      
      
      if jumlah_artikel> 19 :
        self.hal = self.hal+1
        next_page = 'https://news.detik.com/indeks/'+str(self.hal)+'?date='+self.tanggal
        request = scrapy.Request(url=next_page)
        yield request
      
        
    def parse_artikel(self,response):
      penulis_selector = 'div.detail__author ::text'
      judul_selector = 'h1.detail__title ::text'
      waktu_selector = 'div.detail__date ::text'
      isi_selector = 'div.detail__body-text ::text'
      tag_selector = 'div.detail__body-tag.mgt-16 div a ::text'
      penulis = ' '.join(response.css(penulis_selector).getall())
      judul = response.css(judul_selector).get()
      waktu = response.css(waktu_selector).get()
      

      beda = {
        'Mei':'May',
        'Agu':'Aug',
        'Okt':'Oct',
        'Des':'Dec'
      }
      bulan = ''.join(findall('[a-zA-Z]+',waktu))
      
      try:
        waktu = ''.join(findall('\d{2}\s+[a-zA-Z]+\s+\d{4}\s+\d{2}:\d{2}',waktu))
        waktu = waktu.replace(bulan,beda[bulan])
        waktu = datetime.strptime(waktu,'%d %b %Y %H:%M')
      except:
        waktu = datetime.strptime(self.tanggal,"%m/%d/%Y")
        
      
      isi = ' '.join(response.css(isi_selector).getall())
      css_ = response.css('style ::text').getall()
      js_ = response.css('script ::text').getall()
      iklan = response.css('div.lihatjg ::text').getall()
      for _ in css_:
        isi = isi.replace(_,"")
      for _ in js_:
        isi = isi.replace(_,"")
      for _ in iklan :
        isi = isi.replace(_,"")
      for _ in response.css(tag_selector).getall():
        isi = isi.replace(_,"")
      isi = isi.strip()



      tag = "["+(','.join(response.css(tag_selector).getall()))+"]"
        
        
      item = BeritaItem()
      item['tanggal'] = waktu
      item['penulis'] = penulis
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      item['sumber'] = 'Detik'
      yield item
        
