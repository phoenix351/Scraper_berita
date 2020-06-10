import pandas as pd
import numpy as np
from tqdm import tqdm


from NER_processing import ner_modeling


data_total = pd.read_csv("c:/data/berita_detail.csv")
isi = data_total.isi.copy()
isi_ar = np.array(isi)
del data_total,isi
vektor =[]
i = 0 
for row in tqdm(isi_ar):
	id = "B" + "%02d" %i
	vektor.append(ner_modeling(row,i))
	i = i + 1


pd.DataFrame(vektor).to_csv("hasil.csv",header=False,index=False)




