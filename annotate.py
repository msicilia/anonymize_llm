import streamlit as st
import random
import pandas as pd
from streamlit_annotation_tools import text_labeler
import json
import os

st.set_page_config(layout="wide")

@st.cache_data
def load_notes():
    return pd.read_csv("data/examples.csv", sep="|", quotechar="'")

def get_random_note():
    st.session_state["note_id"]= random.randint(0, notes.shape[0]-1) 

notes = load_notes()
notes["text"] = notes["text"].str.replace("\n", " ") # Texto uniforme haciendo que todo el texto aparezca en una sola línea por fila

if "note_id" not in st.session_state:
    get_random_note()

note = notes["text"][st.session_state["note_id"]]
st.button("Pick random note", on_click=get_random_note)

def save_labels(note_id, labels):
    with open(f"data/labels_{note_id}.json", "w", encoding="utf-8") as f: # encoding="utf-8": Especificae codificación UTF-8
        json.dump(labels, f, ensure_ascii=False) # encoding="utf-8": Deshabilitar codificación automática a Unicode

saved_labels={}
if os.path.exists(f"data/labels_{st.session_state['note_id']}.json"):
    with open(f"data/labels_{st.session_state['note_id']}.json", "r", encoding="utf-8") as f: # encoding="utf-8": Especificae codificación UTF-8
        saved_labels = json.load(f)

labels = text_labeler(note, labels=saved_labels, in_snake_case=False)

st.button("Save", on_click=save_labels, 
                  args=(st.session_state["note_id"], labels,))