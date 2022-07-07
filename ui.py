import streamlit as st
from search import search
from translate import translate


st.navbar()

st.title('EWBot für die EWBerichtserstattung')

do_translation = False
do_translation = st.checkbox('Auf deutsch übersetzen')
if not do_translation:
    load = st.checkbox('Vollständige Artikel laden')
    for article in search(end_date=st.date_input('Enddatum')):
        st.markdown(article.to_html(), unsafe_allow_html=True)
        if load:
            with st.expander('Vollständigen Artikel lesen'):
                st.markdown(article.full_article, unsafe_allow_html=True)

else:
    load = st.checkbox('Vollständige Artikel laden')
    for article in search(end_date=st.date_input('Enddatum')):
        st.markdown(article.german_version.to_html(), unsafe_allow_html=True)
        if load:
            with st.expander('Vollständigen Artikel lesen'):
                st.markdown(translate(article.full_article), unsafe_allow_html=True)

