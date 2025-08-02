# Importações no topo
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Título e nome
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Escolha as frutas para seu Smoothie personalizado!")

name_on_order = st.text_input('Nome no pedido:')
st.write('Nome no Smoothie:', name_on_order)

# Conexão com Snowflake
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Seleção de ingredientes
ingredients_list = st.multiselect(
    'Escolha até 5 ingredientes:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# Monta a instrução INSERT
my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""

# Botão de enviar pedido
time_to_insert = st.button('Pedir Smoothie')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Seu Smoothie foi pedido!', icon="✅")
