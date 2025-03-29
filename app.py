import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain


# Load environment variables
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please check your .env file.")
    st.stop()

llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=GOOGLE_API_KEY)

# Predefined URL
FIXED_URL = "https://medium.com/study-guide/career-paths-after-10th-and-12th-standard-30f069541c48"

def get_vectorstore_from_url(url):
    """Fetches website data, splits it into chunks, and creates a vectorstore."""
    try:
        loader = WebBaseLoader(url)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)
        return Chroma.from_documents(
            document_chunks, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )
    except Exception as e:
        st.error(f"Error loading website: {e}")
        return None

def get_context_retriever_chain(vector_store):
    """Creates a retriever chain for fetching relevant context."""
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to retrieve relevant information.")
    ])
    return create_history_aware_retriever(llm, retriever, prompt)

def get_conversational_rag_chain(retriever_chain):
    """Creates a retrieval-augmented generation (RAG) chain."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

def get_response(user_input):
    """Generates a response using Google Gemini."""
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    response = llm.invoke(user_input)
    return response if response else "I'm sorry, I couldn't generate a response."

# Suggested Questions
CATEGORY_QUESTIONS = {
    "Engineering & Technology": ["What are the best engineering fields for the future?", "Is AI engineering a good career?"],
    "Medical & Healthcare": ["Which medical careers don't require NEET?", "What are the top paramedical courses?"],
    "Business & Management": ["What career options exist in finance?", "Is an MBA worth it in 2025?"],
    "Arts & Humanities": ["How to build a career in journalism?", "What are the best career options in humanities?"],
    "Government & Civil Services": ["How to join the Indian Army after 12th?", "What are the best government exams after 12th?"]
}

st.set_page_config(page_title="EduLLM-PERSONALISED EDUCATION PATHWAYS AND CURRICULUM GUIDANCE", page_icon="📚", layout="wide")

with st.sidebar:
    st.title("📌 Project Details")
    st.write("🚀 **EduLLM** is a smart education assistant designed to provide **personalized career guidance** and **curriculum recommendations**.")



    st.write("### 👩‍💻 **Developers**")
    st.write("- **Aayushi Sharma**")

    st.write("### 🔗 **Useful Links**")
    st.markdown("[📖 Visit Source Website](https://medium.com/study-guide/career-paths-after-10th-and-12th-standard-30f069541c48)", unsafe_allow_html=True)
    ##st.markdown("[📩 Contact Support](mailto:navyamehta.tech@gmail.com)", unsafe_allow_html=True)

st.title("📚 EduLLM - PERSONALISED EDUCATION PATHWAYS AND CURRICULUM GUIDANCE")



# Technical Overview Section
st.subheader("🛠️ Technical Overview")
st.write(
    "EduLLM is powered by Google's Gemini AI (gemini-1.5-flash-latest), utilizing LangChain for conversational memory and document retrieval. "
    "It employs retrieval-augmented generation (RAG) with a vector database (ChromaDB) and embeddings from Hugging Face to ensure accurate responses. "
    "The chatbot fetches career-related content from the web via WebBaseLoader, processes it with a context-aware retriever, and provides insightful answers in real-time. "
)


if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vectorstore_from_url(FIXED_URL)

career_category = st.selectbox("Choose a Career Category:", list(CATEGORY_QUESTIONS.keys()))

if career_category:
    st.subheader(f"Suggested Questions for {career_category}")
    for question in CATEGORY_QUESTIONS[career_category]:
        if st.button(question):
            user_query = question
            response = get_response(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))

if st.session_state.vector_store:
    if "chat_history" not in st.session_state:
          st.session_state.chat_history = [AIMessage(content="Hello! I am EduLLM, your personalized education assistant. Ask me anything about career paths, courses, and curriculum guidance! 💡")]

    user_query = st.chat_input("Ask me a question about the content...")
    if user_query:
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(f"""{message.content}""")
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(f"""{message.content}""")
