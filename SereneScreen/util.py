from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import RetrievalQA
import pandas as pd

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import pandas as pd
import logging
import numpy as np


def context_retrieval(filename, query, k=10):
    try:
        
        loader = CSVLoader(file_path=filename, source_column="Summary")
        documents = loader.load()
        print("hello")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings)

        retrieved_docs = db.similarity_search(query, k=k)
        return retrieved_docs
    except Exception as e:
        print("error: ", e)
        raise e

def rag_process(llm_model, retrieved_docs, question):
    try:
        # Initialize LLM
        llm = Ollama(model=llm_model)

        # Generate the final response using the Ollama model directly
        prompt = f"""
        1. Use the following pieces of context to answer the question at the end.
        2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
        3. Keep the answer crisp and limited to 3,4 sentences.

        Context: {retrieved_docs}

        Question: {question}

        Helpful Answer:"""

        response = llm(prompt=prompt)

        return response
    except Exception as e:
        print("Error occurred during rag_process:", e)
        raise e
    
def anxiety_model_processing():
    module_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2'
    data = np.random.rand(5, 3)
    anxiety = np.random.randint(2, size=5)
    
    def tokenize(texts):
        return np.random.randint(0, 500, size=(len(texts), 20))
    
    inputs = tokenize(["labels"] * 5)
    def model_processing(inputs):
        return np.zeros(inputs.shape[0])
    
    predictions = model_processing(inputs)
    return predictions


def loneliness_model_processing():
    module_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2'
    data = np.random.rand(5, 3)
    loneliness = np.random.randint(2, size=5)
    
    def tokenize(texts):
        return np.random.randint(0, 500, size=(len(texts), 20))
    
    inputs = tokenize(["labels"] * 5)
    def model_processing(inputs):
        return np.zeros(inputs.shape[0])
    
    predictions = model_processing(inputs)
    return predictions

def stress_model_processing():
    module_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2'
    data = np.random.rand(5, 3)
    stress = np.random.randint(2, size=5)
    
    def tokenize(texts):
        return np.random.randint(0, 500, size=(len(texts), 20))
    
    inputs = tokenize(["labels"] * 5)
    def model_processing(inputs):
        return np.zeros(inputs.shape[0])
    
    predictions = model_processing(inputs)
    return predictions
