import streamlit as st

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Conexão com Snowflake
conn = st.connection("snowflake")

# Consulta os ingredientes disponíveis
df = conn.query("SELECT FRUIT_NAME FROM smoothies.public.fruit_options", ttl="10m")

# Lista de seleção
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    df["FRUIT_NAME"].tolist(),
    max_selections=5
)

# Monta string de ingredientes
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

# Botão para enviar pedido
time_to_insert = st.button('Submit Order')

if time_to_insert:
    insert_query = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    conn.query(insert_query, ttl=0)
    st.success('Seu Smoothie foi pedido!', icon="✅")
