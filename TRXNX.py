# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 14:43:07 2018

@author: Guillermo Yañez
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time, datetime

plt.rcParams["figure.figsize"] = (12,8)

LPAR = ['TPS Paine OC', 'TPS Paine REP', 'TPS Liray OC', 'TPS Liray REP']


df_total = pd.read_excel('TRXCONS.xlsx')

# Suma Réplicas
df_REP = df_total[df_total['OC/REP'] == 'REP']
df_OC = df_total[df_total['OC/REP'] == 'OC']
df_liray = df_total[df_total['LPAR'] == 'Liray']
df_paine = df_total[df_total['LPAR'] == 'Paine']

filtro = df_total['WFHAPG'].unique()

def graficar_apl(df, nombre, filtro):
    max_tps = pd.DataFrame()
    hora = []
    apli = pd.DataFrame()
    
    for i, value in enumerate(filtro):
        apl = df[df['WFHAPG'] == value]
        hora = list(apl['HORAGRABA'])
        hora = [int(i) for i in hora]
        hora = [str(i).rjust(6, '0') for i in hora]
        hora = [time(int(i[:2]), int(i[2:4]), int(i[4:])) for i in hora]
        apl['Hora'] = hora
        
        max_tps = max_tps.append(apl.iloc[apl['TPS'].argsort()[-3:]], ignore_index = True)
        apli = apli.append(apl, ignore_index = True)
        
        plt.plot(apl['Hora'], apl['TPS'], label = value)
    
    
    plt.ylabel("TPS")
    plt.xlabel("Hora")
    plt.legend(loc="upper right", prop={'size': 9})
    plt.title('TPS '+nombre)
    plt.show()
    
    for i in max_tps['WFHAPG'].unique():
        apl2 = max_tps[max_tps['WFHAPG']==i]
        plt.plot(apl2['Hora'], apl2['TPS'], 'o', label = i)
        plt.legend(loc="upper right", prop={'size': 9})
    plt.ylabel("TPS")
    plt.xlabel("Hora")
    plt.title('TPS máximas '+nombre)
    plt.show()
    print('TPS máximas '+nombre)
    print(max_tps)
    
    return max_tps, apli
#maximo, apl = graficar_apl(df_REP, 'Réplicas', filtro)
#maximo, apl = graficar_apl(df_OC, 'Otros canales', filtro)
#maximo, apl = graficar_apl(df_liray, 'Liray', filtro)
#maximo, apl = graficar_apl(df_paine, 'Paine', filtro)

    
def graficar_maximos(maximo, df):
    tps_max = [df[df['Hora'] == maximo['Hora'].iloc[i]]['TPS'].sum() for i in range(0, len(maximo))]
    plt.plot(list(maximo['Hora']), tps_max, 'o')
    d = {'Hora': list(maximo['Hora']), 'TPS': tps_max}
    df = pd.DataFrame(data=d)
    df = df.sort_values(['Hora'], ascending= 1)
    return df