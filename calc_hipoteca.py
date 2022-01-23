# Calculadora de Pagos y Amortización Hipotecaria

import csv, math, decimal, copy, pandas as pd, numpy as np


def main():
    monto = decimal.Decimal(input('Ingresa el valor de la propiedad: '))
    años = int(input('Ingresa la cantidad de años de la Hipoteca: '))
    tasa = decimal.Decimal(input('Ingresa la tasa de interes (sin signo de porcentaje): ')) / 100
    pago_mensual = pagos(monto, tasa, años)
    tabla_amortizacion = []
    
    for mes in range(años * 12):

        # Monto Inicial
        if mes == 0:
            monto_inicial = monto
        else:
            monto_inicial = monto_final


        año = math.floor(mes / 12)
        ints_mes = (tasa/12) * monto_inicial # Pago mensual de intereses
        cap_mes = pago_mensual - ints_mes # Pago mensual de capital
        monto_final = monto_inicial - cap_mes # Monto final del mes

        # Incluye la data del mes
        tabla_amortizacion.append([año, mes, monto_inicial, pago_mensual, ints_mes, cap_mes, monto_final])

    # Pandas para agrupar la tabla de amortización de forma anual
    np_array = np.array(tabla_amortizacion)
    data = pd.DataFrame(data=np_array, columns=['año', 'mes', 'monto_inicial', 'pago', 'intereses', 'capital', 'monto_final'])

    # Agrupar columnas individuales a través de "Series" y 
    # contatenar en un nuevo Dataframe
    monto_inicial_anual = data.groupby('año')['monto_inicial'].max()
    pago_anual = data.groupby('año')['pago'].sum()
    intereses_anual = data.groupby('año')['intereses'].sum()
    capital_anual = data.groupby('año')['capital'].sum()
    monto_final_anual = data.groupby('año')['monto_final'].min()

    df = pd.concat([monto_inicial_anual, pago_anual, intereses_anual, capital_anual, monto_final_anual], axis=1).reset_index()
    pago_total = df['pago'].sum()
    capital_total = df['capital'].sum()
    intereses_total = df['intereses'].sum()

    print(
        '-' * 40,
        f'Mensualidad => {pago_mensual:,.2f}',
        f'Pago total, acumulado al año #{años} => {pago_total:,.2f}', 
        f'Pago de capital, acumulado al año #{años} => {capital_total:,.2f}', 
        f'Pago de intereses, acumulado al año #{años} => {intereses_total:,.2f}',
        sep='\n'
    )


    # Exportar el Dataframe a CSV usando Pandas
    df.to_csv('amortizacion_anual_pandas.csv', index=False)
    print('-' * 40, 'Tabla de amortización anual exportada en CSV desde Pandas', sep='\n')

    # Exportar el Dataframe a CSV usando el módulo CSV
    df_list = df.values.tolist()

    
    for i, lista in enumerate(copy.deepcopy(df_list)):
        for j, item in enumerate(lista):
            # Convertir los numeros de Decimal a Float
            df_list[i][j] = round(float(df_list[i][j]), 2)

    with open('amortizacion_anual_csv.csv', mode='x', newline='') as f:
        writer = csv.writer(f)
        for fila in df_list:
            writer.writerow(fila)
    
    print('-' * 40, 'Tabla de amortización anual exportada en CSV desde modulo CSV', sep='\n')

    
def pagos(monto:decimal.Decimal, tasa:decimal.Decimal, años:int) -> decimal.Decimal:
    """
    Calcula el pago mensual de un préstamo, dado el valor
    total del préstamo, la tasa y cantidad de años a pagar.
    
    P = (Pv*R) / [1 - (1 + R)^(-n) donde:

    P = Pago Mensual \n
    Pv = Valor del préstamo \n
    APR = Tasa de interés anual \n
    R = Tasa de interés mensual = APR/meses del año \n
    n = Total de meses en la vida del préstamo (12 meses * número de años)
    """

    return (monto * tasa/12) / (1 - ((1 + (tasa/12))**(-1 * años * 12)))


if __name__ == '__main__':
    main()