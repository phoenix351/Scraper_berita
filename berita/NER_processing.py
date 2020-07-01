
import spacy 
import os
path_file = os.path.dirname(os.path.abspath(__file__))
import re
from concurrent.futures import ProcessPoolExecutor
from berita.Database_connection import Database_connection
from berita.fungsi import justAlphaNum
from berita.fungsi import get_listkatakunci


def kata_Indikator(kata):
  list_katakunci = get_listkatakunci()
  kata = str(kata).lower()
  if len(kata) < 3 :
    return 0
  for indikator_kamus in list_katakunci:
    if kata in indikator_kamus['katakunci']:
      id_indikator = indikator_kamus['id_indikator']
      indikator = indikator_kamus['indikator']
      ind_dict = {'id_indikator':id_indikator,'indikator':indikator}
      return ind_dict
    continue
  return 0


def ner_fun(konten):
  os.chdir(path_file+'/../ner_model')
  semua =  spacy.load('All')
  hasil = semua(konten)
  return hasil

def ner_modeling(konten,id_berita):


  #doc5 = ner_fun(konten,'indikator')
  semua = ner_fun(konten)
  doc5 = semua
  ner_tokoh = semua
  ner_posisi = semua
  ner_organisasi = semua
  ner_lokasi = semua
  ner_kutipan = semua


  indicator = list(set([(e.text) for e in doc5.ents if e.label_ == 'indicator']))
  list_indikator = []
  for ind in indicator:
    filtered = kata_Indikator(ind)
    if filtered != 0:
      list_indikator.append(filtered)

  if len(list_indikator)>=1:

  
    # mengambil teks hasil prediksi dari label
    #ner_tokoh = ner_tokoh.result()
    tokoh = [justAlphaNum(e) for e in list(set([(e.text) for e in ner_tokoh.ents if e.label_ == 'person']))]

    #ner_posisi = ner_posisi.result()
    posisi = [justAlphaNum(e) for e in list(set([(e.text) for e in ner_posisi.ents if e.label_ == 'position']))]

    #ner_organisasi = ner_organisasi.result()
    organisasi = [justAlphaNum(e) for e in list(set([(e.text) for e in ner_organisasi.ents if e.label_ == 'organization']))]

    #ner_lokasi = ner_lokasi.result()
    lokasi = [justAlphaNum(e) for e in list(set([(e.text) for e in ner_lokasi.ents if e.label_ == 'location']))]
    
    #ner_kutipan = ner_kutipan.result()
    kutipan = [justAlphaNum(e) for e in list(set([(e.text) for e in ner_kutipan.ents if e.label_ == 'quote']))]
  else:
    tokoh = []
    posisi = []
    organisasi = []
    lokasi = []
    kutipan = []
   
  # memasukkkan hasil prediksi kedalam list
  
  ner_dict = {
    'tokoh':tokoh,
    'posisi':posisi,
    'organisasi':organisasi,
    'lokasi':lokasi,
    'indikator':list_indikator,
    'kutipan':kutipan
  }
  
  return ner_dict
def kata2list(kata):
  kata = re.sub("[\[\]\']","",kata)
  kata = re.sub('"',"",kata)
  kata_v = []
  kata_s = kata.strip().split(",")
  for x in range(len(kata_s)):
    kbx = kata_s[x].strip()
    kata_v.append(kbx)
  
  return kata_v