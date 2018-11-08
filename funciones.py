# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:11:25 2018

@author: Guillermo Yañez
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import time, datetime
from texttable import Texttable
import math

colores = ['g', 'r']

# Cargo la base de datos en un DF
# La idea es que después este método reciba otro parámetro que corresponde
# al tipo de carga que se hará, de TR, PF, o COL
def cargar(LPAR, fecha):
    # Para TR
    name = LPAR + 'TR' + fecha[2:4]+fecha[:2]
    # Por ahora se hace esta separación, la idea es que vengan todos en .csv
    if 'PE' in LPAR:
        df = procesar_pe(name + '.CSV')
    else:
        df = pd.read_csv(name + '.CSV', sep = ';', 
                         names = ['nodo', 'negocio', 'autorizador', 'hora_ini', 
                                   'fecha', 'hora_grab', 'mlsec_grab', 
                                   'prom_tpo_resp', 'total_trx', 'negadas', 
                                   'aprobadas', 'time_out', 'std_in'])

    # Saco las columnas que no usaré
    if df.empty == False:
        df = df.drop(['hora_grab', 'mlsec_grab'], axis = 1)
    
        # Cambio el formato de la fecha
        df[['fecha']] = pd.to_datetime(df['fecha'].iloc[0], format = '%Y%m%d')
    
        horas = list(df['hora_ini'])
        horas = [time(int(str(i).rjust(4, '0')[:2]), int(str(i).rjust(4, '0')[2:])) 
                for i in horas]
        df['hora_ini'] = pd.Series(horas)
        
    # Si es Perú, me aseguro que la columna negocio tenga el formato correspondiente
    
    return df

def generar_horas():
    horas_dia = []
    #Genero vector de horas
    for i in range(0,24):
        for j in range(0, 60, 5):
            if i<10:
                hora = '0'+str(i)
            else:
                hora = str(i)
            if j<10:
                mins = '0'+str(j)
            else:
                mins = str(j)
            horas_dia.append(int(hora+mins))
            
    horas_dia.remove(horas_dia[0])
    horas_dia.append(2359)
    return horas_dia

def cargar_arg(LPAR, fecha):

    matriz = []
    trx_fin = []
    ejex = []
    
    file_name =LPAR +'TR'+fecha[2:4]+fecha[:2]+'.CSV'
    
    # Abre archivo
    with open(file_name) as csvfile1:
                matriz = list(csv.reader(csvfile1))
    
    if len(matriz) > 1:
        trx_fin, ejex = agrupar_trx(matriz)
    
    df = pd.DataFrame([], columns = ['nodo', 'negocio', 'autorizador', 'hora_ini', 
                                   'fecha', 'hora_grab', 'mlsec_grab', 
                                   'prom_tpo_resp', 'total_trx', 'negadas', 
                                   'aprobadas', 'time_out', 'std_in'])
    if len(trx_fin) > 0:
        df['total_trx'] = trx_fin
        df['hora_ini'] = ejex
        df['nodo'] = 'SWT' + LPAR[3]
        df['negocio'] = 'Argentina'
        df['fecha'] = pd.to_datetime(formatear_fecha(fecha), format = '%Y%m%d')
    df = df.drop(['hora_grab', 'mlsec_grab'], axis = 1)
    
    return df

def agrupar_trx(mact):
    contador = 0
    trx = []
    trx_fin = []
    ejex = []    
    horas_dia = generar_horas()
    
    mact.sort(key=lambda x: int(x[3]))
    # Convierte de str a int
    for i in range(0, len(mact)):
        mact[i][3]=int(mact[i][3])
    
    #Recorre el archivo origen y crea uno agrupado según las horas del día
    for i in range(0, len(horas_dia)):
        for j in range(0,len(mact)):
            #La hora de arg es menor a la hora del dia
            if mact[j][3]<horas_dia[i]:
                contador+=1
            #La hora de arg es igual a la hora del dia
            elif mact[j][3] == horas_dia[i]:
                #No estoy al final de la matriz
                if j+1<len(mact):
                    #El siguiente elemento de arg cambia de rango del día
                    if mact[j+1][3] > horas_dia[i]:
                        contador+=1
                        trx.append(contador)
                        contador=0
                        ejex.append(horas_dia[i])
                        i+=1
                        break                   
                    #El siguiente elemento de arg no cambia de rango del día
                    else:
                        contador+=1
                #Estoy al final de la matriz
                else:
                    #termino el ciclo
                    contador+=1
                    trx.append(contador)
                    ejex.append(horas_dia[i])
                    break
            elif mact[j][3] > horas_dia[i]:
                trx.append(contador)
                contador=1
                ejex.append(horas_dia[i])
                i+=1
                break
    
    # Arregla el resultado, restando el anterior
    trx_fin.append(trx[0])
    for i in range(1,len(trx)):
        trx_fin.append(trx[i]-trx[i-1])
    
    # Deja el vector de tiempo en formato time
    for i in range(0, len(ejex)):
        ejex[i] = time(int(str(ejex[i]).rjust(4, '0')[:2]), int(str(ejex[i]).rjust(4, '0')[2:]))
    
    return trx_fin, ejex

def formatear_fecha(fec):
    return '20'+fec[4:]+fec[2:4]+fec[:2]

