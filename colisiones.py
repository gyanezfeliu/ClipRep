# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 15:05:22 2018

@author: Guillermo Yañez
"""

import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta
import numpy as np

contador=0
resumen=[]
cont=[]
resultado=''
col=[]
horas_dia=[]
tiempo_col=[]
col_fin=[]
ejex = []

fecha = input(str('Ingrese fecha: '))
LPAR = ['ARS1', 'ARS2', 'CLS1', 'CLS2']

#Genero vector de horas
for i in range(0,24):
    for j in range(0, 60, 30):
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

for n in LPAR:
    resumen=[]
    cont=[]
    resultado=''
    col=[]
    tiempo_col=[]
    col_fin=[]
    try:
        archivo = open(n+'COL'+fecha[2:4]+fecha[:2] + '.txt','r')
        lista = []    
        for linea in archivo:
            if 'FILE' not in linea and '*' not in linea:
                lista.append(linea)
                #Matriz con los datos separados como strings en una matriz    
        del lista[len(lista)-1]
        matriz = []           
        
        for i in lista:
            y = i.split()
            matriz.append(y)
    
        files=list(set([row[0] for row in matriz]))
    
        for i in range(0, len(files)):
            contador=0
            for j in range(0, len(matriz)):
                if matriz[j][0]==files[i]:
                    contador+=1
            cont.append(contador)
        resumen.append(files)    
        resumen.append(cont)
        
        resultado='Colisiones en '+n+'\n'
        for i in range(0, len(files)):
            resultado+=resumen[0][i]+': '+str(resumen[1][i])+'\n'
        print(resultado)
        
        for i in range(0, len(matriz)):
            matriz[i][2]=int(matriz[i][2][11:13]+matriz[i][2][14:16])
       
        matriz.sort(key=lambda x: x[2])
        
        for i in range(0, len(horas_dia)):
            contador=0
            for j in range(0, len(matriz)):
                if matriz[j][2]<=horas_dia[i]:
                    contador+=1
                else:
                    break
            col.append(contador)
            tiempo_col.append(horas_dia[i])
       
        col_fin.append(col[0])
        for i in range(1,len(col)):
            col_fin.append(col[i]-col[i-1])
        
        """ 
        i=0
        while i < len(col_fin):
            if col_fin[i]==0:
                del col_fin[i]
                del tiempo_col[i]
            else:
                i+=1
        """
        
        for i in range(0, len(tiempo_col)):
            tiempo_col[i] = time(int(str(tiempo_col[i]).rjust(4, '0')[:2]), int(str(tiempo_col[i]).rjust(4, '0')[2:]))
        
        global eje
        eje = [time(0,0), time(3,0), time(6,0), time(9,0), time(12,0), time(15,0), time(18,0), time(21,0), time(23,59)]
                                  
        #Gráfico
        #Por máquina
        plt.plot(tiempo_col, col_fin, 'g', linewidth = 1, label = n)
        plt.axhline(50, color = 'r')
        plt.xticks(eje, rotation= 30)
        plt.xlabel(fecha[:2]+"/"+fecha[2:4]+"/"+fecha[4:])
        plt.ylabel("Colisiones")
        plt.legend(loc="upper left")
        plt.title('Colisiones '+n)
        plt.show()
    except:
        print ("No hay colisiones en "+n)