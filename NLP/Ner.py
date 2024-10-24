import streamlit as st
import spacy
from spacy import displacy

NLP = spacy.load("en_core_web_sm")

def extract(text):
    doc = NLP(text)
    entities = [(ent.text ,ent.label_) for ent in doc.ents]
    return entities

def show_ner(doc):
    html = displacy.render(doc,style ="ent",jupyter = False )
    return html 

st.title ("Text Extraction using spacy")
st.write ("please enter some text")
text = st.text_area("please enter text to extract entities")

if st.button("extract"):
    if text:
        doc = NLP(text)
        entities = extract(text)
       # st.write(entities)
        st.subheader("Extracted Entities")
        st.markdown(show_ner(doc),unsafe_allow_html=True)
