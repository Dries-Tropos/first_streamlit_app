import snowflake.connector
import streamlit
import requests
from urllib.error import URLError
import pandas

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized  

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocade Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruity_function_result = get_fruityvice_data(fruity_choice)
    streamlit.dataframe(fruity_function_result)
except URLError as e:
  streamlit.error()

streamlit.text("The fruit load list contains:")

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

if streamlit.butten('Get Fruit Load List'):
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_Cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('" + new_fruit + "')")
    return "Thanks for adding " + add_my_fruit

add_my_fruit = streamlit.text_input("What fruit would you like to add?", "jackfruit")
if streamlit.button('Add a Fruit to the List'):
  fruit_from_func = insert_row_snowflake(add_my_fruit)
  streamlit.text(fruit_from_func)
