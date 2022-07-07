import streamlit as st

st.title('EWBot')

from main import article_objects

for article_object in article_objects:
    st.write(article_object)