def procesar_pe(name):
    list_obj = []
    
    with open(name) as csvfile:
        csv_obj = csv.reader(csvfile)#, delimiter =';')
        for i in csv_obj:
            list_obj.append(i)

    del list_obj[-1]
    
    
    matriz = []
    
    for row in list_obj:
        matriz.append(row[0].split(";"))

    for i, row in enumerate(matriz):
        matriz[i][1] = row[1].replace('"', '')
        matriz[i][2] = row[2].replace('"', '')
    
    cols = ['nodo', 'negocio', 'autorizador', 'hora_ini', 'fecha', 'hora_grab',
            'mlsec_grab', 'prom_tpo_resp', 'total_trx', 'negadas', 'aprobadas',
            'time_out', 'std_in']
    
    df_pe = pd.DataFrame(data=matriz, columns=cols)
        
    df_pe['negocio'] = 'Perú'
    df_pe['hora_ini'] = df_pe['hora_ini'].map(lambda x: x.strip())
    
    if 'ATZ' in df_pe['autorizador'].values:
        df_pe['autorizador'] = df_pe['autorizador'].map(lambda x: x.replace('ATZ', 'VMS'))
        
    for i in cols[3:]:
        df_pe[i] = df_pe[i].astype(np.int64)
    
    return df_pe

def graficar_trx(matriz_dia, negocio, site, fecha):
    eje = [time(0,0), time(3,0), time(6,0), time(9,0), time(12,0), time(15,0), time(18,0), time(21,0), time(23,59)]

    for n in negocio:
        for i, s in enumerate(site):
            pais_site = matriz_dia[(matriz_dia['negocio'] == n) & (matriz_dia['nodo'] == s)]
            grupo = pais_site.groupby(['hora_ini'])['total_trx'].sum()
            plt.plot(grupo.index, grupo/300, colores[i], linewidth = 1, label = n + ' ' + s) 
        plt.xticks(eje, rotation= 30)
        plt.xlabel(fecha[:2]+"/"+fecha[2:4]+"/"+fecha[4:])
        plt.ylabel("TPS")
        plt.legend(loc="upper left")
        plt.title('TPS ' + n)
        plt.show()   
        
def calidad_trx(matriz_dia, site, fecha):
    # Para cada Chile y Perú
    negocio = ['Chile', 'Perú']
    var = matriz_dia.columns[6:]
    
    for n in negocio:
        for i, s in enumerate(site):
            pais_site = matriz_dia[(matriz_dia['negocio'] == n) & (matriz_dia['nodo'] == s)]
            #autorizadores = pais_site['autorizador'].unique()
            autorizadores = np.asarray(np.sort(list(pais_site['autorizador'].unique()), axis=-1), dtype = object)
            
                        ## Calidad ##
            calidad = []
            row = []
            x = np.insert(autorizadores, obj = 0, values = 'Autorizadores')
            head = list(np.insert(x, obj = len(x), values = 'Total'))
            calidad.append(head)
            
            for v in var:
                row = []
                row.append(v) 
                for a in autorizadores:
                    pais_site_aut = pais_site[pais_site['autorizador'] == a]
                    grupo = pais_site_aut.groupby(['autorizador'])[v].sum()
                    row.append(int(grupo))
                row.append(pais_site[v].sum())    
                calidad.append(row)
            
            ## Muestro la tabla
            ancho = []
            for i, value in enumerate(calidad[0]):
                ancho.append(6)
            ancho[0] = 9
            t = Texttable()
            t.set_cols_width(ancho)
            t.add_rows(calidad)
            print("\n")
            print("Calidad transaccional para {} {}".format(n, s))
            print(t.draw())
            
            ## Tiempos respuesta
            tiempos = []
            head2 = head[:len(head)-1]
            tiempos.append(head2)
            for t in ['Mínimo', 'Promedio', 'Máximo']:
                row = []
                row.append(t) 
                for a in autorizadores:
                    grupo = 0
                    pais_site_aut = pais_site[pais_site['autorizador'] == a]
                    if t == 'Mínimo':
                        grupo = min(pais_site_aut['prom_tpo_resp'])
                    elif t == 'Promedio':
                        grupo = pais_site_aut['prom_tpo_resp'].sum() / len(pais_site_aut['prom_tpo_resp'])
                    elif t == 'Máximo':
                        grupo = max(pais_site_aut['prom_tpo_resp'])
                    row.append(int(grupo))
                tiempos.append(row)
            ancho = []
            for i, value in enumerate(tiempos[0]):
                ancho.append(6)
            ancho[0] = 9
            t2 = Texttable()
            t2.set_cols_width(ancho)
            t2.add_rows(tiempos)
            print("\n")
            print("Tiempos de respueta para {} {}".format(n, s))
            print(t2.draw())
                
    
    # Para Argentina
    grupo = []
    for i, s in enumerate(site):
        pais_site = matriz_dia[(matriz_dia['negocio'] == 'Argentina') & (matriz_dia['nodo'] == s)]
        grupo.append(pais_site['total_trx'].sum())
        
    t = Texttable()
    t.add_rows([['Nodo', 'Switch 1', 'Switch 2'],
                ['Total TRX', grupo[0], grupo[1]]])
    print("\n")
    print("Para Argentina")
    print(t.draw())
    