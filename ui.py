import streamlit as st
from search import search
from httpcore._exceptions import ReadError


articles = search(end_date=st.date_input('Enddatum'))

try:
    categories = {(a.category, b.category) for a, b in zip(articles, [c.german_version for c in articles])}
except ReadError:
    st.error('Es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.')
    quit()


st.title('EWBot für die EWBerichtserstattung')
st.markdown('<a href="https://ewbkarlsruhe.sharepoint.com/sites/haiti-teamorder/_layouts/15/Doc.aspx?sourcedoc={6f989814-dbf5-46bd-96c7-d55795fe6b41}&action=edit&wd=target%28News.one%7C18eaa96c-23d1-426b-88f0-1689d9042f7f%2FNews-Update%7C973fe869-1c36-9144-8671-63fd5bda7db8%2F%29">One-Note Dokument</a>', unsafe_allow_html=True)

load = st.checkbox('Vollständige Artikel laden')


with st.sidebar:
    language = st.radio('Sprache der Artikel', ('englisch', 'deutsch'))
    st.subheader('Kategorien')
    checkboxes = {}
    if language == 'englisch':
        if checkboxes:
            for cb in checkboxes.values():
                del cb

        checkboxes = {c[0]: st.checkbox(c[0], value=True, key=c[0]) for c in categories}
    elif language == 'deutsch':
        if checkboxes:
            for cb in checkboxes.values():
                del cb

        checkboxes = {c[0]: st.checkbox(c[1], value=True, key=c[1]) for c in categories}

for article in articles:
    if checkboxes[article.category]:
        article = article.german_version if language == 'deutsch' else article

        col1, col2 = st.columns((10, 1))
        col1.markdown(article.to_html(), unsafe_allow_html=True)
        if load:
            with col1.expander('Vollständigen Artikel lesen'):
                col1.markdown(article.full_article, unsafe_allow_html=True)


