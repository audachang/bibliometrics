import pandas as pd
import glob

allfn = glob.glob('../../data/csv*.csv')


data = pd.DataFrame()

for fn in allfn:
	tmp = pd.read_csv(fn)
	data = pd.concat((data, tmp))

data.to_csv("../../data/pubmed_2019-2024.csv")