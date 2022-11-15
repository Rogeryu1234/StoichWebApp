# This is a test file. 
# It is used for testing javascript functions and debugging.
# Created on 21:13 Nov 14, 2022

from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True


@app.route("/", methods=['GET', 'POST'])
def index():
    print(1)
    if request.method == "POST":
        print(2)
        name = request.form["name"]
        return name + " Hello"
    print(3)
    return render_template("index3.html")


if __name__ == "__main__":
    app.run()