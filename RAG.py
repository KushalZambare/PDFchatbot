from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages import get_buffer_string
from langchain_core.prompts import format_document
from langchain.prompts.prompt import PromptTemplate
from operator import itemgetter
import ollama
from tqdm import tqdm
import argparse
import sys
import os
from typing import List

# Global constants
TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Prompts
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """
    Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.

    Chat History:
    {chat_history}

    Follow-Up Input: {question}
    Standalone question:"""
)

ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """
    ### Instruction:
    You're a helpful research assistant, who answers questions based on provided research in a clear way and easy-to-understand way.
    If there is no research, or the research is irrelevant to answering the question, simply reply that you can't answer.
    Please reply with just the detailed answer and your sources. If you're unable to answer the question, do not list sources.

    ## Research:
    {context}

    ## Question:
    {question}
    """
)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="Source Document: {source}, Page {page}:\n{page_content}"
)

# Helper Functions
def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def __pull_model(name: str) -> None:
    current_digest, bars = "", {}
    for progress in ollama.pull(name, stream=True):
        digest = progress.get("digest", "")
        if digest != current_digest and current_digest in bars:
            bars[current_digest].close()

        if not digest:
            print(progress.get("status"))
            continue

        if digest not in bars and (total := progress.get("total")):
            bars[digest] = tqdm(
                total=total, desc=f"Pulling {digest[7:19]}", unit="B", unit_scale=True
            )

        if completed := progress.get("completed"):
            bars[digest].update(completed - bars[digest].n)

        current_digest = digest


def __is_model_available_locally(model_name: str) -> bool:
    try:
        ollama.show(model_name)
        return True
    except ollama.ResponseError:
        return False


def get_list_of_models() -> List[str]:
    """Retrieves a list of available models from the Ollama repository."""
    return [model["name"] for model in ollama.list()["models"]]


def check_if_model_is_available(model_name: str) -> None:
    """Ensures that the specified model is available locally."""
    try:
        available = __is_model_available_locally(model_name)
    except Exception:
        raise Exception("Unable to communicate with the Ollama service")

    if not available:
        try:
            __pull_model(model_name)
        except Exception:
            raise Exception(
                f"Unable to find model '{model_name}', please check the name and try again."
            )


def load_documents_and_prompt_user(documents_path: str) -> List[Document]:
    """Loads documents from the specified directory and prompts the user to select which ones to use."""
    if not os.path.exists(documents_path):
        raise FileNotFoundError(f"The specified path does not exist: {documents_path}")

    loaders = {
        ".pdf": DirectoryLoader(
            documents_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,
            use_multithreading=True,
        ),
        ".md": DirectoryLoader(
            documents_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
        ),
    }

    raw_documents = []
    for loader in loaders.values():
        raw_documents.extend(loader.load())

    # Display the list of loaded documents to the user
    print("\nAvailable Documents:")
    document_options = [f"{i + 1}: {doc.metadata['source']}" for i, doc in enumerate(raw_documents)]
    print("\n".join(document_options))

    # Prompt the user to select documents by their indices
    while True:
        try:
            selected_indices = input(
                "\nEnter the numbers of the documents you want to include (comma-separated): "
            )
            selected_indices = list(map(int, selected_indices.split(",")))
            if all(1 <= idx <= len(raw_documents) for idx in selected_indices):
                break
            else:
                print("Invalid selection. Please choose valid document numbers.")
        except ValueError:
            print("Invalid input. Please enter comma-separated numbers.")

    # Filter the selected documents
    selected_documents = [raw_documents[idx - 1] for idx in selected_indices]
    print("\nSelected Documents:")
    for doc in selected_documents:
        print(f"- {doc.metadata['source']}")

    return selected_documents


def load_documents_into_database(model_name: str, documents_path: str) -> Chroma:
    """Loads selected documents from the specified directory into the Chroma database."""
    selected_documents = load_documents_and_prompt_user(documents_path)
    documents = TEXT_SPLITTER.split_documents(selected_documents)
    return Chroma.from_documents(documents, OllamaEmbeddings(model=model_name))


def getChatChain(llm, db):
    """Constructs a chat chain for handling questions and returning answers."""
    retriever = db.as_retriever(search_kwargs={"k": 10})

    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(lambda x: get_buffer_string(x["history"])),
    )

    standalone_question = {
        "standalone_question": {
            "question": lambda x: x["question"],
            "chat_history": lambda x: x["chat_history"],
        }
        | CONDENSE_QUESTION_PROMPT
        | llm
    }

    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }

    final_inputs = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    answer = {
        "answer": final_inputs
        | ANSWER_PROMPT
        | llm.with_config(callbacks=[StreamingStdOutCallbackHandler()]),
        "docs": itemgetter("docs"),
    }

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    def chat(question: str):
        inputs = {"question": question}
        result = final_chain.invoke(inputs)
        memory.save_context(inputs, {"answer": result["answer"]})

    return chat


def main(llm_model_name: str, embedding_model_name: str, documents_path: str) -> None:
    """Main function to initialize the chat system."""
    check_if_model_is_available(llm_model_name)
    check_if_model_is_available(embedding_model_name)

    db = load_documents_into_database(embedding_model_name, documents_path)
    llm = Ollama(model=llm_model_name)
    chat = getChatChain(llm, db)

    while True:
        user_input = input("\n\nPlease enter your question (or type 'exit' to end): ")
        if user_input.lower() == "exit":
            break
        chat(user_input)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run local LLM with RAG with Ollama.")
    parser.add_argument("-m", "--model", default="mistral", help="The name of the LLM model to use.")
    parser.add_argument(
        "-e", "--embedding_model", default="nomic-embed-text", help="The name of the embedding model to use."
    )
    parser.add_argument("-p", "--path", default="Research", help="Path to the documents directory.")
    args = parser.parse_args()

    main(args.model, args.embedding_model, args.path)
