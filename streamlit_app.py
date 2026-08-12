# Custom Smoothie Order Form Streamlit app
# Co-authored with CoCo
# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests
import pandas
# Write directly to the app

cnx= st.connection("snowflake")

session = cnx.session()
                    

st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Choose Fruits You want in your Custom Drink
  """
)

name_of_order= st.text_input("Name On Smoothie")

st.write("The name on your smoothie will be", name_of_order)


my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()           
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list=st.multiselect(
    'Choose upto 5 diffrent ingredients:'
    , my_dataframe
    , max_selections=5
)



if ingredient_list:
    
    ingredient_string = ''

    for fruit_chosen in ingredient_list:
        ingredient_string=ingredient_string + fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredient_string + """','""" +name_of_order+ """')"""

    

    time_to_insert = st.button('Submit Order')
    st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_of_order + '!', icon="✅")


  


