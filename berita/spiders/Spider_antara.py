
import scrapy
from re import findall 
from datetime import datetime,timedelta
import sys
from berita.NER_processing import isBerita
from berita.items import BeritaItem
from berita.kirim_notif import kirim_notif
class Antara_spider(scrapy.Spider):
    #tanggal = "2020-3-19"
    name = "antara_spider"
    download_delay = 0.3
    tanggal=''
    costum_settings = {
      'LOG_LEVEL':'ERROR'
    }
    url_seen = []
    dropped_count = 0
    total_scraped = 0
    hal = 1
    def __init__(self,tanggal='',*args,**kwargs):
      super(Antara_spider, self).__init__(*args, **kwargs)
      try:
        tanggal = datetime.strptime(tanggal,"%Y-%m-%d")
        self.tanggal=datetime.strftime(tanggal,'%d-%m-%Y')
      except:
        kemarin = (datetime.now()+timedelta(hours=7) - timedelta(1))
        self.tanggal=datetime.strftime(kemarin,'%d-%m-%Y')      
      
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
        self.total_scraped += 1
        if (link in self.url_seen):
          sys.exit()
        if (not isBerita(link)):
          jumlah_berita = jumlah_berita +1
          continue

        jumlah_berita = jumlah_berita +1
        
        req = scrapy.Request(link, callback=self.parse_artikel)
        self.url_seen.append(link)
        yield req
        
     
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
        try :
          rasio = self.total_scraped//self.dropped_count
          if rasio < 2:
            kirim_notif(self.name)
        except:
          pass
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

      try:
        waktu = ''.join(findall('\d+\s+[a-zA-Z]+\s+\d{4}',waktu))
        bulan = ''.join(findall('[a-zA-Z]+',waktu))
        waktu = waktu.replace(bulan,beda[bulan])
        waktu = datetime.strptime(waktu,'%d %B %Y')
      except:
        waktu = datetime.strptime(self.tanggal,r'%d-%m-%Y')

      
      # masukkan ke item pipeline
      item = BeritaItem()
      item['waktu'] = waktu
      item['sumber'] = 'Antara'
      item['judul'] = judul
      item['isi_artikel'] = isi
      item['tag']=tag
      yield item