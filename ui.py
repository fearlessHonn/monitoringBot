import streamlit as st
from search import search
from translation import translate


st.title('EWBot für die EWBerichtserstattung')

load = st.checkbox('Vollständige Artikel laden')

articles = search(end_date=st.date_input('Enddatum'))
categories = {a.category for a in articles}

with st.sidebar:
    language = st.radio('Sprache der Artikel', ('englisch', 'deutsch'))
    st.subheader('Kategorien')
    if language == 'englisch':
        checkboxes = {c: st.checkbox(c, value=True) for c in categories}
    elif language == 'deutsch':
        checkboxes = {c: st.checkbox(translate(c), value=True) for c in categories}

for article in articles:
    if checkboxes[article.category]:
        if language == 'englisch':
            st.markdown(article.to_html(), unsafe_allow_html=True)
            if load:
                with st.expander('Vollständigen Artikel lesen'):
                    st.markdown(article.full_article, unsafe_allow_html=True)

        elif language == 'deutsch':
            st.markdown(article.german_version.to_html(), unsafe_allow_html=True)
            if load:
                with st.expander('Vollständigen Artikel lesen'):
                    st.markdown(translate(article.full_article), unsafe_allow_html=True)


