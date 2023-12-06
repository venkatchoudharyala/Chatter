import streamlit as st
import json

st.set_page_config(initial_sidebar_state = "collapsed")

hide_st_style = """
		<style>
		header {visibility: hidden;}
		footer {visibility: hidden;}
  		</style>
  		"""

st.markdown(hide_st_style, unsafe_allow_html = True)

def main():
  Form = st.form("Login")
  UserAcc = Form.text_input("User Name")
  Path = "UserAcc/" + UserName.strip() + ".ua"
  try:
    with open(UserPath, "r") as File:
      UDetails = File.read()
      Details = json.loads(UDetails)
      st.write(Details)
  except FileNotFoundError:
    st.write("User Not Found")

if __name__ == "__main__":
  main()
