import time
import subprocess
from datetime import datetime,timedelta
import os
path_file = os.path.dirname(os.path.abspath(__file__))
os.chdir(path_file+"/../")

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
    bash = "scrapy runspider "+nama+" -a tanggal="+tanggal+" > "+nama_log
    bash_list.append(bash)
    bashx = bash.split()
    try:
      proses = subprocess.run(bashx,shell=True, check=True)
      #subprocess.check_output(bash, shell=True)
      print(proses.returncode)
    except Exception as e:
      output = e
      print(output)
  

def buatlist_tanggal(dari):
  base = datetime.strptime(dari,'%d-%m-%Y')
  end = datetime.now() - timedelta(hours=17)
  numdays = abs((base-end).days)+1
  date_list = [datetime.strftime((end - timedelta(days=x)),'%Y-%m-%d') for x in range(numdays)]
  return date_list
def main():
  list_batch = buatlist_tanggal('08-06-2020')  
  
  for t in list_batch:

    print('sekarang scraping tanggal =',t)
    skrep(t)
if __name__ == '__main__':
  main()