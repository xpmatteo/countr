from flask import Flask, redirect, request, make_response, url_for
from random import Random

random = Random()
counts = {}
app = Flask(__name__)

@app.route('/')
def show_counts():
    return redirect(url_for('all_counts'))

@app.route('/counts/', methods=['GET'])
def all_counts():
    return 'x'

@app.route('/counts/', methods=['POST'])
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

@app.route('/counts/<count_id>', methods=['POST'])
def change_count(count_id):
    if count_id in counts:
        counts[count_id] = counts[count_id] + int(request.form.get('increment', 1))
        return redirect(url_for('get_count', count_id=count_id))
    return ("Not Found", 404)

if __name__ == '__main__':
    app.run()
