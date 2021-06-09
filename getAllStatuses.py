from app import *
from cosmosDB import get_container
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO


@app.route("/getStatuses", methods=['GET', 'POST'])
def get_contact():
    query = "SELECT * FROM c WHERE c.url = '"

    form = WebResources()
    if form.is_submitted():
        result = request.form
        container = get_container('WebStatus')
        error_lst = list(container.query_items(
            query=query + result['url'] + "'",
            enable_cross_partition_query=True
        ))
        all_lst = list(container.query_items(
            query=f"SELECT * FROM c WHERE c.url = '{result['url']}'",
            enable_cross_partition_query=True
        ))
        fig, ax = plt.subplots()

        fig.set_facecolor("#1a1a1a")
        ax.set_facecolor('#1a1a1a')
        ax.tick_params(axis='x', colors='#ffd53a')
        ax.tick_params(axis='y', colors='#ffd53a')
        ax.spines['top'].set_color('#1a1a1a')
        ax.spines['right'].set_color('#1a1a1a')
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))

        plt.plot(np.array([datetime.fromisoformat(el['timestamp']).strftime("%Y-%m-%d %H:%M") for el in all_lst[:]]),
                 np.array(sorted([el['status'] for el in all_lst[:]])), color="#ffd53a")

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png', edgecolor='#1a1a1a')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        html = f'<img src=\'data:image/png;base64,{encoded}\'>'
        for i in range(len(error_lst) - 1, -1, -1):
            if error_lst[i]['status'].startswith('2'):
                del error_lst[i]
        to_render = '{% extends "base.html" %}' \
                    '{% block content %}'
        to_render += '<div class="result-container"><div class="result-msg"> Found ' \
                     + '<b>' + str(len(error_lst)) + '</b> all time errors for <div class="result-url">' \
                     + result['url'] + '</div>' + html + '</div><div class="result-msg">Last 10 errors</div>'
        error_lst.reverse()
        for ell in error_lst[:10]:
            to_render += '<div class="error-container">At: ' + datetime.fromisoformat(ell['timestamp'])\
                .strftime("%Y-%m-%d %H:%M") + ' Status: <b class="status-code">' + ell['status'] + '</b></div>'
        to_render += '</div> {% endblock %}'
        print(to_render)
        return render_template_string(to_render)
    return render_template("getAllStatuses.html", form=form)
