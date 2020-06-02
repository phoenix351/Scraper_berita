from NER_processing import get_summary
import mysql.connector as MySQLdb
from Database_connection import Database_connection
from datetime import datetime,timedelta
import ast
import sys
import numpy as np
sub_indikator = np.array([['0', '0', '0', '1', '1', '1', '1', '2', '2', '3', '3', '3', '3',
        '3', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '5',
        '5', '5', '5', '6', '6', '6', '7', '7', '7', '7', '8', '8', '9',
        '10', '10', '11', '11', '12', '12', '12', '13', '13', '13', '14',
        '14', '15', '15', '15', '16', '16', '16', '17', '17', '17', '18',
        '18', '18', '19', '19', '19', '19', '19', '19', '20', '20', '20',
        '21', '21', '21', '22', '22', '22', '22', '22', '22', '22', '22',
        '22', '22', '22', '23', '23', '23', '23', '24', '24', '24', '25',
        '26', '26', '26', '27', '27', '27', '28', '28', '28', '28', '28',
        '28', '28', '28', '29', '29', '29', '29', '29', '29', '29', '29',
        '29', '29', '29', '29', '29', '29', '30', '30', '30', '30', '31',
        '32', '32', '32', '32', '33', '33', '34', '34', '35', '35', '36',
        '36', '36', '36', '36', '36', '36', '36', '36', '37', '37', '37',
        '38', '39', '39', '39', '39', '39', '39', '40', '40', '40', '40',
        '41', '41', '41', '41', '42', '42', '42', '42', '42', '43', '43',
        '44', '44', '45', '45', '46', '47', '48', '48', '48', '48', '48',
        '48', '48', '48', '48', '49', '49', '50', '50', '50', '51', '51',
        '51', '52', '52', '52', '53', '53', '53', '54', '54', '55', '56',
        '57', '58', '58', '58', '59', '59', '59', '60', '61', '62', '63',
        '64', '64', '64', '64', '65', '66', '66', '66', '67', '67', '67',
        '68', '68', '69', '69', '70', '70', '71', '71', '72', '72', '73',
        '73', '74', '74', '75', '76', '76', '76', '77', '78', '78', '79',
        '79', '80', '80', '80', '81', '81', '81', '81', '82', '82', '82',
        '83', '83', '83', '84', '84', '84', '85', '85', '85', '86', '86',
        '86', '87', '87', '88', '88', '89', '89', '89', '89', '90', '90',
        '90', '90', '91', '92', '92', '92', '93', '94', '95', '96', '97',
        '98', '98', '98', '99', '99', '100', '100', '100', '101', '101',
        '102', '102', '103', '103', '103', '104', '104', '105', '105',
        '106', '106', '107', '107', '108', '108', '109', '109', '109',
        '109', '109', '109', '109', '109', '109', '109', '109', '110',
        '110', '110', '110', '110', '111', '111', '112', '112', '113',
        '113', '113'],
       ['ekspor', 'impor', 'neraca perdagangan',
        'indeks tendensi konsumen (itk)', 'indeks tendensi konsumen',
        'itk', 'tendensi konsumen',
        'ketimpangan pendapatan (ukuran bank dunia)',
        'ketimpangan bank dunia', 'koefisien gini', 'gini ratio',
        'rasio gini', 'tingkat ketimpangan pendapatan',
        'ketimpangan pendapatan', 'ketimpangan', 'angkatan kerja',
        'pengangguran', 'penganggur', 'penduduk usia kerja',
        'jumlah penduduk yang bekerja', 'jumlah penduduk bekerja',
        'jumlah pengangguran', 'jumlah angkatan kerja',
        'jumlah penduduk angkatan kerja',
        'jumlah penduduk bukan angkatan kerja',
        'angka setengah pengangguran', 'setengah penganggur',
        'setengah pengangguran', 'pekerja setengah penganggur',
        'tingkat partisipasi angkatan kerja (tpak)',
        'tingkat partisipasi angkatan kerja', 'tpak',
        'tingkat pengangguran terbuka (tpt)',
        'tingkat pengangguran terbuka', 'tpt', 'tingkat pengangguran',
        'tingkat kesempatan kerja', 'kesempatan kerja',
        'rasio ketergantungan', 'rata-rata upah harian buruh bangunan',
        'upah nomial harian buruh bangunan',
        'rata-rata upah harian buruh tani',
        'upah nominal harian buruh tani', 'indeks indikator kini (iik)',
        'indeks indikator kini', 'iik',
        'indeks pembangunan manusia (ipm)', 'indeks pembangunan manusia',
        'ipm',
        'rata-rata pengeluaran perkapita riil yang disesuaikan (daya beli)',
        'daya beli masyarakat', 'indeks pembangunan gender (ipg)',
        'indeks pembangunan gender', 'ipg',
        'indeks pemberdayaan gender (idg)', 'indeks pemberdayaan gender',
        'idg', 'potensi desa (podes)', 'podes', '',
        'indeks indikator mendatang (iim)', 'indeks indikator mendatang',
        'iim', 'nilai tukar petani (ntp)', 'nilai tukar petani', 'ntp',
        'nilai tukar usaha rumah tangga pertanian (ntup)',
        'nilai tukar usaha rumah tangga pertanian', 'ntup',
        'indeks harga yang diterima petani (it)',
        'indeks harga yang diterima petani', 'it',
        'indeks harga yang dibayar petani (ib)',
        'indeks harga yang dibayar petani', 'ib',
        'rata-rata harga gabah', 'harga gabah',
        'rata-rata harga gabah kering giling (gkg)',
        'harga gabah kering giling', 'harga gkg',
        'rata-rata harga gabah kering panen (gkp)',
        'harga gabah kering panen', 'harga gkp',
        'rata-rata harga gabah kualitas rendah (gkr)',
        'harga gabah kualitas rendah', 'harga gkr',
        'rata-rata lama menginap tamu (asing dan dalam negeri)',
        'rata-rata lama menginap tamu asing',
        'rata-rata lama menginap tamu indonesia',
        'rata-rata lama menginap tamu',
        'rata-rata lama tinggal wisatawan mancanegara',
        'rata-rata lama tinggal wisman',
        'rata-rata lama tinggal wisatawan',
        'rata-rata pengeluaran per wisman per hari per kunjungan',
        'indeks harga perdagangan besar (ihpb)',
        'indeks harga perdagangan besar', 'ihpb',
        'tingkat penghunian kamar (tpk)', 'tingkat penghunian kamar',
        'tpk', 'penerimaan dari wisatawan mancanegara',
        'penerimaan dari wisman',
        'jumlah kunjungan wisatawan mancanegara',
        'jumlah kunjungan wisman', 'kunjungan wisatawan mancanegara',
        'kunjungan wisman', 'jumlah wisatawan mancanegara',
        'jumlah wisman', 'produk domestik bruto (pdb)',
        'produk domestik regional bruto (pdrb)', 'produk domestik bruto',
        'produk domestik regional bruto', 'pdb', 'pdrb',
        'pdb atas dasar harga berlaku', 'pdb atas dasar harga konstan',
        'pdb adhb', 'pdb adhk', 'pdrb atas dasar harga berlaku',
        'pdrb atas dasar harga konstan', 'pdrb adhb', 'pdrb adhk',
        'laju pertumbuhan pdb', 'laju pertumbuhan pdrb',
        'pertumbuhan ekonomi', 'laju pertumbuhan ekonomi',
        'indeks implisit', 'distribusi persentase pdb',
        'distribusi persentase pdrb', 'distribusi pdb',
        'distribusi pdrb', 'pdb per kapita', 'pdrb per kapita',
        'rasio modal-output marginal', 'icor',
        'rasio tenaga kerja-output marginal', 'ilor',
        'pertumbuhan produksi industri pengolahan',
        'pertumbuhan produksi industri', 'ppi',
        'industri kecil menengah (ikm)', 'industri kecil menengah',
        'ikm', 'industri besar sedang (ibs)', 'industri besar sedang',
        'ibs', 'indeks harga konsumen (ihk)', 'indeks harga konsumen',
        'ihk', 'indeks produksi industri pengolahan',
        'rasio penumpang per pesawat udara', 'rppu',
        'penumpang per pesawat', 'jumlah penumpang angkutan udara',
        'pengguna angkutan udara', 'jumlah pengguna angkutan udara',
        'rasio barang per pesawat udara', 'rbpu',
        'jumlah barang yang diangkut', 'rasio jumlah barang per pesawat',
        'rasio penumpang per kapal', 'rpk',
        'jumlah penumpang angkutan laut', 'penumpang angkutan laut',
        'rasio barang per kapal', 'rbk. jumlah barang yang dibongkar',
        'jumlah barang yang dimuat', 'jumlah barang yang diangkut naik',
        'jumlah barang yang diangkut turun',
        'rasio penduduk terhadap mobil penumpang', 'rpmp',
        'rasio penduduk terhadap kendaraan bermotor', 'rpkb',
        'rasio penduduk terhadap bus umum', 'rpbu',
        'jumlah kendaraan bermotor', 'panjang jalan', 'inflasi',
        'deflasi', 'laju inflasi', 'inflasi bulanan', 'inflasi tahunan',
        'inflasi tahun kalender', 'inflasi inti',
        'inflasi volatile food', 'inflasi administered prices',
        'rasio kendaraan bermotor terhadap panjang jalan', 'rkbpj',
        'angka melek huruf (amh)', 'angka melek huruf', 'amh',
        'angka partisipasi kasar (apk)', 'angka partisipasi kasar',
        'apk', 'angka partisipasi murni (apm)',
        'angka partisipasi murni', 'apm',
        'angka partisipasi sekolah (aps)', 'angka partisipasi sekolah',
        'aps', 'rata-rata lama sekolah', 'tingkat pendidikan',
        'angka putus sekolah', 'rasio murid-guru',
        'pengeluaran publik masuk pendidikan sebagai persentase dari total belanja pemerintah',
        'persentase balita yang ditolong penolong kelahiran',
        'persentase bayi lahir ditolong nakes',
        'persentase bayi lahir ditolong non-nakes',
        'indeks konsumsi rumah tangga (ikrt)',
        'indeks konsumsi rumah tangga', 'ikrt', 'cakupan imunisasi',
        'persentase balita yang sudah diimunisasi lengkap',
        'persentase penduduk sakit dengan pengobatan sendiri',
        'persentase penduduk sakit yang konsultasi ke tenaga medis',
        'persentase penduduk sakit yang menjalani rawat inap di rs/klinik yang menyediakan tenaga medis',
        'persentase penduduk sakit yang menjalani rawat inap di rumah sakit yang menyediakan tenaga medis',
        'persentase penduduk sakit yang menjalani rawat inap di rs yang menyediakan tenaga medis',
        'persentase penduduk sakit yang menjalani rawat inap di klinik yang menyediakan tenaga medis',
        'rata-rata jumlah anak yang pernah dilahirkan/paritas',
        'anak lahir hidup (alh)', 'anak lahir hidup', 'alh',
        'anak masih hidup (amh)', 'anak masih hidup', 'amh',
        'angka kelahiran kasar', 'cbr', 'angka kelahiran menurut umur',
        'asfr', 'inflasi perdesaan', 'deflasi perdesaan',
        'angka kelahiran total', 'tfr', 'angka kelahiran umum', 'gfr',
        'angka reproduksi neto', 'nrr', 'angka reproduksi kasar', 'grr',
        'rasio anak-ibu', 'umur kawin pertama (ukp)',
        'umur kawin pertama', 'ukp',
        'angka prevalensi pemakaian kontrasepsi',
        'persentase pemakai suatu cara kb menurut alat/cara kb',
        'pus memakai alat/cara kb', 'persentase pernah pakai kb',
        'persentase pus yang pernah memakai suatu cara kb',
        'angka kematian anak (aka)', 'angka kematian anak', 'aka',
        'indeks tendensi bisnis (itb)', 'indeks tendensi bisnis', 'itb',
        'tendensi bisnis', 'angka kematian balita (akba)',
        'angka kematian balita', 'akba', 'angka kematian bayi (akb)',
        'angka kematian bayi', 'akb', 'angka kematian ibu (aki)',
        'angka kematian ibu', 'aki', 'angka kematian kasar (akk)',
        'angka kematian kasar', 'akk',
        'angka kematian menurut usia (akmu)',
        'angka kematian menurut usia', 'akmu',
        'angka kematian neo-natal', 'akneo',
        'angka kematian post neo-natal', 'akpneo',
        'angka harapan hidup (ahh)', 'angka harapan hidup', 'ahh',
        'harapan hidup', 'angka kesakitan', 'angka morbiditas',
        'morbiditas',
        'persentase penduduk yang mempunyai keluhan kesehatan',
        'rata-rata lama sakit', 'indeks indikator kini (iik)',
        'indeks indikator kini', 'iik', 'tingkat prevalensi',
        'insidensi', 'angka fatalitas kasus', 'angka daya tular',
        'tingkat serangan', 'kepadatan penduduk', 'jumlah penduduk',
        'jumlah populasi penduduk', 'laju pertumbuhan penduduk',
        'pertumbuhan penduduk', 'rasio jenis kelamin', 'sex ratio', 'sr',
        'distribusi penduduk menurut wilayah',
        'persentase penduduk menurut wilayah', 'angka migrasi masuk',
        'migrasi masuk', 'indeks indikator mendatang (iim)',
        'indeks indikator mendatang', 'iim', 'angka migrasi keluar',
        'migrasi keluar', 'angka migrasi neto', 'migrasi neto',
        'migrasi seumur hidup', 'migrasi semasa hidup',
        'angka migrasi risen', 'migrasi risen', 'angka migrasi total',
        'migrasi total', 'garis kemiskinan (gk)', 'garis kemiskinan',
        'garis kemiskinan makanan', 'garis kemiskinan bukan makanan',
        'garis kemiskinan nonmakanan', 'gk', 'gkm', 'gkbm', 'gknm',
        'kemiskinan', 'angka kemiskinan', 'persentase penduduk miskin',
        'persentase kemiskinan', 'jumlah penduduk miskin',
        'tingkat kemiskinan', 'jumlah masyarakat miskin',
        'indeks kedalaman kemiskinan', 'kedalaman kemiskinan',
        'indeks keparahan kemiskinan', 'keparahan kemiskinan',
        'indeks kemiskinan manusia (ikm)', 'indeks kemiskinan manusia',
        'ikm']])
def filter_indikator(ner_string):
  # ubah ke huruf kecil
  ner_string = ner_string.lower()
  # inisiasi hasil_sub 0 dengan panjang sesuai ukuran sub_indikator
  #hasil_sub = np.zeros((114,), dtype=int)
  # ubah string menjadi list
  list_ = ast.literal_eval(ner_string)
  #setiap alias pada list di cocokkan dengan  sub indikator
  # apabila cocok maka tambahkan nilai 1 pada array hasil_sub
  # menurut indeks sub yg bersangkutan
  alias_fix=[]
  kode = []
  for alias_ in list_:
    try:
      indeks = int(sub_indikator[0][np.where(sub_indikator[1]==alias_)[0][0]])
      #hasil_sub[int(indeks)] +=1    
      alias_fix.append(alias_)
      kode.append("IND"+str("%03d" % indeks))
    except IndexError:
      continue
  return [alias_fix,kode]

db = Database_connection()
connection = db.connection
cursor = db.cursor
tanggal = (datetime.now()-timedelta(1)).strftime('%Y-%m-%d')
query = "SELECT * FROM `ner_tmp`"
cursor.execute(query)
list_res = cursor.fetchall()
list_indicator = [row[4] for row in list_res]
print(filter_indikator('["inflasi","ihk"]'))

for ind in list_indicator:
	print(filter_indikator(ind))


sys.exit("debugging...")

list_person = get_summary([row[1] for row in list_res],'tokoh',tanggal)
list_organization = get_summary([row[2] for row in list_res],'organisasi',tanggal)
list_position = get_summary([row[3] for row in list_res],'posisi',tanggal)
list_indicator = get_summary([row[4] for row in list_res],'indikator',tanggal)
list_location = get_summary([row[5] for row in list_res],'lokasi',tanggal)
list_quote = get_summary([row[6] for row in list_res],'kutipan',tanggal)

semua_list_tuple = []
semua_list_tuple.extend(list_person)
semua_list_tuple.extend(list_organization)
semua_list_tuple.extend(list_indicator)
semua_list_tuple.extend(list_position)
semua_list_tuple.extend(list_location)
semua_list_tuple.extend(list_quote)
#insert ke database 	


query_insert = "INSERT INTO `ner_table` (tanggal,jenis,nama,jumlah) VALUES (%s,%s,%s,%s)"


cursor.executemany(query_insert, semua_list_tuple)

connection.commit()

print(cursor.rowcount, "was inserted.")
