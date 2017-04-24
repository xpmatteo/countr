from flask import Flask, redirect, make_response
from random import Random

random = Random()
counts = {}
app = Flask(__name__)

@app.route('/')
def show_counts():
    return 'No counts defined'

@app.route('/counts', methods=['POST'])
def create_count():
    count_id = str(random.randint(0, 1000*1000*1000))
    counts[count_id] = 0
    return redirect('/counts/' + count_id)

@app.route('/counts/<count_id>', methods=['GET'])
def get_count(count_id):
    if count_id in counts:
        response = make_response(str(counts[count_id]))
        response.content_type = 'text/plain'
        return response
    return ("Not Found", 404)

if __name__ == '__main__':
    app.run()