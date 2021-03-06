
#TODO 2 GRÁFICOS (INSERCAO/BUSCA)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
from matplotlib import style

dfs_busca_div = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_div.csv', usecols=[3]),
    pd.read_csv(r'./out/busca_hash_aberto_divisao.csv', usecols=[3])]

dfs_busca_mul = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_mul.csv', usecols=[3]),
    pd.read_csv(r'./out/busca_hash_aberto_multiplicacao.csv', usecols=[3])]

dfs_busca_pri = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_primos.csv', usecols=[3]),
    pd.read_csv(r'./out/busca_hash_aberto_primos.csv', usecols=[3])]

dfs_busca_duplo = [
    pd.read_csv(r'./out/busca_hash_fechado_duplo.csv', usecols=[3]),
    pd.read_csv(r'./out/busca_hash_aberto_duplo.csv', usecols=[3])]

dfs_insercao_div = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_div.csv', usecols=[2]),
    pd.read_csv(r'./out/busca_hash_aberto_divisao.csv', usecols=[2])]

dfs_insercao_mul = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_mul.csv', usecols=[2]),
    pd.read_csv(r'./out/busca_hash_aberto_multiplicacao.csv', usecols=[2])]

dfs_insercao_pri = [
    pd.read_csv(r'./out/busca_hash_fechado_overflow_primos.csv', usecols=[2]),
    pd.read_csv(r'./out/busca_hash_aberto_primos.csv', usecols=[2])]

dfs_insercao_duplo = [
    pd.read_csv(r'./out/busca_hash_fechado_duplo.csv', usecols=[2]),
    pd.read_csv(r'./out/busca_hash_aberto_duplo.csv', usecols=[2])]

dfs_busca = [dfs_busca_div, dfs_busca_mul, dfs_busca_pri, dfs_busca_duplo]
dfs_insercao = [dfs_busca_div, dfs_insercao_mul, dfs_insercao_pri, dfs_insercao_duplo]

df_types = [
    'Fechado',
    'Aberto']

df_names = [
    'Divisão',
    'Multiplicação',
    'Primo',
    'Duplo']

combined_df_names = []
for type in df_types:
    for name in df_names:
        combined_df_names.append(type + " " + name)

#region Clean data frame
def dataframeCleaner(df, name):
    df.sort_values(df.keys()[0], inplace=True) #sort the values
    df.drop(index=df.index[0], axis=0, inplace=True) #remove the smallest value (high chance of being outlier)
    df.drop(index=df.index[len(df.index) - 1], axis=0, inplace=True) #remove the biggest value (high chance of being outlier)
    df.reset_index(drop=True, inplace=True)
    #print(name)
    #print(df)

for dfs in dfs_busca:
    for df, name in zip(dfs, df_names):
        dataframeCleaner(df, name)

for dfs in dfs_insercao:
    for df, name in zip(dfs, df_names):
        dataframeCleaner(df, name)
#endregion

#region Calculate median and std 
def med_dsvp(dfs, key):
    medias = np.array([])
    dsvp = np.array([])
    for df in dfs:
        media = df.mean()
        medias = np.append(medias, media)

        desv_pad = df.std()
        dsvp = np.append(dsvp, desv_pad)

    return medias, dsvp

busca_data_points = [[0, 0], [0, 0], [0, 0], [0, 0]]
insercao_data_points = [[0, 0], [0, 0], [0, 0], [0, 0]]

for i in range(len(dfs_busca)):
    busca_data_points[i][0], busca_data_points[i][1] = med_dsvp(dfs_busca[i], 'TempoBusca')

for i in range(len(busca_data_points)):
    print(busca_data_points[i])

for i in range(len(dfs_insercao)):
    insercao_data_points[i][0], insercao_data_points[i][1] = med_dsvp(dfs_insercao[i], 'TempoInsercao')

def GerarMediaCSV(data_points, type):
    media = []; dsvp = []
    for i in range(2):
        for data in data_points:
            media.append(data[0][i])
            dsvp.append(data[1][i])

    media_dsvp_df = pd.DataFrame([media, dsvp], index=['Média', 'Desvio'], columns=combined_df_names)
    media_dsvp_df = media_dsvp_df.round(decimals=4)
    media_dsvp_df = media_dsvp_df.transpose()
    loc = 'out/' + type + '_hash_media_dsvp.csv'
    media_dsvp_df.to_csv(loc)

GerarMediaCSV(busca_data_points, 'busca')
GerarMediaCSV(insercao_data_points, 'insercao')
#endregion

#region Generate graphs
x = np.arange(len(df_types))
width = 0.3
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()


j = 0

j = -width/2
for data, name in zip(busca_data_points, 2 * df_names):
    media_arr = [data[0][0], data[0][1]]
    dsvp_arr = [data[1][0], data[1][1]]
    ax1.errorbar(x - j, media_arr, yerr=dsvp_arr, fmt = 'o', capsize=3, label=name)
    j += width/2

j = -width/2
for data, name in zip(insercao_data_points, df_names):
    media_arr = [data[0][0], data[0][1]]
    dsvp_arr = [data[1][0], data[1][1]]
    ax2.errorbar(x - j, media_arr, yerr=dsvp_arr, fmt = 'o', capsize=3, label=name)
    j += width/2

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Tempo(s)')
ax1.set_title('Tempo de busca hash')
ax1.set_xticks(x);ax1.set_xticklabels(df_types, minor=False)
ax1.set_yticks(np.arange(0.00, 0.78, 0.03))
ax1.legend()
fig1.tight_layout()
ax1.grid(which='major', axis='y')

ax2.set_ylabel('Tempo(s)')
ax2.set_title('Tempo de inserção hash')
ax2.set_xticks(x);ax2.set_xticklabels(df_types, minor=False)
ax2.set_yticks(np.arange(0.00, 0.78, 0.03))
ax2.legend()
fig2.tight_layout()
ax2.grid(which='major', axis='y')

fig1.savefig('out/busca_hash_media_e_desv_pad.png')
fig2.savefig('out/insercao_hash_media_e_desv_pad.png')
plt.show()
#endregion
