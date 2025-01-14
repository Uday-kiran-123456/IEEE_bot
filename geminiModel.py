import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai

class model:
    def __init__(self) -> None:
        load_dotenv()
        genai.configure(api_key='AIzaSyCcmp2DrcnVpp-2z4ng-PfPGjU0jcq9wD8')
        raw_text = self.get_text(r'data2.txt')
        if not os.path.exists("faiss_index"):
            text_chunks = self.get_text_chunks(raw_text)
            self.get_vector_store(text_chunks)

    def process(self, text):
        return self.user_input(text)

    def user_input(self, user_question):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        index_path = "faiss_index"
        try:
            new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(user_question)

            if docs:
                chain = self.get_conversational_chain()
                response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
                if "answer is not available in the context" in response["output_text"].lower():
                    if os.getenv("GOOGLE_API_KEY"):
                        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_question)
                    return response.text
                else:
                    return response["output_text"]
            else:
                general_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
                general_response = general_model(user_question=user_question)
                return general_response

        except Exception as e:
            print(f"Error processing user input: {e}")
            return 'There was an error processing your request. Please try again later.'

    def get_text(self, file_path):
        text = ""
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    def get_text_chunks(self, text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks

    def get_vector_store(self, text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        index_path = "faiss_index"
        try:
            vector_store.save_local(index_path)
        except Exception as e:
            print(f"Error saving FAISS index: {e}")

    def get_conversational_chain(self):
        prompt_template = """
        Answer the question as short as possible from the provided context, make sure to provide all the details. 
        If the answer is not in the provided context, and if the context refers to daily routine or wishes, give the output; 
        otherwise, say "answer is not available in the context". Do not provide a wrong answer.

        Context:\n {context}\n
        Question: {question}\n

        Answer:
        """

        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain
