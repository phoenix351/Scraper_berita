from sentistrength_id.sentistrength_id import sentistrength
from sentistrength_id_negasi.sentistrength_id_negasi import sentistrength_negasi

# Untuk mengelompokkan sentimen berita dan sentimen kutipan

def sentiment(id_berita,konten,kutipan,indikator):
    # config
    config = dict()
    config["negation"] = True
    config["booster"] = True
    config["ungkapan"] = True
    config["consecutive"] = True
    config["repeated"] = True
    config["emoticon"] = True
    config["question"] = True
    config["exclamation"] = True
    config["punctuation"] = True
    senti = sentistrength(config)
    senti_negasi = sentistrength_negasi(config)
    skor = 0

    # select konten berita hasil prediksi dari database
    
    #kutipan = row[2]
    r = indikator
    # mendefinisikan indikator negasi
    negasi = [line.replace('\n','') for line in open("indikator_negasi.txt").read().splitlines()]
    # jika indikator merupakan indikator negasi
    if r in negasi:
        senti_konten = senti_negasi.main(konten)
        senti_kutipan = senti_negasi.main(kutipan)
        # jika bukan indikator negasi
    else:
        senti_konten = senti.main(konten)
        senti_kutipan = senti.main(kutipan)
    
    sk = senti_konten['kelas']
    sq = senti_kutipan['kelas']

    sent = {
    'id_berita':id_berita,
    'indikator':indikator
    'sentimen_isi':sk,
    'sentimen_kutipan':sq
    }
    return sent

 
