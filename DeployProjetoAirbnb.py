#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import streamlit as st
import joblib


x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'Ano': 0, 'Mes': 0, 'numero_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Other', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

diccionario={}
for item in x_listas:
    for valor in x_listas[item]:
        diccionario[f'{item}_{valor}'] = 0        

for item in x_numericos:
    if item=='latitude' or item=='longitude':
        valor=st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
    elif item=='extra_people':
        valor=st.number_input(f'{item}', step=0.01, value=0.0)
    else:
        valor=st.number_input(f'{item}', step=1, value=0)
    x_numericos[item]=valor
        
for item in x_tf:
    valor=st.selectbox(f'{item}', ('Sim','Não'))
    if valor=='Sim': 
        x_tf[item]=1
    else:
        x_tf[item]=0
        
for item in x_listas:
    valor=st.selectbox(f'{item}', x_listas[item])
    diccionario[f'{item}_{valor}'] = 1

boton=st.button('Prever valor do Imóvel')

if boton:
    diccionario.update(x_numericos)
    diccionario.update(x_tf)
    valores_x=pd.DataFrame(diccionario, index=[0])
    
    #a la hora de hacer mi deploy, cuando voy a pasarle las informaciones al modelo para q haga la prediccion, tienen que estar en el mismo orden en como el modelo fue entrenado
    datos=pd.read_csv('dados.csv')
    datos=datos.drop('Unnamed: 0', axis=1)
    datos=datos.drop('price', axis=1)
    
    columnas=list(datos.columns)
                
    valores_x=valores_x[columnas]
    modelo=joblib.load('modelo.joblib')
    precio=modelo.predict(valores_x)
    st.write(precio[0])

