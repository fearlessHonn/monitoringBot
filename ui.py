import streamlit as st
from search import search


articles = search(end_date=st.date_input('Enddatum'))
categories = {(a.category, b.category) for a, b in zip(articles, [c.german_version for c in articles])}


st.title('EWBot für die EWBerichtserstattung')

load = st.checkbox('Vollständige Artikel laden')


with st.sidebar:
    language = st.radio('Sprache der Artikel', ('englisch', 'deutsch'))
    st.subheader('Kategorien')
    if language == 'englisch':
        checkboxes = {c[0]: st.checkbox(c[0], value=True) for c in categories}
    elif language == 'deutsch':
        checkboxes = {c[0]: st.checkbox(c[1], value=True) for c in categories}

for article in articles:
    if checkboxes[article.category]:
        article = article.german_version if language == 'german' else article

        st.markdown(article.to_html(), unsafe_allow_html=True)
        if load:
            with st.expander('Vollständigen Artikel lesen'):
                st.markdown(article.full_article, unsafe_allow_html=True)
