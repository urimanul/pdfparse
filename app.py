import streamlit as st
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from io import BytesIO

def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

uploaded_file = st.file_uploader("PDFファイルを選択してください", type=["pdf"])

if uploaded_file is not None:
    text = read_pdf(uploaded_file)
    
    # 2000行要約をする（sentences_count=2000なので、2000行）
    parser = PlaintextParser.from_string(text, Tokenizer('japanese'))
    summarizer = LexRankSummarizer()
    res = summarizer(document=parser.document, sentences_count=2000)

    for sentence in res:
        st.write(sentence)
