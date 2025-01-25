# 📚 PDF Chatbot

Welcome to **PDF Chatbot** – a Python-based tool that allows users to search and interact with the contents of a PDF file through an intuitive chatbot interface. Whether you're looking to extract information or simply explore the content, this project makes working with PDFs a breeze! 🚀

---

## 🌟 Features
- 🛠️ **PDF Parsing**: Reads the content of a PDF file and extracts searchable text.
- 💬 **Chat Interface**: Chat with your PDF content effortlessly.
- 🔍 **Search Functionality**: Quickly find specific content within the PDF.
- 📄 **GUI Interface**: A user-friendly interface to upload PDFs, search, and get results.
- 🔒 **Error Handling**: Ensures proper handling of non-searchable PDFs and provides appropriate feedback.

---

## 🛑 Prerequisites
To get started, ensure you have the following installed on your system:
- **Python 3.x**
- **PyPDF2 Library**

To install the required library, run:
```bash
pip install PyPDF2
```

---

## 📂 Project Structure
The project is organized into easy-to-understand components:

1. `read_pdf(file_path)`: A function that reads and extracts text from a PDF file.
2. `chat_with_pdf(content)`: A chat interface that allows users to interact with the extracted PDF content.
3. **GUI Elements**:
   - **Upload Button**: Upload your PDF file for analysis.
   - **Search Box**: Enter your queries to find specific information in the PDF.
   - **Results Section**: Displays search results from the PDF.
4. `file_path`: Modify this variable to specify the PDF file you want to process.
5. `pdf_content = read_pdf(file_path)`: Extracts text content from the PDF.

---

## 💻 Usage

Follow these steps to use the project:

### 1. **Prerequisites**
   - Ensure **Python 3.x** is installed on your system.
   - Install the required dependency:
     ```bash
     pip install PyPDF2
     ```

### 2. **Setup**
   - Place the PDF file in the same directory as the script.
   - Alternatively, provide the **absolute path** to the PDF file in the script.

### 3. **Run the Script**
   - Open your terminal or command prompt.
   - Navigate to the directory where the script (`pdfbot.py`) is located:
     ```bash
     cd path/to/pdfchatbot
     ```
   - Run the script:
     ```bash
     python pdfbot.py
     ```

### 4. **Interact with the GUI**
   - After running the script, a **GUI window** will open.
   - Features include:
     - **Upload PDF**: Click this button to select and upload your PDF file.
     - **Search Box**: Enter your query and click "Search" to find relevant content.
     - **Status Label**: Displays the status of the uploaded PDF (e.g., "PDF uploaded and ready to use (Total Pages: X)").
     - **Results Section**: The chatbot displays search results from the uploaded PDF.

### 5. **Note**
   - Ensure your PDF contains **searchable text**. If no text is found, the chatbot will display an appropriate message.
   - You can upload and analyze different PDF files during the same session.

---

## 🌐 How to Clone and Run This Project

### 1. Clone this repository:
```bash
git clone https://github.com/your-username/pdfchatbot.git
```

### 2. Navigate to the project directory:
```bash
cd pdfchatbot
```

### 3. Install dependencies:
```bash
pip install PyPDF2
```

### 4. Run the project:
Follow the steps described in the **Usage** section.

---

## 🤝 How to Contribute

We’re always looking for contributors to help us improve this project! Here’s how you can get involved:

### 1. **Fork the Repository**
   - Click the **Fork** button on this repository to create your copy.

### 2. **Clone Your Fork**
   - Clone the forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/pdfchatbot.git
     ```

### 3. **Create a New Branch**
   - Create a feature branch for your changes:
     ```bash
     git checkout -b feature-branch-name
     ```

### 4. **Make Your Changes**
   - Enhance the chatbot, fix bugs, or improve the documentation.

### 5. **Commit Your Changes**
   - Write a descriptive commit message:
     ```bash
     git commit -m "Add: Description of your changes"
     ```

### 6. **Push to Your Branch**
   - Push your changes to your forked repository:
     ```bash
     git push origin feature-branch-name
     ```

### 7. **Submit a Pull Request**
   - Go to the original repository on GitHub.
   - Click **Pull Requests** and submit your pull request for review.

We’ll review your contribution and merge it if it adds value!

---

## 📝 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute this project in compliance with the license.

---

## 📧 Contact

For any questions, issues, or feedback, please reach out:
- **Email**: your-email@example.com
- **GitHub**: [Your Profile](https://github.com/your-username)

---

### 🌟 If you found this project useful, don’t forget to star it! ⭐
