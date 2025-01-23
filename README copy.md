# Retrieval-Augmented Generation with Document Selection

This project demonstrates a Retrieval-Augmented Generation (RAG) system using local language models with the Ollama framework. Users can load documents, select specific ones to include in the retrieval database, and ask questions based on those selected documents. The system provides clear, detailed answers using the selected research materials.

## Features
- Load documents from a specified directory (`.pdf` and `.md` files supported).
- Interactive document selection before building the retrieval database.
- Retrieval-Augmented Generation using selected documents.
- Support for custom language models and embedding models with Ollama.
- Continuous chat system for question answering.

## Prerequisites
- Python 3.8+
- Install the required Python packages using the provided `requirements.txt` file.
- Ollama installed and configured locally ([Ollama Documentation](https://ollama.ai)).

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/rag-with-document-selection.git
   cd rag-with-document-selection
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Ollama is installed and running.

## Usage

### Command-Line Arguments
- `--model` (`-m`): The name of the language model to use (default: `mistral`).
- `--embedding_model` (`-e`): The name of the embedding model to use (default: `nomic-embed-text`).
- `--path` (`-p`): Path to the directory containing documents (default: `Research`).

### Running the Program
1. Start the program:
   ```bash
   python main.py -m mistral -e nomic-embed-text -p /path/to/documents
   ```
2. The program will display a list of available documents.
3. Enter the numbers corresponding to the documents you want to include in the retrieval database (comma-separated).
4. Ask questions interactively based on the selected documents.
5. Type `exit` to quit the program.

### Example
```bash
$ python main.py -m mistral -e nomic-embed-text -p ./docs

Available Documents:
1: Research1.pdf
2: Notes.md
3: Summary.pdf

Enter the numbers of the documents you want to include (comma-separated): 1,3

Selected Documents:
- Research1.pdf
- Summary.pdf

Please enter your question (or type 'exit' to end): What are the key findings in Research1?
...
```

## File Structure
- `main.py`: Entry point for the application.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.

## Customization
- Modify `TEXT_SPLITTER` in the code to adjust document chunk sizes.
- Extend `load_documents_and_prompt_user` to support additional file formats.
- Replace default prompts (`CONDENSE_QUESTION_PROMPT`, `ANSWER_PROMPT`) to customize the assistant's behavior.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [LangChain](https://github.com/hwchase17/langchain): For providing the foundation for RAG implementation.
- [Ollama](https://ollama.ai): For supporting local language models.