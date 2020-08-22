from flask import Flask, render_template, request, jsonify
from following import get_following, get_oauth

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        username = request.json['username']
        token = get_oauth()
        res = get_following(username, token)
        data = {'username': username, 'following': res}
        return jsonify(data)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
