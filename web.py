from flask import Flask, render_template, request
from main import create_full_data_struct

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    bus_time_info = create_full_data_struct(postcode)
    return render_template('info.html', info=bus_time_info)


if __name__ == "__main__":
    app.run()
