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
    
    # 要約行数を指定
    sentences_count = st.number_input("要約行数を指定してください", min_value=1, max_value=100000, value=1000)
    
    # 要約を実行
    parser = PlaintextParser.from_string(text, Tokenizer('japanese'))
    summarizer = LexRankSummarizer()
    res = summarizer(document=parser.document, sentences_count=sentences_count)

    for sentence in res:
        st.write(sentence)
