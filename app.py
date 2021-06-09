from flask import Flask, render_template, render_template_string, request, redirect, url_for
from forms import *
import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

import requestURL, base, getAllStatuses