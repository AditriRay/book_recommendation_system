from flask import Flask, render_template, request
import pickle
import numpy as np


# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
df1 = pickle.load(open('df1.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           votes=list(popular_df['Number_Rating'].values),
                           rating=list(popular_df['Average_Rating'].values),
                           image=list(popular_df['Image-URL-M'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    recommended_books = get_recommendations(user_input)
    return render_template('recommend.html', data=recommended_books)

# Recommendation logic
def get_recommendations(book_name):
    try:
        index = np.where(pt.index == book_name)[0][0]
    except IndexError:
        return []  # Book not found

    similar_items = sorted(
        list(enumerate(similarity_score[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []
    for i in similar_items:
        book_title = pt.index[i[0]]
        temp_df = df1[df1['Book-Title'] == book_title].drop_duplicates('Book-Title')

        title = temp_df['Book-Title'].values[0]
        author = temp_df['Book-Author'].values[0]
        image_url = temp_df['Image-URL-M'].values[0]

        data.append([title, author, image_url])

    return data

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

