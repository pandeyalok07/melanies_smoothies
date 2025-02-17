# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col    

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """**Choose the fruits you want in your cuatome Smoothie!**"""
)

from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col ('FRUIT_NAME'))
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

cnx = st.connection("snowflake")
session = cnx.session()

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections= 5
)
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    
    st.write(ingredients_string)
        
    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS (ingredients , name_on_order)
        values ('""" + ingredients_string + """', '""" +name_on_order+"""')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")      
    
