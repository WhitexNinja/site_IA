import pandas as pd

#Carregar a base
link = 'https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/d4332a3056f44e1a1dec9600a31f21c8_boston.csv'
data = pd.read_csv(link)

#Convertendo type da coluna RM
data['RM'] = data['RM'].astype(int)

#Removendo colunas irrelevantes
data = data.drop(columns=['TOWN', 'TRACT', 'LON', 'LAT', 'ZN', 'AGE', 'RAD', 'DIS', 'TAX'])

#Salvando
data.to_csv('data.csv', index=False)