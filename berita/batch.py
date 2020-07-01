import time
import subprocess
from datetime import datetime,timedelta
import os
os.chdir("../")

def skrep(tanggal):
  #tanggal_ = tanggal.replace("/","-")
  nama_py = ["berita/spiders/Spider_antara.py",
  "berita/spiders/Spider_bisnis.py",
  "berita/spiders/Spider_detik.py",
  "berita/spiders/Spider_kompas.py",
  "berita/spiders/Spider_okezone.py",
  "berita/spiders/Spider_republika.py"]
  bash_list = []
  log_list = ['antara','bisnis','detik','kompas','okezone','republika']
  i = 0
  for nama in nama_py:
    nama_log = log_list[i]+tanggal+".log"
    bash = "scrapy runspider "+nama_py+" -a tanggal="+tanggal+" > "+nama_log
    bash_list.append(bash)
    try:
      subprocess.check_output(bsh, shell=True)
    except subprocess.CalledProcessError as e:
      output = e.output
  return output

def buatlist_tanggal(dari):
  base = datetime.strptime(dari,'%d-%m-%Y')
  end = datetime.now() - timedelta(hours=17)
  numdays = abs((base-end).days)+1
  date_list = [datetime.strftime((end - timedelta(days=x)),'%Y-%m-%d') for x in range(numdays)]
  return date_list
def main():
  list_batch = buatlist_tanggal('08-06-2020')  
  print(list_batch)
  for t in list_2020:
    print('sekarang scraping tanggal =',t)
    skrep(t)
if __name__ == '__main__':
  main()