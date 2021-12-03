"""
Algoritmo para análisis de las acciones de Google en un periodo determinado. El archivo usado en este caso corresponde
al período de enero de 2017 a diciembre de 2021.
Se visualiza símbolo verde cuando conviene comprar y rojo cuando conviene vender.

Matias Horst
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Defino la función para obtener las listas de los precios de compra y venta
def senial(data):
    compra = []
    venta = []
    condicion = 0

    for dia in range(len(data)):
        if data['MMS30'][dia] > data['MMS100'][dia]:
            if condicion != 1:
                compra.append(data['Google'][dia])
                venta.append(np.nan)
                condicion = 1
            else:
                compra.append(np.nan)
                venta.append(np.nan)

        elif data['MMS30'][dia] < data['MMS100'][dia]:
            if condicion != 2:
                compra.append(np.nan)
                venta.append(data['Google'][dia])
                condicion = 2
            else:
                compra.append(np.nan)
                venta.append(np.nan)
        else:
            compra.append(np.nan)
            venta.append(np.nan)

    return (compra, venta)




def main():
    # Primero se carga el archivo obtenido de Yahoo Finance con los datos de las acciones
    datos = pd.read_csv('GOOG.csv')
    print('\nPrimeros datos del archivo:')
    print(datos.head())

    # Calculo de la Media Móvil Simple 30 dias
    MMS30 = pd.DataFrame()
    MMS30['Close'] = datos['Close'].rolling(window = 30).mean()
    print('\nMedia Móvil simple primeros 30 días:  ')
    print(MMS30[MMS30.index == 29])

    # Calculo de la Media Móvil Simple 100 dias
    MMS100 = pd.DataFrame()
    MMS100['Close'] = datos['Close'].rolling(window = 100).mean()
    print('\nMedia Móvil simple primeros 100 días:  ')
    print(MMS100[MMS100.index == 99])

# Algoritmo para detectar cuando la MVS30 es superior a la MVS100, y por ende conviene comprar, caso contrario conviene
# vender

    data = pd.DataFrame()
    data['Google'] = datos['Close']
    data['MMS30'] = MMS30['Close']
    data['MMS100'] = MMS100['Close']

    seniales = senial(data)
    data['Compra'] = seniales[0]
    data['Venta'] = seniales[1]

    # Graficamos
    plt.figure(figsize=(15, 8))
    # Datos de los valores de precio de cierre de cada dia
    plt.plot(datos['Close'], label='Google', alpha=0.5)
    # Valores de la media móvil con período de 30 días
    plt.plot(MMS30['Close'], label='Media móvil 30', alpha=0.5)
    # Valores de la media móvil con período de 100 días
    plt.plot(MMS100['Close'], label='Media móvil 100', alpha=0.5)
    # Precios en los que conviene comprar
    plt.scatter(data.index, data['Compra'], label='Precio de Compra', marker='^', color='green')
    # Precios en los que conviene vender
    plt.scatter(data.index, data['Venta'], label='Precio de Venta', marker='v', color='red')

    plt.title('Google Precio de las acciones - Período 2017/2021')
    plt.xlabel('1 Ene. 2017 - 3 Dic. 2021')
    plt.ylabel('Precio de cierre [U$S]')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()
