# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:00:00 2018

@author: Guillermo Yáñez
"""
#Librerías
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta
import numpy as np


#Inputs de trabajo
fecha = input(str('Ingrese fecha: '))
rango = int(input('Gráficos en rango de 5, 30 o 60 minutos?: '))
puntos = 0
sumados = 0
horas_dia = []
hora = '';
mins = '';
recursos = ['CPU','DISCO', 'MEMORIA']
LPAR = ['FR1', 'FR2', 'SW1', 'SW2']
nombre_archivo = ''
valor_recursos = []
lista = []
colores = ['m','c','b','g']
t1 = []
f1 = []
f2 = []
s1 = []
s2 = []

if rango == 60:
    puntos = 24
    sumados = 12
elif rango == 30:
    puntos = 48
    sumados = 6
elif rango == 5:
    puntos=288
    sumados=1
    
for j in recursos:
    t1 = []
    f1 = []
    f2 = []
    s1 = []
    s2 = []
    nombre_archivo=j+fecha
    archivo = open(nombre_archivo + '.txt','r')

    lista = []
   
    for linea in archivo:
        #print(str(linea[0])
        if linea[0] != 'F' and linea[0] != '-' and linea[0] != '\n':
            
            lista.append(linea)
    matriz = []           

    for i in lista:
        y = i.split()
        matriz.append(y[1:])           

    #Limpiar la matriz en caso que venga con '.' en vez de un dato, o con una ','
    #que señale separador de miles:
    for i in range(0,len(matriz)):
        
        matriz[i][2]=matriz[i][2].replace(',','')
        matriz[i][3]=matriz[i][3].replace(',','')
        matriz[i][4]=matriz[i][4].replace(',','')
        matriz[i][5]=matriz[i][5].replace(',','')
        
        if i != 0:
            if matriz[i][2]=='.':
                matriz[i][2] = matriz[i-1][2]
            if matriz[i][3]=='.':
                matriz[i][3] = matriz[i-1][3]
            if matriz[i][4]=='.':
                matriz[i][4] = matriz[i-1][4]
            if matriz[i][5]=='.':
                matriz[i][5] = matriz[i-1][5]
        else:
            if matriz[i][2]=='.':
                matriz[i][2] = 0
            if matriz[i][3]=='.':
                matriz[i][3] = 0
            if matriz[i][4]=='.':
                matriz[i][4] = 0
            if matriz[i][5]=='.':
                matriz[i][5] = 0

    for i in range(0, puntos):
        if i != puntos-1:
            subc = matriz[i*sumados:(i+1)*sumados]                    
        else:
            if sumados == 1:
                subc = matriz[len(matriz)-1:]
            else:
                subc = matriz[i*sumados:(i+1)*sumados - 1]    
        #Rutina para arreglar la hora
        #Cambiar todos los i[0] por subc[len(subc)-1][0]
        if len(subc[len(subc)-1][0])==7:
            subc[len(subc)-1][0]='0'+subc[len(subc)-1][0]
        if subc[len(subc)-1][1]=='AM':
            h=int(subc[len(subc)-1][0][0:2])
            if h<10:
                h='0'+str(h)
            if h==11 or h==10:    
                h=str(h)
            if subc[len(subc)-1][0][0:2]=='12':
                h='00'
        if subc[len(subc)-1][1]=='PM' and subc[len(subc)-1][0][0:2]!='12':
            h=int(subc[len(subc)-1][0][0:2])+12
            h=str(h)
        if subc[len(subc)-1][1]=='PM' and subc[len(subc)-1][0][0:2]=='12':
            h=int(subc[len(subc)-1][0][0:2])
            h=str(h)
        
        v=h+':'+subc[len(subc)-1][0][3:5]
        v=time(int(v[:2]), int(v[3:]))
        t1.append(v)       
        
        #Saco la hora y dejo solamente los números
        subc = [subc[j][2:] for j in range(0, len(subc))]
        
        f1.append(np.mean(np.array(list(np.float_(subc)))[:,1]))
        f2.append(np.mean(np.array(list(np.float_(subc)))[:,3]))
        s1.append(np.mean(np.array(list(np.float_(subc)))[:,2]))
        s2.append(np.mean(np.array(list(np.float_(subc)))[:,0]))                
    
    ejex = []
    for l in range(0,24,2):
        ejex.append(time(l,0))
        
    ejex.append(time(23,59))
    
    if j=='CPU':
        plt.plot(t1, f1, colores[0], linewidth = 1.5, label = LPAR[0])
        plt.plot(t1, f2, colores[1], linewidth = 1.5, label = LPAR[1])
        plt.plot(t1, s1, colores[2], linewidth = 1.5, label = LPAR[2])
        plt.plot(t1, s2, colores[3], linewidth = 1.5, label = LPAR[3])
        plt.axhline(100, color = 'r')
        plt.xticks(ejex, rotation= 30)
        plt.legend(loc="upper left")
        plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
        plt.title('Utilización de CPU PE')
        plt.axis([ejex[0], ejex[len(ejex)-1], 0, 160])
        
        #Procesos
        #Renewall Full y Diario
        plt.axhline(y=0, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=3600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga Archivos AZCLEAR
        plt.axhline(y=0, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=10800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Renewall SAT y Pivote Vencido
        plt.axhline(y=0, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axvline(x=28800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=34200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)

        #Creación Archivo Renewall SAT
        plt.axhline(y=0, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axvline(x=59400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=63000, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        #AZDEPURAR FRT y SWT
        plt.axhline(y=0, xmin=0.916667, xmax=0.958333, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.916667, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        plt.show()
    
    if j=='DISCO':
        plt.plot(t1, f1, colores[0], linewidth = 1.5, label = LPAR[0])
        plt.plot(t1, f2, colores[1], linewidth = 1.5, label = LPAR[1])
        plt.plot(t1, s1, colores[2], linewidth = 1.5, label = LPAR[2])
        plt.plot(t1, s2, colores[3], linewidth = 1.5, label = LPAR[3])
        plt.axhline(40, color = 'r')
        plt.xticks(ejex, rotation= 30)
        plt.legend(loc="upper left")
        plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
        plt.title('Utilización Brazo de Disco PE')
        plt.axis([ejex[0], ejex[len(ejex)-1], 0, 70])
        
        #Procesos
        #Renewall Full y Diario
        plt.axhline(y=0, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=3600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga Archivos AZCLEAR
        plt.axhline(y=0, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=10800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Renewall SAT y Pivote Vencido
        plt.axhline(y=0, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axvline(x=28800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=34200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
          
        #Creación Archivo Renewall SAT
        plt.axhline(y=0, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axvline(x=59400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=63000, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        #AZDEPURAR FRT y SWT
        plt.axhline(y=0, xmin=0.916667, xmax=0.958333, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.916667, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        plt.show()
    
    if j=='MEMORIA':
        plt.plot(t1, f1, colores[0], linewidth = 1.5, label = LPAR[0])
        plt.plot(t1, f2, colores[1], linewidth = 1.5, label = LPAR[1])
        plt.plot(t1, s1, colores[2], linewidth = 1.5, label = LPAR[2])
        plt.plot(t1, s2, colores[3], linewidth = 1.5, label = LPAR[3])
        plt.axhline(400, color = 'r')
        plt.xticks(ejex, rotation= 30)
        plt.legend(loc="upper left")
        plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
        plt.title('Faltas en pool de usuarios PE')
        plt.axis([ejex[0], ejex[len(ejex)-1], 0, 600])
        
        #Procesos
        #Renewall Full y Diario
        plt.axhline(y=0, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0, xmax=0.041667, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=3600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga Archivos AZCLEAR
        plt.axhline(y=0, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.083333, xmax=0.125, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=10800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Renewall SAT y Pivote Vencido
        plt.axhline(y=0, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.333333, xmax=0.395833, color = 'k', alpha=0.2)
        plt.axvline(x=28800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=34200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
          
        #Creación Archivo Renewall SAT
        plt.axhline(y=0, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.6875, xmax=0.729167, color = 'k', alpha=0.2)
        plt.axvline(x=59400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=63000, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        #AZDEPURAR FRT y SWT
        plt.axhline(y=0, xmin=0.916667, xmax=0.958333, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.916667, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
        
        plt.show()
        
        archivo.close()