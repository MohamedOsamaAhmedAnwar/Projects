import streamlit as st 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk
nltk.download('punkt_tab')

def summarize(text,summarizer_type="lsa",sentence_count=5):
    parser=PlaintextParser.from_string(text,Tokenizer("arabic"))
    if summarizer_type=="lsa":
        summarizer=LsaSummarizer()
    elif summarizer_type=="luhn":
        summarizer=LuhnSummarizer()
    elif summarizer_type=="lexrank":
        summarizer=LexRankSummarizer()
    elif summarizer_type=="textrank":
        summarizer=TextRankSummarizer()
    else:
        st.error("Please enter a valid name for summarizer")
    summary=summarizer(parser.document,sentence_count)
    return " ".join(str(sentence) for sentence in summary)
st.title("Text Summarization")
text=st.text_area("Please enter some text")
summarizer_type=st.selectbox("Choose Summarizer",("lsa","luhn","lexrank","textrank"))
sentence_count=st.slider("Number of Sentences",1,10,4)

if st.button("Summarize"):
    if text:
        summary=summarize(text,summarizer_type,sentence_count)
        st.subheader("Summary")
        st.write(summary)