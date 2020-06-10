import scrapy
from re import findall
from datetime import datetime,timedelta
from berita.items import BeritaItem
import mysql.connector as MySQLdb
import sys
  
class Republik_spider(scrapy.Spider):
  name = "repu_spider"
  tanggal=''
  i = 1
  download_delay = 0.3
  costum_settings = {
      'LOG_LEVEL':'DEBUG'
    }
 
  
  host = 'localhost'
  user = 'root'
  password = ''
  db = 'phoenix'
    
  hal = 1
    
  def __init__(self,tanggal='',*args,**kwargs):
    super(Republik_spider, self).__init__(*args, **kwargs)
    db = Database_connection()
    self.connection = db.connection
    self.cursor = db.cursor
    
    if len(tanggal)<2:
      tanggal = datetime.now()-timedelta(1)
      self.tanggal=tanggal.strftime("%Y/%m/%d")
    else:
      tanggal = datetime.strptime(tanggal,'%d-%m-%Y')
      tanggal = tanggal.strftime(tanggal,"%Y/%m/%d")
      self.tanggal = tanggal
    
    self.start_urls = [('https://republika.co.id/index/'+self.tanggal)]
    
  def parse(self,response):
    #print('========',self.start_urls)
    berita_selector ="div.txt_subkanal.txt_index h2 a::attr(href)"
    i = self.i
    #jumlah berita untuk mengecek halaman apakah masih bisa di scrape
    jumlah_berita = 0

    for baris in response.css(berita_selector):
      # crawl each url in particular page
      url = baris.getall()[0]
      jumlah_berita = jumlah_berita+1
      req = scrapy.Request(url, callback=self.parse_artikel) 
      #yield request
      yield req
      

    #go to next page

    
    if jumlah_berita>=40:
      np_sel = 'div.pagination section nav a::attr(href)'
      next_page = response.css(np_sel).getall()[-1]
      req = scrapy.Request(next_page,callback=self.parse)
      self.i = i +1
      yield  req
    else:
      sys.exit("scraping Republika - selesai")


    

  def parse_artikel(self,response):

    konten_selektor = '.wrap_detail'
    for konten in response.css(konten_selektor):
      #selector
      penulis_selector = '.by ::text'
      judul_selector = 'div.wrap_detail_set  h1::text'
      waktu_selector = '.date_detail ::text'
      isi_selector = '.artikel p ::text'
      tag_selector = 'div.wrap_blok_tag li h1 a::text'

      #get text
      penulis = konten.css(penulis_selector).getall()
      judul = konten.css(judul_selector).get()
      waktu = konten.css(waktu_selector).get()
      waktu = ''.join(findall('\d{2}\s[a-zA-z]+\s\d{4}\s+\d{2}:\d{2}',waktu))
      waktu = datetime.strptime(waktu,'%d %b %Y  %H:%M')

      isi = konten.css(isi_selector).getall()
      tag = konten.css(tag_selector).getall()
      
      # just make form with scrapy Field format 
      penulis = ' '.join(penulis)
      penulis = ''.join(findall('\s[a-zA-Z]+\s\S+',penulis))

      
      isi = ' '.join(isi)
      tag = '['+','.join(tag)+']'
     
      # masukkan ke item pipeline
      item = BeritaItem()
      item['tanggal'] = waktu
      item['penulis'] = penulis
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      item['sumber']='Republika'
      yield item
      
      