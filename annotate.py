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

if "note_id" not in st.session_state:
    get_random_note()

note = notes["text"][st.session_state["note_id"]]
st.button("Pick random note", on_click=get_random_note)

def save_labels(note_id, labels):
    with open(f"data/labels_{note_id}.json", "w") as f:
        json.dump(labels, f)

saved_labels={}
if os.path.exists(f"data/labels_{st.session_state['note_id']}.json"):
    with open(f"data/labels_{st.session_state['note_id']}.json", "r") as f:
        saved_labels = json.load(f)

labels = text_labeler(note, labels=saved_labels)

st.button("Save", on_click=save_labels, 
                  args=(st.session_state["note_id"], labels,))