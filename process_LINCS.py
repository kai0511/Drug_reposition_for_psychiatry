import os
import re
import pandas as pd
import numpy as np
from cmapPy.pandasGEXpress import parse

os.chdir('/exeh/exe3/zhaok/data')

# extract all samples that were treated with vorinostat
sig_info = pd.read_csv("GSE92742_Broad_LINCS_sig_info.txt", sep="\t")

# unique the pert name set
pert_set = set(sig_info["pert_iname"])

# read N05A data file
drug_list = pd.read_csv('N05A.txt', header=None)
drug_list.columns = ['names']
drug_list = [d.lower() for d in drug_list['names']]

# search pattern
se_pattern = "|".join(drug_list) 

# find the fuzzy intersection set
search_res = [s for s in pert_set if bool(re.search(se_pattern, s)) == True]

idx = np.repeat(False, sig_info.shape[0])

for s in search_res:
    idx[sig_info["pert_iname"] == s] = True

# generate positive observations    
sig_id = sig_info["sig_id"][idx]

# print its size
print("number of samples treated with N051A drug: %s" % len(sig_id))

# parse gene expression data using sig_id obtained in the above step 
positive_gctx = parse('GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx', cid=sig_id)

# write result to a csv file
(positive_gctx.data_df.T).to_csv('GSE92742_Broad_LINCS_Level5_COMPZ_N05A.csv')