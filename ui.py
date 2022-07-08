import streamlit as st
from search import search
from translation import translate


st.title('EWBot für die EWBerichtserstattung')

do_translation = st.checkbox('Auf deutsch übersetzen')
load = st.checkbox('Vollständige Artikel laden')

articles = search(end_date=st.date_input('Enddatum'))
categories = {a.category for a in articles}

with st.sidebar:
    st.header('Kategorien')
    if not do_translation:
        checkboxes = {c: st.checkbox(c, value=True) for c in categories}
    else:
        checkboxes = {c: st.checkbox(translate(c), value=True) for c in categories}

for article in articles:
    if checkboxes[article.category]:
        if not do_translation:
            st.markdown(article.to_html(), unsafe_allow_html=True)
            if load:
                with st.expander('Vollständigen Artikel lesen'):
                    st.markdown(article.full_article, unsafe_allow_html=True)

        else:
            st.markdown(article.german_version.to_html(), unsafe_allow_html=True)
            if load:
                with st.expander('Vollständigen Artikel lesen'):
                    st.markdown(translate(article.full_article), unsafe_allow_html=True)


