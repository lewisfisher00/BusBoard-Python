from flask import Flask, render_template, request

from main import send_data_for_webpage

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    bus_time_info = send_data_for_webpage(postcode)
    return render_template('info.html', info=(postcode, bus_time_info))


if __name__ == "__main__":
    app.run()
