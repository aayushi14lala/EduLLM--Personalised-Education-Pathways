# EduLLM--Personalised-Education-Pathways

EduLLM is powered by Google's Gemini AI (gemini-1.5-flash-latest), utilizing LangChain for conversational memory and document retrieval.
It employs retrieval-augmented generation (RAG) with a vector database (ChromaDB) and embeddings from Hugging Face to ensure accurate responses.
The chatbot fetches career-related content from the web via WebBaseLoader, processes it with a context-aware retriever, and provides insightful answers in real-time. \n

Key Technologies & Libraries
 🔹 Google Gemini (PaLM LLM) → Generates intelligent responses.\n
 🔹 LangChain → Manages retrieval & response generation pipeline.\n
 🔹 Hugging Face Sentence Transformers → Converts text into dense embeddings.\n
 🔹 ChromaDB → Stores & retrieves vectorized content for fast search.\n
 🔹 Streamlit → Provides an interactive user interface for real-time conversations.

 <img width="959" alt="Screenshot 2025-03-29 111150" src="https://github.com/user-attachments/assets/572d76ba-2822-460e-81a4-059c10618bf6" />\n
How to deploy?\n
Download the zip file\n
Create virtual environment\n
python -m venv venv\n
Activate virtual environment\n
.\venv\Scripts\Activate\n
Install requirements\n
pip install -r requirements.txt\n
Run streamlit\n
streamlit run app.py\n
