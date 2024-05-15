from flask import Flask, request, render_template
from python.api import *

app = Flask(__name__)

# Set the threshold value here (e.g., 10)
THRESHOLD = 10

@app.route('/', methods=['GET', 'POST'])
def search_post():
    if request.method == 'POST':
        query = request.form['query']
        page_scores = get_word_frequencies(query)
        ranked_pages = rank_pages(page_scores)
        return render_template('search.html', query=query, pages=ranked_pages)
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)
