import tkinter as tk
from tkinter import filedialog, messagebox, font

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = {line.strip().lower() for line in file}
    return words

def is_valid_word(word, center_letter, input_letters):
    return (
        len(word) >= 4 and
        center_letter in word and
        all(letter in input_letters for letter in word)
    )

def spellbee_solver(input_string, words_file):
    center_letter = None
    for char in input_string:
        if char.isupper():
            center_letter = char.lower()
            break

    if not center_letter:
        raise ValueError("Input must contain one capital letter as the center letter.")

    input_letters = {char.lower() for char in input_string}
    word_list = load_words(words_file)

    valid_words = [word for word in word_list if is_valid_word(word, center_letter, input_letters)]
    return sorted(valid_words)

def solve_spellbee():
    input_string = input_entry.get()
    try:
        if not words_file:
            raise ValueError("Please load a dictionary file first.")
        
        valid_words = spellbee_solver(input_string, words_file)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Valid words ({len(valid_words)}):\n\n")
        
        for index, word in enumerate(valid_words, start=1):
            result_text.insert(tk.END, f"{index}. {word}\n")  # Add serial number before the word
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def load_dictionary():
    global words_file
    file_path = filedialog.askopenfilename(
        title="Select Dictionary File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        words_file = file_path
        dictionary_label.config(text=f"Dictionary Loaded: {file_path.split('/')[-1]}")

def zoom_in():
    adjust_font_size(2)

def zoom_out():
    adjust_font_size(-2)

def adjust_font_size(delta):
    current_size = app_font.actual()["size"]
    new_size = max(current_size + delta, 8)
    app_font.configure(size=new_size)
    result_text.configure(font=app_font)

def apply_styles():
    root.configure(bg="#2C3E50")
    frame.configure(bg="#34495E")
    input_label.configure(bg="#34495E", fg="white", font=("AppFont", 12, "bold"))
    dictionary_label.configure(bg="#34495E", fg="#AAB7B8", font=("AppFont", 10))
    solve_button.configure(bg="#1ABC9C", fg="white", font=("AppFont", 12), activebackground="#16A085")
    load_button.configure(bg="#3498DB", fg="white", font=("AppFont", 12), activebackground="#2980B9")
    result_text.configure(bg="#ECF0F1", fg="#2C3E50", font=app_font, state="normal")

# Initialize main window
root = tk.Tk()
root.title("Spellbee Solver")
root.geometry("600x600")

# Create the custom font
app_font = font.Font(root=root, family="Helvetica", size=12)

words_file = None

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

input_label = tk.Label(frame, text="Enter 7 letters (1 capital letter):")
input_label.grid(row=0, column=0, sticky="w")

input_entry = tk.Entry(frame, width=20, font=app_font)
input_entry.grid(row=0, column=1, padx=5)

solve_button = tk.Button(frame, text="Solve", command=solve_spellbee)
solve_button.grid(row=0, column=2, padx=5)

load_button = tk.Button(frame, text="Load Dictionary", command=load_dictionary)
load_button.grid(row=1, column=0, pady=5)

dictionary_label = tk.Label(frame, text="No dictionary loaded", fg="gray")
dictionary_label.grid(row=1, column=1, columnspan=2, sticky="w")

result_text = tk.Text(root, width=50, height=20, wrap="word", padx=10, pady=10)
result_text.pack()

zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in, bg="#27AE60", fg="white")
zoom_in_button.pack(side="left", padx=5, pady=5)

zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out, bg="#E74C3C", fg="white")
zoom_out_button.pack(side="left", padx=5, pady=5)

apply_styles()

root.mainloop()
