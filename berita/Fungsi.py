import re

def justAlphaNumSpace(kata):
	alphanumeric = re.compile(r'[^a-zA-Z0-9]')
	space = re.compile(r'\s+')
	kata = space.sub(' ',kata).strip()
	kata = alphanumeric.sub('',kata)
	return kata
def get_listkatakunci():

  database = Database_connection()
  query = '''select k.id_indikator, k.katakunci, r.indikator 
  from katakunci_indikator k, indikator_ref r 
  where r.id_indikator = k.id_indikator
  '''
  list_katakunci = []
  try:
    database.kursor.execute(query)
    result = database.kursor.fetchall()
    for r in result:
      kamus = {
      'id_indikator':r[0],
      'indikator':r[2],
      'katakunci':r[1].lower()}
      list_katakunci.append(kamus)
  except Exception as ex:
    print("gagal melakukan query")
    print(ex)
  database.tutup()
  return list_katakunci


def isBerita(url):
    site_berita = re.compile(r'https\:\/\/[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+\/berita\S*\/')
    logika = bool(site_berita.search(url))
    return logika

def isJS(kalimat):
    a = re.compile(r'var\s*[a-zA-Z_]*\s*=\s*[\S]*;')
    b = re.compile(r'let\s*\S*\s*=\s*[\S]*;*')
    c = re.compile(r'function \S+\(\S*\)\s*\{[\s\s]*\}')
    x = bool(a.search(kalimat))
    y = bool(b.search(kalimat))
    z = bool(c.search(kalimat))
    if x or y or z:
        return True
    else:
        return False
if __name__ == '__main__':
	get_listkatakunci()