import scrapy
from re import findall
from datetime import datetime,timedelta
from berita.items import BeritaItem
import sys
from berita.NER_processing import isBerita
from berita.kirim_notif import kirim_notif
class Republik_spider(scrapy.Spider):
  name = "repu_spider"
  tanggal=''
  i = 1
  download_delay = 0.3
  costum_settings = {
      'LOG_LEVEL':'DEBUG'
    }
  dropped_count = 0 
  hal = 1
  total_scrapped = 0  
  def __init__(self,tanggal='',*args,**kwargs):
    super(Republik_spider, self).__init__(*args, **kwargs)
   
    try:
      tanggal = datetime.strptime(tanggal,r'%Y-%m-%d')
      tanggal = tanggal.strftime(tanggal,r"%Y/%m/%d")
      self.tanggal = tanggal      
    except:
      tanggal = datetime.now() + timedelta(hours=7) - timedelta(1)
      self.tanggal=tanggal.strftime(r"%Y/%m/%d")      
    
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
      self.total_scrapped += 1
      if  (not isBerita(url)):
        jumlah_berita = jumlah_berita+1
        continue
      jumlah_berita = jumlah_berita+1
      req = scrapy.Request(url, callback=self.parse_artikel) 
      #yield request
      yield req
      

    #go to next page

    
    if jumlah_berita>=39:
      np_sel = 'div.pagination section nav a::attr(href)'
      next_page = response.css(np_sel).getall()[-1]
      req = scrapy.Request(next_page,callback=self.parse)
      self.i = i +1
      yield  req
    else:
      try:
        rasio = self.total_scraped//self.dropped_count
        if rasio < 2:
          kirim_notif(self.name)
      except:
        pass
      sys.exit("scraping Republika - selesai")


    

  def parse_artikel(self,response):

    konten_selektor = '.wrap_detail'
    for konten in response.css(konten_selektor):
      #selector

      judul_selector = 'div.wrap_detail_set  h1::text'
      waktu_selector = '.date_detail ::text'
      isi_selector = '.artikel p ::text'
      tag_selector = 'div.wrap_blok_tag li h1 a::text'

      #get text
    
      judul = konten.css(judul_selector).get()
      waktu = konten.css(waktu_selector).get()
      try:
        waktu = ''.join(findall('\d{2}\s[a-zA-z]+\s\d{4}\s+\d{2}:\d{2}',waktu))
        waktu = datetime.strptime(waktu,'%d %b %Y  %H:%M')
      except:
        waktu = datetime.strptime(self.tanggal,r'%Y/%m/%d')

      isi = konten.css(isi_selector).getall()
      tag = konten.css(tag_selector).getall()
      

      isi = ' '.join(isi)
      tag = '['+','.join(tag)+']'
     
      # masukkan ke item pipeline
      item = BeritaItem()
      item['waktu'] = waktu
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      item['sumber']='Republika'
      yield item
      
      