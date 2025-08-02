# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Título e instruções
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Campo de entrada para o nome do pedido
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Conectar ao Snowflake
cnx = st.connection("snowflake")  # substitua se necessário
session = cnx.session()

# Buscar opções de frutas
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(my_dataframe, use_container_width=True)

# Multiselect para escolher ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Só continua se o usuário preencheu o nome e escolheu ao menos 1 ingrediente
if ingredients_list and name_on_order.strip() != "":
    # Montar a string dos ingredientes
    ingredients_string = ' '.join(ingredients_list)

    # Preparar o insert
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Botão para enviar o pedido
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('✅ Seu Smoothie foi pedido!')
else:
    st.info("Preencha o nome do Smoothie e selecione ao menos 1 ingrediente.")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=true)
