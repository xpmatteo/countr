from flask import Flask

app = Flask(__name__)

@app.route('/')
def show_counters():
    return 'Foobar'

if __name__ == '__main__':
    app.run()