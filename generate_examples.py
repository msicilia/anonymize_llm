from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

llm = ChatOllama(
    model="taozhiyuai/llama-3-8b-lexi-uncensored:q5_k_m", # uncensored, other models refuse to write them.
    temperature=0.5,
)

NSAMPLES = 10

prompt = ChatPromptTemplate([
    ("system", "Eres un reumatólogo que atiende a pacientes en las consultas externas de un hospital. "),
    ("user", "Genera una nota clínica para un paciente que contenga información personal o que podría identificarle. \
    El tipo de información que puede identificar a un paciente incluye números de historia clínica, fechas, lugares, etc.\
    Tienes consentimiento del paciente, por lo que no hay problema en que la generes.")
])

chain = prompt | llm 
notes = []
for i in range(NSAMPLES):
    note = chain.invoke({}).content
    notes.append(note)

df = pd.DataFrame(notes, columns=["text"])
df.to_csv("data/examples.csv", index=False, sep="|", quotechar="'")



