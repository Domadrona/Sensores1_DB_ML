import logging
import azure.functions as func
import pyodbc #permite crear la base de datos.
import pandas as pd
import json #permite intercambio de datos entre la misma red
import uuid #permite crear valor alfanumerico de 12 digitos
import os #permite navegar por carpetas y por otros archivos
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
import numpy as np
import pickle
import joblib

# Definicion de la funcion de traseo de error.
def traceDB(cnxnAzure,uuid,message):
    query = "INSERT INTO [dbo].[logs] ([ID],[Fecha],[Descripcion]) VALUES ('{}',GETDATE(),'{}')".format(uuid,message) #inserta en base valotes de date(servidor) y el mensaje
    cnxnAzure.execute(query) #conexion con DB stand by
    cnxnAzure.commit() #imprime lo de la DB
    return(True)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Seteo de variables globales.') #imprime codigo
    ID = str(uuid.uuid1())
    logging.info(ID)
    driverAzure = os.environ["DriverAzure"]
    serverAzure = os.environ["ServerBdAzure"]
    databaseAzure = os.environ["DataBaseAzure"]
    usernameAzure = os.environ["UserNameBdAzure"]
    passwordAzure = os.environ["PassWordBdAzure"]
    SQL_Featurestest = os.environ["SQL_Featurestest"] #se comunica con el archivo y lo guarda aca
    logging.info(SQL_Featurestest)

    logging.warning('Establece conexión con la base de datos Conectados.') #info, warning,error imprimen en colores
    conStringAzure = "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(driverAzure,serverAzure,databaseAzure,usernameAzure,passwordAzure) #concateno datos en orden
    logging.info(conStringAzure)
    cnxnAzure = pyodbc.connect(conStringAzure) #ahora si nos conectamos a info que pide constring
    logging.info('Conexión establecida con la base de datos Azure.')
    traceDB(cnxnAzure,ID,'Inicio servicio web, por fin.')

    logging.info('Obtiene parámetros del JSON.')
    traceDB(cnxnAzure,ID,'Parámetros del servicio recibidos.')
    req_body = req.get_json()
    variable1 = req_body.get('variable1') #informacion que obtengo por el postman la guardo en la variable1 IMPORTANTE
    logging.info(variable1)

    query = (SQL_Featurestest)
    df_datos = pd.read_sql_query(query,cnxnAzure) #creo pandas, y le guardo lo que lea en query con la conexion de azure--- "SQL_Featuretest": "SELECT * FROM datos"

    #"""PRUEBA DE QUE SIRVE CON DATAFRAME"""###
    datanumpy = df_datos.to_numpy()
    x=datanumpy[:,0:5]
    y=datanumpy[:,5:6]#que bendito problema para indexar las etiquetas
    y=y.astype(int)

    X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size=0.3,random_state=42)

    modelo = SVC(gamma='auto')
    modelo.fit(X_train, Y_train)
    predicciones = modelo.predict(X_test)
    SVM=classification_report(Y_test, predicciones)

    veci = KNeighborsClassifier(n_neighbors=3)
    veci.fit(X_train, Y_train)
    prediccionesKNN = veci.predict(X_test)
    KNN=classification_report(Y_test, prediccionesKNN)

    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    prediccionesNB = clf.predict(X_test)
    NB=classification_report(Y_test, prediccionesNB)

    comparacion=np.hstack((KNN,SVM,NB))
    comparacion_df = pd.DataFrame ([comparacion],columns=['KNN','SVM','NB'])
    diccionario = comparacion_df.to_dict('dict') #convierto porque json pide
    json_response = json.dumps(diccionario,indent=2) #puedo hacer multiples respuestas

    diccionario2 = df_datos.to_dict('dict') #convierto porque json pide
    json_response2 = json.dumps(diccionario2,indent=2) #puedo hacer multiples respuestas
    traceDB(cnxnAzure,ID,'Enviando respuesta, Funcionó.')

    logging.warning('FINALMENTE TODO CORRE Y FUNCIONA')
    logging.warning('AQUI IBA A PONER LO MISMO CON OTRO COLOR jejeje.')


    if variable1 < 10:
        return func.HttpResponse(json_response)
    elif variable1 == 29:
        return func.HttpResponse(json_response2)
    else:
        return func.HttpResponse("LISTO EL POLLO-maybe we should writing in English too. by the way, the postman flawlessly worked",status_code=200)