
import spacy 


def ner_modeling(konten):
  
  per = spacy.load('Person')
  pos = spacy.load('Position')
  org = spacy.load('Organization')
  loc = spacy.load('Location')
  ind = spacy.load('Indicator')
  qot = spacy.load('Quote')


  doc1 = per(konten)
  doc2 = pos(konten)
  doc3 = org(konten)
  doc4 = loc(konten)
  doc5 = ind(konten)
  doc6 = qot(konten)
  
  # mengambil teks hasil prediksi dari label
  person_temp = [(e.text) for e in doc1.ents if e.label_ == 'person']
  position_temp = [(e.text) for e in doc2.ents if e.label_ == 'position']
  organization_temp = [(e.text) for e in doc3.ents if e.label_ == 'organization']
  location_temp = [(e.text) for e in doc4.ents if e.label_ == 'location']
  indicator_temp = [(e.text) for e in doc5.ents if e.label_ == 'indicator']
  quote_temp = [(e.text) for e in doc6.ents if e.label_ == 'quote']
 
  # memasukkkan hasil prediksi kedalam list
  person=[]
  position=[]
  organization=[]
  location=[]
  indicator=[]
  quote=[]

  
  for row in person_temp:
    if row not in person:
      person.append(row)
  for row in position_temp:
    if row not in position:
      position.append(row)
  for row in organization_temp:
    if row not in organization:
      organization.append(row)
  for row in location_temp:
    if row not in location:
      location.append(row)
  for row in indicator_temp:
    if row not in indicator:
      indicator.append(row)
  for row in quote_temp:
    if row not in quote:
      quote.append(row)
  
  # konversi list to str
  ner_raw = [person,position,organization,indicator,location,quote]
  ner_list = [str(row) for row in ner_raw]
  


  return ner_list
def kata2list(kata):
  kata = ganti("[\[\]\']","",kata)
  kata = ganti('"',"",kata)
  kata_v = []
  kata_s = kata.strip().split(",")
  for x in range(len(kata_s)):
    kbx = kata_s[x].strip()
    kata_v.append(kbx)
  
  return kata_v

def get_summary(ner_list,jenis,tanggal):
  """
  ini merupakan fungsi untuk membuat dict berisi summary dari sebuah list hasil NER
  ner_list = iterable / list
  return list
  """

  org = []
  a = 0
  #ner_list = ner_list.apply(lambda x : len(str("x"+ x))>2)
  for i in ner_list:
    i = kata2list(i)
    #i = ast.literal_eval(i)
    a = a + 1
    for x in i:
      
      if len(x)<2:
        continue
      org.append(x)
    
  org = dict(sorted(Counter(org).items(), key=operator.itemgetter(1),reverse=True))
  nama = pd.Series(pd.Series(org)[0:50].index)
  nilai = pd.Series(pd.Series(org)[0:50].values)
  df = pd.concat([nama,nilai],axis=1)
  
  df.columns = ['nama_ner','jumlah']
  df['jenis'] = jenis
  df['tanggal'] = tanggal
  df = df[['tanggal','jenis','nama_ner','jumlah']]
  return df
