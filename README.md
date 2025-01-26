# PDFchatbot

This project creates a PDF Chatbot that allows users to search and chat with the contents of a PDF file.

Prerequisites
Python 3.x

PyPDF2 library

To install the PyPDF2 library, you can use pip in the terminal:

pip install PyPDF2 

PROJECT STRUCTURE

1. read_pdf(file_path): This function reads the content of a PDF file and returns the text.

2. chat_with_pdf(content): This function allows the user to interact with the PDF content through a chat interface.

3. file_path = "maths.pdf": The path to the PDF file you want to read.

4. pdf_content = read_pdf(file_path): Reads the PDF content.

If the PDF content is read successfully, chat_with_pdf(pdf_content) is called to start the chat interface.

Here's the updated **Usage** section based on your provided instructions:

USAGE:

1. **Prerequisites**:
   - Ensure that you have **Python 3.x** installed on your system.
   - You must have the **PyPDF2** library installed. If not         -installed, you can install it using:
     pip install PyPDF2


2. **Setup**:
   - Place your **PDF file** in the same directory as your script, or ensure you provide the correct path to the PDF file you want to upload.

3. **Running the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory where your script (`pdfbot.py`) is located.
   - Run the script by executing:
     python pdfbot.py

4. **Interacting with the GUI**:
   - Upon running the script, the **PDF Chatbot** GUI will open.
   - You will see the following UI elements:
     - **Upload PDF**: Click this button to select and upload your PDF file.
     - once you click upload and choose the wait for few seconds until a new similar dialogue box appear.
     - **Search**: Now, Enter your query in the text box and click this button to search for the text within the uploaded PDF.
     - **Status Label**: This label will display the status of the uploaded PDF (e.g., "PDF uploaded and ready to use (Total Pages: x)").
   - **Results**: The search results will be displayed in a text area within the GUI.

5. **Note**:
   - Ensure your PDF file contains searchable text. If no text is found, an appropriate message will be displayed.
   - You can interact with the PDF by uploading different files and searching through them using various queries.

This updated **Usage** section makes it clearer for users to understand the steps required to run and interact with the script efficiently.

4. Interact with your PDF through the chat interface. Type your queries, and the bot will search for relevant content within the PDF and display it. Type exit to end the chat.

   Don't forget to change the file_path to the original path of the required pdf

--Added the Text-to-Speech support