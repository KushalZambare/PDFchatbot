import tkinter as tk
from tkinter import messagebox, simpledialog
from googletrans import Translator

# Initialize main window
root = tk.Tk()
root.title("Text Translator")
root.geometry("500x400")

translator = Translator()

# Function to handle translation
def handle_translation():
    try:
        # Ensure focus on the text widget
        text_widget.focus_set()
        
        # Get selected text
        selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        if not selected_text:
            raise ValueError("No text selected")

        # Ask user for target language
        target_language = simpledialog.askstring(
            "Translate", "Enter target language code (e.g., 'fr' for French, 'es' for Spanish):"
        )

        if target_language:
            # Translate text
            translated_text = translator.translate(selected_text, dest=target_language).text
            
            # Clear previous translation and insert new one
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Original: {selected_text}\n\nTranslated ({target_language}):\n{translated_text}")

    except (tk.TclError, ValueError):
        messagebox.showinfo("Translation Error", "Please select some text first!")

# Text Widget for Input
text_widget = tk.Text(root, wrap=tk.WORD, height=8, font=("Arial", 12))
text_widget.pack(pady=10, padx=10)
text_widget.insert(tk.END, "Select this text and try translating it!")

# Button to trigger translation
translate_button = tk.Button(root, text="Translate Selected Text", command=handle_translation)
translate_button.pack(pady=5)

# Text Widget to Show Translated Output
result_text = tk.Text(root, wrap=tk.WORD, height=6, font=("Arial", 12), fg="blue")
result_text.pack(pady=10, padx=10)

# Run the application
root.mainloop()
