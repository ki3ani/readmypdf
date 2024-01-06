from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback

load_dotenv()

app = Flask(__name__)

@app.route('/api/process_pdf', methods=['POST'])
def process_pdf():
    pdf_file = request.files.get('pdf')
    if pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )  

        chunks = text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        question = request.form.get('question')
        if question:
            docs = knowledge_base.similarity_search(question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=question)

            return jsonify({'response': response})

    return jsonify({'error': 'Invalid PDF file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
