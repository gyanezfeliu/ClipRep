# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:00:00 2018

@author: Guillermo Yáñez
"""
#Librerías
import matplotlib.pyplot as plt
from datetime import time
import numpy as np

#Inputs de trabajo
#Agregar control flow como por ejemplo isalpha()
fecha = input(str('Ingrese fecha: '))
rango = int(input('Gráficos en rango de 5, 30 o 60 minutos?: '))
puntos=0
sumados=0
negocios = ['CL', 'AR']
LPAR = ['FR1', 'FR2', 'SW1', 'SW2']
nombre_archivo= ''
CPU= []
Disco= []
Usuarios= []
lista = []
subc = []
cpu_col=0;
disco_col=0;
usuario_col=0;

if len(LPAR)==4:
    colores=['m','c','b','g']
else:
    colores=['b', 'g']
    
#Ciclo que arma las matrices de CPU, Disco y Usuarios con las variables para 
#Los 2 negocios

if rango == 60:
    puntos=24
    sumados=12
elif rango == 30:
    puntos=48
    sumados=6
elif rango == 5:
    puntos=288
    sumados=1
for n in range(0,len(negocios)):
    #Matriz CPU
    CPU=[]
    #Matriz Disco
    Disco=[]
    #Matriz Usuarios
    Usuarios=[]
    
    #las 4 LPAR
    for j in LPAR:
        #Agrega cada línea a lista sólo si empieza con números de hora
        nombre_archivo='PF'+j+negocios[n]+fecha
        archivo = open(nombre_archivo + '.txt','r')
        #archivo = open(nombre_archivo + '.txt')
        #Arreglo con todos los datos del archivo, con elementos de strings
        lista = []
        
        for linea in archivo:
            if linea[0] == '0' or linea[0] == '1' or linea[0] == '2':
                
                lista.append(linea)
        
        #Matriz con los datos separados como strings en una matriz
        matriz = []           
        for i in lista:
            y = i.split()
            matriz.append(y)

        #Tiempo
        x = []
        #CPU
        y1 = []
        #Disco
        y2 = []
        #Pool usuarios
        y3 = []
        
        for i in range(0, puntos):
            if i != puntos-1:
                subc = matriz[i*sumados:(i+1)*sumados]                    
            else:
                if sumados == 1:
                    subc = matriz[len(matriz)-1:]
                else:
                    subc = matriz[i*sumados:(i+1)*sumados - 1]             

            x.append(time(int(subc[len(subc)-1][0][:2]), int(subc[len(subc)-1][0][3:])))
            
            #Saco la hora y dejo solamente los números
            subc = [subc[j][1:] for j in range(0, len(subc))]
            #Reemplazo las ',' por '.'
            for j in range(0, len(subc)):
                for k in range(0, len(subc[0])):
                    subc[j][k]=subc[j][k].replace('.', '');
                    subc[j][k]=subc[j][k].replace(',', '.');
            
            if 'AR' in nombre_archivo:
                cpu_col=3;
                disco_col=11;
                usuario_col=14;
            else:
                cpu_col=3;
                disco_col=12;
                usuario_col=15;
            y1.append(np.mean(np.array(list(np.float_(subc)))[:,cpu_col]))
            y2.append(np.mean(np.array(list(np.float_(subc)))[:,disco_col]))
            y3.append(np.mean(np.array(list(np.float_(subc)))[:,usuario_col]))
                
        CPU.append(y1)
        Disco.append(y2)
        Usuarios.append(y3)    

    ejex = []
    for l in range(0,24,2):
        ejex.append(time(l,0))
        
    ejex.append(time(23,59))
    
    
    
    #Gráficos CPU
    for g in range(0,len(LPAR)):
        plt.plot(x, CPU[g], colores[g], linewidth = 1.5, label = LPAR[g])
    plt.axhline(100, color = 'r')
    plt.xticks(ejex, rotation= 30)
    plt.legend(loc="upper left")
    plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
    plt.title('Utilización de CPU '+negocios[n])
    plt.axis([ejex[0], ejex[len(ejex)-1], 0, 160])
    
    if 'CL' in nombre_archivo:
    
        #Procesos
        #Malla Extract SWT1
        plt.axhline(y=0, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axvline(x=300, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=1200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa con LHT SWT2 
        plt.axhline(y=0, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axvline(x=1900, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=5400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Malla Renewall SWT1
        plt.axhline(y=0, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axvline(x=14400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=21600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga TRX
        plt.axhline(y=0, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=75600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa sin LHT SWT1
        plt.axhline(y=0, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=82800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)    
        
        #Extract HA SWT1 y SWT2
        plt.axhline(y=0, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=84600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
    
    elif 'AR' in nombre_archivo:
        #Procesos
        #Extract y Depuración nativa
        plt.axhline(y=0, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Ejecución Renewall
        plt.axhline(y=0, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axhline(y=152, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axvline(x=25200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
    
    plt.show()
    
    #Gráficos Disco

    for g in range(0,len(LPAR)):
        plt.plot(x, Disco[g], colores[g], linewidth = 1.5, label = LPAR[g])
    plt.axhline(40, color = 'r')
    plt.xticks(ejex, rotation= 30)
    plt.legend(loc="upper right")
    plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
    plt.title('Utilización Brazo de Disco '+negocios[n])
    plt.axis([ejex[0], ejex[len(ejex)-1], 0, 70])
    
    if 'CL' in nombre_archivo:
        #Procesos
        #Malla Extract SWT1
        plt.axhline(y=0, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axvline(x=300, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=1100, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa con LHT SWT2
        plt.axhline(y=0, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axvline(x=1900, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=5400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Malla Renewall SWT1
        plt.axhline(y=0, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axvline(x=14400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=21600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga TRX
        plt.axhline(y=0, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=75600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa sin LHT SWT1
        plt.axhline(y=0, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=82800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)    
        
        #Extract HA SWT1 y SWT2
        plt.axhline(y=0, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=84600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
   
    elif 'AR' in nombre_archivo:
        #Procesos
        #Extract y Depuración nativa
        plt.axhline(y=0, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Ejecución Renewall
        plt.axhline(y=0, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axhline(y=66.5, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axvline(x=25200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
    
    plt.show()
    
    #Gráficos Pool de usuarios
    for g in range(0,len(LPAR)):
        plt.plot(x, Usuarios[g], colores[g], linewidth = 1.5, label = LPAR[g])
    plt.axhline(y=400, color = 'r')
    plt.xticks(ejex, rotation= 30)
    plt.legend(loc="upper right")
    plt.xlabel(fecha[0:2]+'/'+fecha[2:4]+'/20'+fecha[4:])
    plt.title('Faltas en pool de usuarios '+negocios[n])
    plt.axis([ejex[0], ejex[len(ejex)-1], 0, 600])
    
    if 'CL' in nombre_archivo:
    
        #Procesos
        #Malla Extract SWT1
        plt.axhline(y=0, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0, xmax=0.01388889, color = 'k', alpha=0.2)
        plt.axvline(x=300, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=1200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa con LHT SWT2
        plt.axhline(y=0, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.02199074, xmax=0.0625, color = 'k', alpha=0.2)
        plt.axvline(x=1900, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=5400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Malla Renewall SWT1
        plt.axhline(y=0, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.1666667, xmax=0.25, color = 'k', alpha=0.2)
        plt.axvline(x=14400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=21600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Carga TRX
        plt.axhline(y=0, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.375, xmax=0.875, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=75600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Dep Nativa sin LHT SWT1
        plt.axhline(y=0, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.9166667, xmax=0.9583333, color = 'k', alpha=0.2)
        plt.axvline(x=79200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=82800, ymin=0, ymax=0.95, color = 'k', alpha=0.2)    
        
        #Extract HA SWT1 y SWT2
        plt.axhline(y=0, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.979, xmax=1, color = 'k', alpha=0.2)
        plt.axvline(x=84600, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=86400, ymin=0, ymax=0.95, color = 'k', alpha=0.2) 
   
    elif 'AR' in nombre_archivo:
        #Procesos
        #Extract y Depuración nativa
        plt.axhline(y=0, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0, xmax=0.082, color = 'k', alpha=0.2)
        plt.axvline(x=0, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=7200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        
        #Ejecución Renewall
        plt.axhline(y=0, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axhline(y=570, xmin=0.29, xmax=0.375, color = 'k', alpha=0.2)
        plt.axvline(x=25200, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
        plt.axvline(x=32400, ymin=0, ymax=0.95, color = 'k', alpha=0.2)
    
    plt.show()
    
archivo.close()