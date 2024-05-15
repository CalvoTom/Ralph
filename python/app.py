from flask import Flask, request, render_template
from api import *

app = Flask(__name__)

# Set the threshold value here (e.g., 10)
THRESHOLD = 10

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        word_freqs = get_word_frequencies()
        pages = rank_pages(word_freqs)
        return render_template('index.html', query=query, pages=pages)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
