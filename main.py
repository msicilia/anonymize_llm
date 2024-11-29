import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import random
import json
import os
from streamlit_annotation_tools import text_labeler

st.set_page_config(layout="wide")

@st.cache_data
def load_notes():
    return pd.read_csv("data/examples.csv", sep="|", quotechar="'")

def get_random_note():
    st.session_state["note_id"] = random.randint(0, notes.shape[0] - 1)

notes = load_notes()
notes["text"] = notes["text"].str.replace("\n", " ")  # Texto uniforme haciendo que todo el texto aparezca en una sola línea por fila

if "note_id" not in st.session_state:
    get_random_note()

note = notes["text"][st.session_state["note_id"]]

st.button("Pick random note", on_click=get_random_note)

MODEL_NAMES = ("llama3.1", "llama2", "meditron")
left, right = st.columns(2)
with left:
    llm = st.selectbox("LLM Model", MODEL_NAMES)
with right:
    temp = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1)

llm = ChatOllama(
    model=llm,
    temperature=temp,
)

# Prompt para anonimizar
# prompt_anonymise = ChatPromptTemplate([
#     ("system", "La siguiente es una nota clínica de un paciente de reumatología: \n {text} \n"),
#     ("user", "Reescribe la nota clínica cambiando los datos anónimos como nombres, fechas o ubicaciones por otros" \
#       " diferentes, para preservar la privacidad de los datos del paciente.")
# ])

prompt_anonymise = ChatPromptTemplate([
    ("system", "La siguiente es una nota clínica de un paciente de reumatología: \n {text} \n"),
    ("user", "Reescribe la nota clínica cambiando únicamente los datos incluidos en {labels} por otros" \
     " diferentes para preservar la privacidad de los datos del paciente, manteniendo el resto de la nota original.")
])

def save_labels(note_id, labels):
    with open(f"data/labels_{note_id}.json", "w", encoding="utf-8") as f: # encoding="utf-8": Especificar codificación UTF-8
        json.dump(labels, f, ensure_ascii=False) # ensure_ascii=False: Deshabilitar codificación automática a Unicode

saved_labels = {}
if os.path.exists(f"data/labels_{st.session_state['note_id']}.json"):
    with open(f"data/labels_{st.session_state['note_id']}.json", "r", encoding="utf-8") as f: # encoding="utf-8": Especificar codificación UTF-8
        saved_labels = json.load(f)

st.write("### Nota original")
labels = text_labeler(note, labels=saved_labels, in_snake_case=False)
print(labels)

st.button("Save Annotations", on_click=save_labels, 
          args=(st.session_state["note_id"], labels,))

st.write("### Nota anonimizada")
chain = prompt_anonymise | llm
note_anon = chain.invoke({"text": note, "labels": labels}).content
st.write(note_anon)
