9import streamlit as st
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

# Streamlitアプリの設定
st.title('PDFパーサー')
st.write('PDFファイル要約')

uploaded_file = st.file_uploader(label="ここにファイルをドラッグ＆ドロップしてください", type=["pdf"])

if uploaded_file is not None:
    text = read_pdf(uploaded_file)
    
    # 読み込んだPDFファイルの文字数を表示
    st.write(f"読み込んだPDFファイルの文字数: {len(text)}文字")
    
    # 要約文字数を指定
    char_count = st.number_input("要約文字数を指定してください", min_value=1, max_value=100000, value=500)
    
    # 要約を実行
    parser = PlaintextParser.from_string(text, Tokenizer('japanese'))
    summarizer = LexRankSummarizer()
    res = summarizer(document=parser.document, sentences_count=1000)  # 大きな値を設定しておく

    # 指定された文字数に要約を調整
    summary = ""
    for sentence in res:
        if len(summary) + len(str(sentence)) <= char_count:
            summary += str(sentence)
        else:
            break

    # フォントサイズを12pxに設定して表示
    st.markdown(f"<div style='font-size: 12px;'>{summary}</div>", unsafe_allow_html=True)
