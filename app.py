import streamlit as st
import PyPDF2
import re
import pyttsx3
import threading
import time
import json
from typing import List, Tuple
from gtts import gTTS
import tempfile 

# Optional libraries for OCR
try:
    from pdf2image import convert_from_bytes
    import pytesseract
except ImportError:
    st.warning("To enable OCR for scanned PDFs, please install 'pdf2image' and 'pytesseract' libraries.")

# For WebSocket client functionality
try:
    import websocket  # from 'websocket-client' package
except ImportError:
    st.warning("To enable real-time collaboration, please install the 'websocket-client' package.")

# For OpenAI API (ensure you have openai installed and your API key configured)
try:
    import openai
except ImportError:
    st.warning("To enable AI summarization, please install the 'openai' package.")

# ------------------------------
# Helper Functions
# ------------------------------



def extract_pdf_text(file) -> Tuple[List[str], bool]:
    """
    Extract text from a PDF file.
    If the page text is empty, try using OCR to extract text from the page image.
    Returns a tuple (list of page texts, success flag).
    """
    try:
        reader = PyPDF2.PdfReader(file)
        pages_text = []
        
        # Read file bytes for OCR conversion
        file.seek(0)
        file_bytes = file.read()
        file.seek(0)  # Reset pointer for PyPDF2
        
        # Try to convert PDF pages to images for OCR if available
        try:
            images = convert_from_bytes(file_bytes)
        except Exception as e:
            images = []
            st.warning("OCR conversion failed; make sure Poppler is installed properly.")
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text or not text.strip():
                # If text extraction failed, try OCR if we have an image
                if images and i < len(images):
                    try:
                        text = pytesseract.image_to_string(images[i])
                        if not text.strip():
                            text = f"Page {i+1} has no extractable text."
                    except Exception as e:
                        text = f"Error during OCR on Page {i+1}: {str(e)}"
                else:
                    text = f"Page {i+1} has no extractable text."
            pages_text.append(text)
        return pages_text, True
    except Exception as e:
        st.error(f"PDF Error: {str(e)}")
        return [f"Error processing PDF: {str(e)}"], False

def translate_text(text: str, dest_lang: str) -> str:
    """Translate text to the target language synchronously."""
    try:
        from googletrans import Translator
        translator = Translator()
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        st.error(f"Translation Error: {str(e)}")
        return text

def text_to_speech(text):
    """Convert text to speech and return the audio file path."""
    tts = gTTS(text=text, lang="en")
    
    # Save audio in a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    
    return temp_file.name

def summarize_text(text: str) -> str:
    """
    Use the OpenAI API to summarize the provided text.
    Make sure your API key is set in Streamlit secrets as OPENAI_API_KEY.
    """
    openai_api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not openai_api_key:
        st.error("OpenAI API key not found in secrets. Please add it as OPENAI_API_KEY.")
        return "Summarization unavailable."
    
    openai.api_key = openai_api_key
    try:
        # Using GPT-3.5 Turbo for summarization
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "Summarization failed."

# ------------------------------
# Real-Time Collaboration: WebSocket Client
# ------------------------------

WS_SERVER_URL = "ws://localhost:6789"

def on_message(ws, message):
    """Callback when a message is received from the WebSocket server."""
    try:
        data = json.loads(message)
        # Append the received annotation to the shared session state list.
        if "collab_annotations" not in st.session_state:
            st.session_state.collab_annotations = []
        st.session_state.collab_annotations.append(data)
        # Force a re-run of the app to display new annotations.
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error processing collaborative message: {e}")

def on_error(ws, error):
    st.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    st.info("WebSocket connection closed.")

def websocket_listen():
    """Background thread function to connect and listen to the WebSocket server."""
    ws = websocket.WebSocketApp(WS_SERVER_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

def start_ws_client():
    """Start the WebSocket client thread if not already started."""
    if "ws_client_started" not in st.session_state:
        st.session_state.ws_client_started = True
        threading.Thread(target=websocket_listen, daemon=True).start()

# ------------------------------
# Streamlit UI Configuration
# ------------------------------

st.set_page_config(
    page_title="PDF Bot - Your AI Assistant",
    page_icon="📄",
    layout="wide",
)

# ------------------------------
# Sidebar: Dark Mode Toggle and File Upload
# ------------------------------

with st.sidebar:
    st.header("📂 Document Operations")
    dark_mode = st.checkbox("Enable Dark Mode", value=False)
    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"],
        help="Maximum file size: 50MB"
    )

# ------------------------------
# Conditional CSS Styling for Dark and Light Modes
# ------------------------------

if dark_mode:
    background_color = "#1a1a1a"
    text_color = "#ffffff"
    header_color = "#ecf0f1"
    button_bg = "#4CAF50"
    button_hover = "#45a049"
else:
    background_color = "#f8f9fa"
    text_color = "#000000"
    header_color = "#2c3e50"
    button_bg = "#4CAF50"
    button_hover = "#45a049"

