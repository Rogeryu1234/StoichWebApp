from flask import Flask, render_template
#from flask import render_template
import matplotlib.pyplot as plt
import io
import base64


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins

app = Flask(__name__)

@app.route('/')
def build_plot():
    return render_template("a.html")

if __name__ == '__main__':
    app.debug = True
    app.run()