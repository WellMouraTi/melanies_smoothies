# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# ✅ Pega sessão ativa automaticamente no SIS App
session = get_active_session()

# Pega frutas da tabela
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect com ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string}','{name_on_order}')"""

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Seu Smoothie foi pedido!', icon="✅")

# Informações nutricionais
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
