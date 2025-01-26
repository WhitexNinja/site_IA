#Deploy da Aplicação

#imports
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

#Função para carregar o dataset
def get_data():
    return pd.read_csv('data.csv')

#Função para treinar o modelo
def train_model():
    data = get_data()
    x = data.drop('MEDV', axis=1)
    y = data['MEDV']
    rf_regressor = RandomForestRegressor()

    rf_regressor.fit(x,y)
    return rf_regressor

#Criando dataframe
data = get_data()

#Treinando o modelo
model = train_model()

#Título
st.title("Data App - Prevendo valores de imóveis")

#Subtítulo
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning para o problema de predição de valores de imóveis com o dataset Boston House Prices do MIT.")

#Verificando o dataset
st.subheader("Selecionando apenas um pequeno conjunto de atributos")

#Atributos para serem exibidos por padrão
defaultcols = ['RM','PTRATIO','CRIM','MEDV']

#Definindo atrivutos a partirt do multiselect
cols = st.multiselect('Atributos', data.columns.tolist(), default=defaultcols)

#Exibindo os top 10 registros
st.dataframe(data[cols].head(10))
st.subheader('Distribuição de imóveis por preço')

#Definindo a faixa de valores
faixa_valores = st.slider('Faixa de preço', float(data.MEDV.min()), 150., (10.0, 100.0))

#Filtrando os dados
dados = data[data['MEDV'].between(left=faixa_valores[0], right=faixa_valores[1])]

#Plot da distribuição dos dados
f = px.histogram(dados, x='MEDV', nbins=100, title='Distribuição de Preços')
f.update_xaxes(title='MEDV')
f.update_yaxes(title='Total imóveis')
st.plotly_chart(f)
st.sidebar.subheader('Defina os atributos dos imóveis para predição')

#Mapeando dados do usuario para cada atributo
crim = st.sidebar.number_input('Taxa de criminalidade', value=data.CRIM.mean())
indus = st.sidebar.number_input("Proporção de hectares de Indústrias", value=data.INDUS.mean())
chas = st.sidebar.selectbox('Faz limite com o rio?', ('Sim', 'Não'))

#Transformando o dado de entrada em binário
chas = 1 if chas == "Sim" else 0
nox = st.sidebar.number_input('Concentração de óxido nítrico', value=data.NOX.mean())
rm = st.sidebar.number_input('Número de quartos', value=1)
pratio = st.sidebar.number_input('Índice de alunos por professores', value=data.PTRATIO.mean())

#Botão de predição
btn_predict = st.sidebar.button('Realizar predição')

#Verificando se o botão foi acionado
if btn_predict:
    result = model.predict([[crim, indus, chas, nox, rm, pratio]])
    st.subheader('O valor previsto para o imóvel é: ')
    result = 'US $ '+str(round(result[0]*10,2))
    st.write(result)
#MEDV