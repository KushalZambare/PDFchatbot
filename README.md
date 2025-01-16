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

USAGE

1. Ensure that you have Python 3.x and the PyPDF2 library installed.

2. Place your PDF file in the same directory as your script or provide the correct path to your PDF file.

3. Run the script:

   python your_script_name.py

4. Interact with your PDF through the chat interface. Type your queries, and the bot will search for relevant content within the PDF and display it. Type exit to end the chat.

   Don't forget to change the file_path to the original path of the required pdf

