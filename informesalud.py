# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:10:00 2018

@author: Guillermo Yañez
"""
#------------------#
# Informe de Salud #
#------------------#

import os
import funciones as fn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import time

negocio = ['Chile', 'Argentina', 'Perú']
site = ['SWT1', 'SWT2']
LPAR = ['CLS1', 'CLS2','PES1', 'PES2', 'ARS1', 'ARS2']
matriz_dia = pd.DataFrame()

fecha = input(str('Ingrese Fecha: '))

#-------------------#
#   Transacciones   #
#-------------------#

# Cargar y consolidar la BD de transacciones
print("************* Cargando base de datos... *************")
for l in LPAR:
    name = l + 'TR' + fecha[2:4]+fecha[:2] + '.CSV'
    if os.path.exists(name):
        # Cargo la BD
        if 'AR' in name:
            df = fn.cargar_arg(l, fecha)
        else:
            df = fn.cargar(l, fecha)
        # Si hay transacciones, las agrego a la matriz consolidada del día
        if len(df) > 0:
            matriz_dia = matriz_dia.append(df, ignore_index = True)
        else:
            print("No hubo transacciones en {} para el día {}".format(l, fecha))
    else:
        print("No está el archivo de {} para el día {}".format(l, fecha))
print("************ Base de datos cargada *************")

# Gráficos
fn.graficar_trx(matriz_dia, negocio, site, fecha)

# Calidad
fn.calidad_trx(matriz_dia, site, fecha)