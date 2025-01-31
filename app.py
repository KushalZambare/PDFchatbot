import streamlit as st
import PyPDF2
import re
from googletrans import Translator
from pathlib import Path
from google.cloud import translate_v2 as translate
import pyttsx3
import base64
from PIL import Image
import asyncio
import time 
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Set page configuration
st.set_page_config(
    page_title="PDF Bot - Your AI Assistant",
    page_icon="📄",
    layout="wide",
)


st.markdown("""
    <style>
        /* General styling */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            font-size: 16px; /* Global font size */
        }

        .main {
            background-color: #f8f9fa;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            width: 100%;
            font-size: 18px; /* Button font size */
        }

        .stTextInput, .stTextArea {
            border-radius: 8px;
            font-size: 16px; /* Input and textarea font size */
        }

        .st-expander {
            background-color: #f1f1f1;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px; /* Expander font size */
        }

        .stProgress>div>div>div {
            background-color: #007BFF;
        }

        .st-bd {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 16px; /* Card content font size */
        }

        /* Dark mode styling */
        .dark .main {
            background-color: #181818;
        }

        .dark .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
        }

        .dark .stTextInput, .dark .stTextArea {
            background-color: #2C2C2C;
            color: white;
            border-radius: 8px;
            font-size: 16px;
        }

        .dark .st-expander {
            background-color: #333333;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }

        .dark .stProgress>div>div>div {
            background-color: #1E90FF;
        }

        .dark .st-bd {
            background-color: #444444;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)



# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>📄 PDF Bot -  <span style='color: blue;'>Your Intelligent PDF Assistant</span></h1>", unsafe_allow_html=True)

st.write("""
    <div  style="text-align: center;color: green; font-size: 45px;">
        🔥 **Features**
    </div><br><br>
    <ul style="text-align: center; font-size: 20px;">
        <li>📂 **Upload** and extract text from PDFs</li>
        <li>🔍 **Search** for <span style="color: orange;">keywords</span> in the document</li>
        <li>📝 **Summarize** content in <span style="color: violet;">seconds</span></li>
        <li>✍ **Annotate** text with <span style="color: green;">highlights</span></li>
        <li>🌎 **Translate** text to <span style="color: red;">multiple languages</span></li>
        <li>🔊 **Listen** to text using <span style="color: blue;">text-to-speech</span></li>
        <li>🌙 **Toggle** between <span style="color: orange;">Light</span> & <span style="color: black;">Dark Mode</span></li>
    </ul>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("📖 Quick Actions")
    uploaded_file = st.file_uploader(":blue[Upload a PDF]", type=["pdf"])


async def translate_text(text, target_lang):
    translator = Translator()
    translation = await translator.translate(text, dest=target_lang)
    return translation.text

# --- FUNCTION TO RUN TTS IN A SEPARATE THREAD ---
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# --- FUNCTION TO EXTRACT TEXT FROM PDF ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = [page.extract_text() for page in pdf_reader.pages]
    return pdf_text if pdf_text else ["No text found in the PDF."]

st.divider()

if uploaded_file:
    with st.spinner(":blue[Processing PDF...]"):
        time.sleep(2)
        pdf_content = extract_text_from_pdf(uploaded_file)

    # --- DISPLAY TABS ---
    st.markdown("""
            <style>
                /* Increase font size for the tab titles */
                .streamlit-expanderHeader {
                    font-size: 40px;  /* Adjust the font size of the tabs */
                }
                
                /* Dark mode adjustments */
                .dark .streamlit-expanderHeader {
                    font-size: 40px;  /* Same font size for dark mode */
                }
            </style>
        """, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs([f"📜 Full PDF Text", "🔍 Search & Highlight", "🌎 Translation & TTS"])

    with tab1:
        st.subheader("📖 Extracted PDF Text")
        with st.expander("📄 Click to Expand PDF Text"):
            for i, page in enumerate(pdf_content):
                st.markdown(f"### 📃 **Page {i+1}**")
                st.write(page)
    
    with tab2:
        st.subheader("🔎 **Search in PDF**")
        query = st.text_input("🔍 **Enter a keyword to search:**", "")
        
        if query:
            search_results = []
            for i, page in enumerate(pdf_content):
                matches = [m.start() for m in re.finditer(query, page, re.IGNORECASE)]
                for match in matches:
                    snippet = page[max(0, match - 50): match + 50]
                    search_results.append(f"📄 **Page {i+1}**: :green[...{snippet}...]")

            if search_results:
                st.success("✅ **Matches Found!**")
                for result in search_results:
                    st.markdown(result)
            else:
                st.warning("⚠️ No matches found.")

    with tab3:
        st.subheader("🌎 **Translation & Text-to-Speech**")
        selected_text = st.text_area("✍ **Enter text to translate or listen:**", "")
        target_lang = st.text_input("🌍 **Target Language Code** (e.g., 'fr' for French)", "")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 **Translate**"):
                if selected_text and target_lang:
                    # Using asyncio to run the asynchronous translation
                    translated_text = asyncio.run(translate_text(selected_text, target_lang))
                    st.success(f"💬 **Translated Text:** :blue[{translated_text}]")
                else:
                    st.error("⚠️ Please enter text and a valid language code!")


        with col2:
            if st.button("🔊 **Listen**"):
                if selected_text:
                    st.toast("📢 :orange[Reading text...]")
                    # Use threading to handle TTS without blocking
                    threading.Thread(target=speak_text, args=(selected_text,)).start()
                else:
                    st.warning("⚠️ Enter text to read.")

    # --- SUMMARY FEATURE ---
    st.subheader("📜 **Summarize PDF**")
    if st.button("📝 **Generate Summary**"):
        st.info("📌 **Summary:**")
        summary = "\n".join(page[:200] + "..." for page in pdf_content[:5])
        st.write(f":blue[{summary}]")

    # --- DOWNLOAD SUMMARY ---
    if st.button("📥 **Download Summary**"):
        summary = "\n".join(page[:200] + "..." for page in pdf_content[:5])
        st.download_button("⬇️ **Download Summary**", summary, file_name="pdf_summary.txt")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-weight: bold;'>📚 PDF Bot - Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)