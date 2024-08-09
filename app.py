import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import review_analysis as mra  # Import the original script

def show_reviews():
    movie_name = movie_entry.get().strip()  # Get and trim the movie name
    if not movie_name:
        messagebox.showwarning("Input Error", "Please enter a movie name.")
        return

    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.INSERT, "Fetching reviews...\n")
    app.update()

    try:
        mra.movie = movie_name  # Set the movie name in the original script
        mra.query = movie_name + " User review"
        mra.r = ""
        for j in mra.search(mra.query, num=40, stop=2, pause=2):
            mra.r = j

        response = mra.urllib.request.urlopen(mra.r)
        html = response.read()
        mra.soup = mra.BeautifulSoup(html, 'html.parser')

        mra.reviews = mra.get_imdb_reviews(movie_name)
        mra.df = mra.pd.DataFrame({'Review': mra.reviews})
        mra.df['Review'] = mra.df['Review'].apply(mra.cleanTxt)

        positive = []
        negative = []
        neutral = []

        for review in mra.df['Review']:
            if mra.afinn.score(review) > 0:
                positive.append(review)
            elif mra.afinn.score(review) < 0:
                negative.append(review)
            else:
                neutral.append(review)

        result_text.delete(1.0, tk.END)  # Clear the "Fetching reviews..." text
        result_text.insert(tk.INSERT, f"Total reviews: {len(mra.df['Review'])}\n")
        result_text.insert(tk.INSERT, f"Positive reviews: {len(positive)}\n")
        result_text.insert(tk.INSERT, f"Negative reviews: {len(negative)}\n")
        result_text.insert(tk.INSERT, f"Neutral reviews: {len(neutral)}\n")

        result_text.insert(tk.INSERT, "\n--- Positive Reviews ---\n")
        for review in positive:
            result_text.insert(tk.INSERT, review + "\n")

        result_text.insert(tk.INSERT, "\n--- Negative Reviews ---\n")
        for review in negative:
            result_text.insert(tk.INSERT, review + "\n")

        result_text.insert(tk.INSERT, "\n--- Neutral Reviews ---\n")
        for review in neutral:
            result_text.insert(tk.INSERT, review + "\n")

    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.INSERT, f"Error fetching reviews: {str(e)}")

app = tk.Tk()
app.title("Movie Review Sentiment Analysis")
app.geometry("600x500")
app.config(bg="#f0f0f0")

# Title Label
title_label = tk.Label(app, text="Movie Review Sentiment Analysis", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Movie Name Entry
entry_frame = tk.Frame(app, bg="#f0f0f0")
entry_frame.pack(pady=5)
tk.Label(entry_frame, text="Enter Movie Name:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5)
movie_entry = tk.Entry(entry_frame, width=30, font=("Helvetica", 12))
movie_entry.pack(side=tk.LEFT, padx=5)

# Show Reviews Button
show_button = tk.Button(app, text="Show Reviews", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=show_reviews)
show_button.pack(pady=10)

# Results Text Box
result_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 10), bg="#ffffff", fg="#333")
result_text.pack(pady=10, padx=10)

# Footer Label
footer_label = tk.Label(app, text="Developed by [Vivekecoder]", font=("Helvetica", 15), bg="#000000", fg="#777")
footer_label.pack(side=tk.BOTTOM, pady=5)

app.mainloop()
