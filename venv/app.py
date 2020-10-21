from flask import Flask, render_template
import projects

app = Flask(__name__)

@app.route('/')
def home_route():
    return render_template("home.html", projects=projects.setup())

@app.route('/hello/')
def hello_route():
    return render_template("hello.html", projects=projects.setup())

@app.route('/fruit&veggie')
def fruit_route():
    return render_template("fruit_veggie.html", projects=projects.setup())

if __name__ == "__main__":
    app.run(debug = True, port=8080)