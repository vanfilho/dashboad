import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
data = pd.read_csv("houses_to_rent_v2.csv")

# Configurar layout do app Streamlit para ocupação total da página
st.set_page_config(layout="wide")
st.title("Dashboard de Imóveis para Aluguel")

# Combobox para selecionar a quantidade de quartos
rooms_selected = st.selectbox("Selecione a quantidade de quartos", sorted(data['rooms'].unique()))

# Filtrar os dados pela quantidade de quartos selecionada
filtered_data = data[data['rooms'] == rooms_selected]

# Criar uma estrutura de 3 colunas para exibir a quantidade de imóveis, preço mínimo e preço máximo
col1, col2, col3 = st.columns(3)

# Exibir os dados nas respectivas colunas
with col1:
    total_properties = len(filtered_data)
    st.metric(label="Quantidade de imóveis", value=total_properties)

with col2:
    min_rent = filtered_data['rent amount (R$)'].min()
    st.metric(label="Preço mínimo", value=f"R$ {min_rent}")

with col3:
    max_rent = filtered_data['rent amount (R$)'].max()
    st.metric(label="Preço máximo", value=f"R$ {max_rent}")

# Preço médio por cidade, ordenado em ordem decrescente
avg_price_by_city = filtered_data.groupby('city')['rent amount (R$)'].mean().sort_values(ascending=True)

# Preço médio com e sem mobília
avg_price_furnished = filtered_data[filtered_data['furniture'] == 'furnished']['rent amount (R$)'].mean()
avg_price_not_furnished = filtered_data[filtered_data['furniture'] == 'not furnished']['rent amount (R$)'].mean()

# Gráfico de barras para preço médio por cidade sem eixo x e em ordem decrescente
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), gridspec_kw={'width_ratios': [2, 1]})

# Gráfico de barras horizontal para o preço médio por cidade sem eixo x
ax1.barh(avg_price_by_city.index, avg_price_by_city.values, color='red', edgecolor='none')
ax1.set_title("Preço Médio por Cidade (Ordem Decrescente)")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.tick_params(left=False, bottom=False)  # Remover ticks do eixo x
ax1.set_xticks([])  # Remover valores do eixo x
for i, v in enumerate(avg_price_by_city.values):
    ax1.text(v + 100, i, f'{v:.2f}', va='center', color='black')

# Gráfico de barras para preços médios com e sem mobília sem eixo y e com largura reduzida
ax2.bar(['Com Mobília', 'Sem Mobília'], [avg_price_furnished, avg_price_not_furnished], color=['blue', 'blue'], edgecolor='none')
ax2.set_title("Preço Médio com e sem Mobília")
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.tick_params(left=False, bottom=False)  # Remover ticks do eixo y
ax2.set_yticks([])  # Remover valores do eixo y
for i, v in enumerate([avg_price_furnished, avg_price_not_furnished]):
    ax2.text(i, v + 100, f'{v:.2f}', ha='center', color='black')

# Exibir os gráficos usando a largura total da página
st.pyplot(fig)

# Pegar a cidade com o maior e menor valor
cidade_maior_preco = avg_price_by_city.index[0]
cidade_menor_preco = avg_price_by_city.index[-1]

# Adicionar um ComboBox para selecionar a cidade, já selecionando a cidade com o maior valor
city_selected = st.selectbox("Selecione a cidade", sorted(filtered_data['city'].unique()), index=0)

# Filtrar os imóveis pela cidade selecionada e ordenar por preço decrescente
city_filtered_data = filtered_data[filtered_data['city'] == city_selected].sort_values(by='rent amount (R$)', ascending=False)

# Exibir a lista dos primeiros imóveis da cidade selecionada, sem o índice
st.write(f"Imóveis na cidade de {city_selected} (ordenados por preço de forma decrescente):")
st.dataframe(city_filtered_data[['city', 'rent amount (R$)', 'rooms', 'furniture', 'total (R$)']].head(10), width=1400, height=300,hide_index=True)
