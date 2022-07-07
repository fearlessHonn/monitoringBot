import streamlit as st
from search import search


st.title('EWBot')


for article in search(end_date=st.date_input('End date'), translate=st.checkbox('Translate to german')):
    st.markdown(article.to_html(), unsafe_allow_html=True)