custom_css = f"""
    <style>
        .main {{
            background-color: {background_color};
            color: {text_color};
            padding: 2rem;
        }}
        [data-testid="stMarkdownContainer"] * {{
            color: {text_color} !important;
        }}
        textarea {{
            color: {text_color} !important;
            background-color: {background_color} !important;
            border: 1px solid #ccc !important;
        }}
        .stButton>button {{
            background-color: {button_bg};
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            transition: transform 0.2s;
        }}
        .stButton>button:hover {{
            transform: scale(1.05);
            background-color: {button_hover};
        }}
        .stDownloadButton>button {{
            background-color: #008CBA !important;
        }}
        .highlight {{
            background-color: #ffff00;
            padding: 2px 4px;
            border-radius: 4px;
        }}
        /* Header styling */
        .header {{
            text-align: center;
            padding: 2rem 0;
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------
# Header Section
# ------------------------------

st.markdown(f"""
    <div class="header">
        <h1 style="color: {header_color};">📄 PDF Bot</h1>
        <h3 style="color: #3498db;">Your Intelligent Document Assistant</h3>
    </div>
""", unsafe_allow_html=True)

# Start the WebSocket client for real-time collaboration
if uploaded_file:
    start_ws_client()

# ------------------------------
# Main Application Logic
# ------------------------------

if uploaded_file:
    with st.spinner("Processing document..."):
        start_time = time.time()
        pdf_pages, success = extract_pdf_text(uploaded_file)
        processing_time = time.time() - start_time

    if not success:
        st.stop()

    st.success(f"Document processed in {processing_time:.2f} seconds.")

    # Create tabs for different operations, including the new AI Summarization tab
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Document Text", 
        "🔍 Advanced Search", 
        "🌍 Translation & TTS", 
        "🤖 AI Summarization"
    ])

    # --- Tab 1: Document Text Viewer with Page Navigation, Annotation & Real-Time Collaboration ---
    with tab1:
        st.subheader("Document Content Viewer")
        
        # Initialize current page and annotations in session state
        if "current_page" not in st.session_state:
            st.session_state.current_page = 0
        if "annotations" not in st.session_state:
            st.session_state.annotations = {}  # Local annotations: {page index: list of (selected_text, annotation)}
        if "collab_annotations" not in st.session_state:
            st.session_state.collab_annotations = []  # Collaborative annotations from other users

        # Navigation Buttons
        nav_cols = st.columns([1, 2, 1])
        with nav_cols[0]:
            if st.button("Previous Page"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
        with nav_cols[1]:
            st.markdown(f"**Page {st.session_state.current_page + 1} of {len(pdf_pages)}**")
        with nav_cols[2]:
            if st.button("Next Page"):
                if st.session_state.current_page < len(pdf_pages) - 1:
                    st.session_state.current_page += 1

        # Display the current page text (non-editable)
        page_text = pdf_pages[st.session_state.current_page]

        st.text_area("Page Text (copy any part to annotate)", value=page_text, height=400,
                     key=f"page_text_{st.session_state.current_page}", disabled=True)    


        st.subheader("🎤 Press Text-to-Speech ")

        if st.button("Generate Speech"):
            if page_text.strip():
                audio_path = text_to_speech(page_text)
                
                # Play the generated audio
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
                
                st.success("✅ Speech generated successfully!")
            else:
                st.warning("⚠️ Please enter text before generating speech.")


        st.markdown("### Annotate Selected Text")
        st.markdown("*Tip: To annotate a snippet, select the text from the above area, copy it, and paste it below.*")
        selected_text = st.text_input("Enter the text you want to annotate:", key="selected_text")
        annotation_text = st.text_area("Enter your annotation for the selected text:", key="annotation_text", height=100)
        if st.button("Save Annotation"):
            if selected_text.strip() != "" and annotation_text.strip() != "":
                page_index = st.session_state.current_page
                # Save locally
                if page_index not in st.session_state.annotations:
                    st.session_state.annotations[page_index] = []
                annotation_data = {
                    "page": page_index + 1,
                    "selected_text": selected_text,
                    "annotation": annotation_text,
                    "timestamp": time.time(),
                    "user": "LocalUser"  # In a real app, use a proper user ID
                }
                st.session_state.annotations[page_index].append((selected_text, annotation_text))
                st.success("Annotation saved locally!")
                
                # Send the annotation to the WebSocket server for collaboration
                try:
                    ws = websocket.create_connection(WS_SERVER_URL)
                    ws.send(json.dumps(annotation_data))
                    ws.close()
                except Exception as e:
                    st.error(f"Failed to send annotation to collaboration server: {e}")
            else:
                st.warning("Please enter both the selected text and your annotation.")

        # Show local annotations for the current page (if any)
        page_index = st.session_state.current_page
        if page_index in st.session_state.annotations and st.session_state.annotations[page_index]:
            st.markdown("#### Your Annotations for this Page:")
            for i, (sel_text, ann_text) in enumerate(st.session_state.annotations[page_index]):
                st.markdown(f"**Annotation {i+1}:**")
                st.markdown(f"- **Selected Text:** {sel_text}")
                st.markdown(f"- **Annotation:** {ann_text}")
        else:
            st.info("No local annotations for this page yet.")

        # Display Collaborative Annotations received from other users
        st.markdown("### Collaborative Annotations from Other Users")
        if st.session_state.collab_annotations:
            for idx, ann in enumerate(st.session_state.collab_annotations):
                st.markdown(f"**From {ann.get('user', 'Unknown')} on Page {ann.get('page')}:**")
                st.markdown(f"- **Selected Text:** {ann.get('selected_text')}")
                st.markdown(f"- **Annotation:** {ann.get('annotation')}")
        else:
            st.info("No collaborative annotations received yet.")

    # --- Tab 2: Document Search Engine & Annotation ---
    with tab2:
        st.subheader("Document Search Engine")
        search_term = st.text_input("Enter search keywords:", "")
        if search_term.strip():
            matches = []
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            for page_num, text in enumerate(pdf_pages):
                for match in pattern.finditer(text):
                    # Extract context around the match (up to 100 characters on either side)
                    start_context = max(0, match.start() - 100)
                    end_context = min(len(text), match.end() + 100)
                    context = text[start_context:end_context]
                    # Highlight the match within the context
                    highlighted = pattern.sub(r'<span class="highlight">\g<0></span>', context)
                    matches.append((page_num + 1, highlighted))
            
            if matches:
                st.success(f"Found {len(matches)} match(es):")
                # Loop through each match and allow annotation
                for idx, (page, context) in enumerate(matches):
                    with st.container():
                        st.markdown(f"**Page {page}:** {context}", unsafe_allow_html=True)
                        annotate_toggle = st.checkbox("Add Annotation", key=f"annotate_toggle_{idx}")
                        if annotate_toggle:
                            if f"annotation_{idx}" not in st.session_state:
                                st.session_state[f"annotation_{idx}"] = ""
                            annotation = st.text_area("Enter your annotation:", 
                                                      value=st.session_state[f"annotation_{idx}"], 
                                                      key=f"annotation_{idx}_area")
                            st.session_state[f"annotation_{idx}"] = annotation
                            if annotation:
                                st.info(f"Annotation: {annotation}")
            else:
                st.warning("No matches found in the document.")

    # --- Tab 3: Translation & Text-to-Speech ---
    with tab3:
        st.subheader("Translation & Text-to-Speech")
        col1, col2 = st.columns(2)

        # Text Translation Section
        with col1:
            st.markdown("### Text Translation")
            target_lang = st.selectbox(
                "Target Language:",
                ["es", "fr", "de", "zh-cn", "ja", "ru"],
                index=0
            )
            text_to_translate = st.text_area("Enter text to translate:", height=150)
            if st.button("Translate Text"):
                if text_to_translate.strip():
                    with st.spinner("Translating..."):
                        result = translate_text(text_to_translate, target_lang)
                    st.success("Translation Result:")
                    st.write(result)
                else:
                    st.warning("Please enter text to translate.")

        # Text-to-Speech Section
        with col2:
            st.subheader("🎤 Press Text-to-Speech ")
            tts_text = st.text_area("Enter text to speak:", height=150)
            if st.button("Generate Speech",key=456):
                if tts_text.strip():
                    audio_path = text_to_speech(tts_text)
                    
                    # Play the generated audio
                    with open(audio_path, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    st.success("✅ Speech generated successfully!")
                else:
                    st.warning("⚠️ Please enter text before generating speech.")



    # --- Tab 4: AI-Powered Summarization ---
    with tab4:
        st.subheader("AI-Powered Summarization")
        st.markdown("Use the OpenAI API to generate a concise summary of your document content.")

        # Option to select between summarizing the entire document or a single page.
        summary_option = st.radio("Summarize:", ("Entire Document", "Current Page"), index=1)
        if summary_option == "Entire Document":
            # Concatenate all pages (you might want to limit the length if the PDF is very large)
            full_text = "\n".join(pdf_pages)
            if st.button("Summarize Entire Document"):
                with st.spinner("Summarizing entire document..."):
                    summary = summarize_text(full_text)
                st.markdown("#### Summary:")
                st.write(summary)
        else:
            # Summarize only the current page
            current_text = pdf_pages[st.session_state.current_page]
            st.markdown(f"**Current Page ({st.session_state.current_page + 1}) Content:**")
            st.text_area("Page Text", value=current_text, height=200, disabled=True)
            if st.button("Summarize Current Page"):
                with st.spinner("Summarizing current page..."):
                    summary = summarize_text(current_text)
                st.markdown("#### Summary:")
                st.write(summary)

# ------------------------------
# Footer Section
# ------------------------------

st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0; color: {text_color};">
        <hr style="margin: 1rem 0;">
        <p>PDF Bot v1.0 • Secure Document Processing</p>
    </div>
""", unsafe_allow_html=True)
