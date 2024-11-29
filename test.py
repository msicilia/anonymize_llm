import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import random

st.set_page_config(layout="wide")

@st.cache_data
def load_notes():
    return pd.read_csv("data/examples.csv", sep="|", quotechar="'")


notes = load_notes()
note_idx = st.button("Pick random note", )
note_idx = random.randint(0, notes.shape[0]-1) 
note = notes["text"][note_idx]

MODEL_NAMES = ("llama3.1", "llama2", "meditron")

left, right = st.columns(2)
with left:
    llm = st.selectbox(
        "LLM Model", 
        MODEL_NAMES, 
    )
with right:
    temp = st.slider(
        "Temperature", 
        0.0, 1.0, 0.4, 0.1,
    )

llm = ChatOllama(
    model=llm,
    temperature=temp,
)

prompt_anonymise = ChatPromptTemplate([
    ("system", "La siguiente es una nota clínica de un paciente de reumatología: \n {text} \n"),
    ("user", "Reescribe la nota clínica cambiado los datos anónimos como nombres, fechas o ubicaciones por otros" \
      "diferentes, para preservar la privacidad de los datos del paciente.")
])

left, right = st.columns(2)
with left:
    st.write(note)
with right:
    chain = prompt_anonymise | llm
    note_anon = chain.invoke({"text": note}).content
    st.write(note_anon)
