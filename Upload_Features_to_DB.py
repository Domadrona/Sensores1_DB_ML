# -*- coding: utf-8 -*-
"""
Created on 2020

@author: Julio Jimmy Cuadros Acosta
"""
"""FUNCIONANDO SERVIDOR LOCAL """
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import numpy as np

data=np.load('Features.npy')

X=data[:,0:5]
y=data[:,5]
y=y.astype(int)#paso etiquetas a enteros


"""PRIMERO CREO DATAFRAME"""
X=pd.DataFrame(data=X)
y=pd.DataFrame(data=y)
Xdf=pd.concat([X,y], axis=1)
Xdf.columns=['Mu','Va','Skw','kurt','rms','label']

#Esta permite definir los parametros para comunicarse al server local
DB = {'servername': 'DESKTOP-QCKU2AH\SQLEXPRESS',
      'database': 'Primera_AzureFunction',
      'driver': 'driver=SQL Server Native Client 11.0'}

#realizo la conexion
engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

"""AÑADO TABLE AL SQL SERVER CON NOMBRE FEATURESTEST"""
Xdf.to_sql('Features', index=False, con=engine)

print('Funcionó la vuelta!')
#%%
"""FUNCIONANDO FULL EN AZURE NUBE"""
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import numpy as np
import urllib


data=np.load('Features.npy')#cargo matriz de caracteristicas

X=data[:,0:5]
y=data[:,5]
y=y.astype(int)#paso etiquetas a enteros

"""PRIMERO CREO DATAFRAME"""
X=pd.DataFrame(data=X)
y=pd.DataFrame(data=y)
Xdf=pd.concat([X,y], axis=1)
Xdf.columns=['Mu','Va','Skw','kurt','rms','label']

#Esta permite definir los parametros para comunicarse al server
params = urllib.parse.quote_plus(
    'Driver=%s;' % 'ODBC Driver 17 for SQL Server' +
    'Server=tcp:%s,1433;' % 'servidor-sensores1-20201.database.windows.net' +
    'Database=%s;' % 'azurefunction1' +
    'Uid=%s;' % 'server' +
    'Pwd={%s};' % 'Dingo27[' +
    'Encrypt=yes;' +
    'TrustServerCertificate=no;' +
    'Connection Timeout=30;')

#realizo la conexion 
conn_str = 'mssql+pyodbc:///?odbc_connect=' + params
engine_azure = create_engine(conn_str)#creo engine con librería SQLAlchemy para poder subir pandas con metodo to_sql


"""AÑADO TABLE AL SQL SERVER CON NOMBRE FEATURESTEST"""
Xdf.to_sql('Featurestest', index=False, con=engine_azure) 

print('Funcionó la vuelta!')
