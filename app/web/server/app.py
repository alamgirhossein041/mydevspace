from flask import Flask, render_template, url_for, flash, redirect, request, send_file, abort, jsonify, json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import numpy as np
import pickle
import folium
import json
import pandas as pd
import os
from rq import Queue
import sys
from worker import return_file
from redis import Redis
from rq.registry import FinishedJobRegistry, StartedJobRegistry
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DOWNLOAD_FOLDER'] = 'misc_files/cryptodata/'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour", "2 per second"]
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(APP_ROOT, 'static')
CRYPTO_FOLDER = os.path.join(STATIC_FOLDER, 'cryptodata')

clusterer = pickle.load(open(os.path.join(APP_ROOT, 'realty_clusterer.pkl'), 'rb'))
realty_ordinal_encoder = pickle.load(open(os.path.join(APP_ROOT, 'realty_ordinal_encoder.pkl'), 'rb'))
realty_onehot_encoder = pickle.load(open(os.path.join(APP_ROOT, 'realty_onehot_encoder.pkl'), 'rb'))
realty_model = pickle.load(open(os.path.join(APP_ROOT, 'realty_xgboost.pkl'), 'rb'))


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/meme_index")
def meme_index():
    pepe_json = str(pd.read_csv('misc_files/pepe_ratio.csv').to_json(orient="records")).replace('\\', '').replace('"',
                                                                                                                  '')
    btcusdt_json = str(pd.read_csv('misc_files/btcusdt.csv').to_json(orient="records")).replace('\\', '').replace('"',                                                                                                     '')

    return render_template('meme_index.html', pepe_json=pepe_json, btcusdt_json=btcusdt_json)


@limiter.exempt
@app.route("/realty_simulator")
def realty_simulator():
    return render_template('realty_simulator.html')


@app.route('/realty_predict', methods=['POST'])
def realty_predict():
    form_inputs = list(request.form.values())
    form_inputs = np.array(form_inputs).reshape(1, -1)

    assigned_cluster = clusterer.predict(form_inputs[:, -2:])

    X_categorical = np.append(form_inputs[:, :8], assigned_cluster)
    X_continuous = form_inputs[:, 8:12]

    X_categorical = realty_ordinal_encoder.transform(X_categorical.reshape(1, -1))
    X_categorical = realty_onehot_encoder.transform(X_categorical)

    X = np.column_stack((X_categorical, X_continuous))

    X = X.astype(np.float32)

    prediction = np.exp(realty_model.predict(X))

    return render_template('realty_simulator.html',
                           prediction_text='Odhadovaná cena bytu je: {:0,.0f} Kč'.format(prediction[0]))


@app.route("/realty_maps_prodeje", methods=['GET', 'POST'])
def realty_maps_prodeje(render=None):
    if render is None:
        render = request.args.get('render')
        if render is None:
            render = '/maps/prodeje_okresy_2021_1.html'

    return render_template('realty_maps_prodeje.html', render=render)


@app.route("/realty_maps_pronajmy", methods=['GET', 'POST'])
def realty_maps_pronajmy(render=None):
    if render is None:
        render = request.args.get('render')
        if render is None:
            render = '/maps/pronajmy_okresy_2021_1.html'

    return render_template('realty_maps_pronajmy.html', render=render)


@limiter.limit("10/minute", override_defaults=False)
@app.route("/display_map", methods=['POST'])
def display_map(typ=None):
    if typ is None:
        typ = request.form['typ']

    try:
        mesic = request.form['mesic']
    except:
        mesic = '1'

    try:
        rok = request.form['rok']
    except:
        rok = '2021'

    filepath = f'maps/{typ}_okresy_{rok}_{mesic[:2]}.html'

    if typ == 'prodeje':

        return redirect(url_for('realty_maps_prodeje', render=filepath))

    elif typ == 'pronajmy':

        return redirect(url_for('realty_maps_pronajmy', render=filepath))

    else:

        print('error')
        print(typ)
        return render_template('home.html')


@limiter.limit("10/minute", override_defaults=False)
@app.route('/tables', methods=('POST', 'GET'))
def tables():
    df = pd.read_csv('misc_files/table_okresy.csv')

    return render_template('tables.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


def download_file(path):
    return send_file(path, as_attachment=True)


q = Queue('default', connection=Redis(host='redis', port=6379))


@limiter.limit("10/minute", override_defaults=False)
@app.route('/binance_api_tool', methods=['GET', 'POST'])
def binance_api_tool():
    registry_finished = FinishedJobRegistry(queue=q)
    registry_current = StartedJobRegistry(queue=q)

    finished_jobs = []
    current_jobs = []

    for finished_job in registry_finished.get_job_ids():

        try:
            finished_jobs.append(q.fetch_job(finished_job))
        except Exception as e:
            print(e)

    finished_jobs = finished_jobs[::-1]

    for current_job in registry_current.get_job_ids():

        try:
            current_jobs.append(q.fetch_job(current_job))
        except Exception as e:
            print(e)

    jobs = q.jobs  # Get a list of jobs in the queue

    q_len = len(q)

    if list(request.form.values()):

        job = q.enqueue(return_file,
                        args=(
                            list(request.form.values()),
                            CRYPTO_FOLDER
                        )
                        )

        jobs = q.jobs
        q_len = len(q)
        current_jobs = []

        for current_job in registry_current.get_job_ids():

            try:
                current_jobs.append(q.fetch_job(current_job))
            except Exception as e:
                print(e)

        return render_template('binance_api_tool.html', jobs=jobs,
                               form_inputs=f"Job added into the queue at {job.enqueued_at}. {q_len} tasks in the queue. {len(current_jobs)} is running.",
                               finished_jobs=finished_jobs, current_jobs=current_jobs)

    return render_template('binance_api_tool.html', jobs=jobs, finished_jobs=finished_jobs, current_jobs=current_jobs,
                           form_inputs=f"There are currently {q_len} tasks in the queue. {len(current_jobs)} is running.")


@limiter.exempt
@app.route("/compound_simulator", methods=['GET', 'POST'])
def compound_simulator():
    stop = False

    X = list(request.form.values())

    try:
        prvni_vklad = int(request.form['prvni_vklad'])
    except Exception:
        stop = True

    try:
        mesicni_prispevek = int(request.form['mesicni_prispevek'])
    except:
        stop = True

    try:
        urok = float(request.form['urok']) / 100
    except:
        stop = True

    try:
        pocet_let = int(request.form['pocet_let'])
    except:
        stop = True

    try:
        vstupni_poplatek = int(request.form['vstupni_poplatek'])
    except:
        stop = True

    try:
        prubezny_poplatek = float(request.form['prubezny_poplatek']) / 100
    except:
        stop = True

    if not stop:

        kumulativni_vklady = []
        kumulativni_poplatky = []
        kumulativni_balance = []
        kumulativni_zhodnoceni = []
        kumulativni_balance_bez_poplatku = []
        months = []

        # VYPOCET

        i = 1
        while i < ((pocet_let * 12) + 1):

            if i == 1:
                balance = prvni_vklad + mesicni_prispevek
                balance_bez_poplatku = prvni_vklad + mesicni_prispevek
                zhodnoceni = (1 + urok / 12)
                poplatek = balance * (prubezny_poplatek / 12) + vstupni_poplatek

            else:

                balance = balance + mesicni_prispevek
                balance_bez_poplatku = balance_bez_poplatku + mesicni_prispevek
                zhodnoceni = (1 + urok / 12)
                poplatek = balance * (prubezny_poplatek / 12)

            balance_bez_poplatku = balance_bez_poplatku * zhodnoceni
            balance = balance * zhodnoceni - poplatek

            # kumulace

            kumulativni_balance.append(round(balance))
            kumulativni_balance_bez_poplatku.append(round(balance_bez_poplatku))

            if i == 1:
                vklady_celkem = mesicni_prispevek + prvni_vklad
                kumulativni_vklady.append(round(mesicni_prispevek + prvni_vklad))
            else:
                vklady_celkem = vklady_celkem + mesicni_prispevek
                kumulativni_vklady.append(round(vklady_celkem))

            if i == 1:
                poplatky_celkem = poplatek
                kumulativni_poplatky.append(round(poplatky_celkem, 2))
            else:
                poplatky_celkem = poplatky_celkem + poplatek
                kumulativni_poplatky.append(round(poplatky_celkem, 2))

            months.append(i)

            i += 1

        return render_template('compound_simulator.html', kum_balance=kumulativni_balance,
                               kum_poplatky=kumulativni_poplatky,
                               kum_vklady=kumulativni_vklady,
                               kum_zhodnoceni=kumulativni_zhodnoceni,
                               kum_balance_bez_poplatku=kumulativni_balance_bez_poplatku,
                               mesice=months,
                               pocet_let=pocet_let,
                               prubezny_poplatek=prubezny_poplatek
                               )
    else:
        return render_template('compound_simulator.html', kum_balance=0,
                               kum_poplatky=0,
                               kum_vklady=0,
                               kum_zhodnoceni=0,
                               kum_balance_bez_poplatku=0,
                               mesice=1,
                               pocet_let=0,
                               prubezny_poplatek=0)


import enchanter


@app.route("/enchanter", methods=['GET', 'POST'])
def enchanter_page():
    X = list(request.form.values())

    stop = False

    try:
        item = str(request.form['item'])
        nr_enchants = str(request.form['nr_enchants'])
    except Exception:
        stop = True

    if not stop:

        ench_results, labels = enchanter.enchant_items(item, nr_enchants)
        print(ench_results, labels)
        df = enchanter.enchant_experiment(item, nr_enchants)

        return render_template('enchanter.html', ench_results=ench_results, labels=labels,
                               column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)


    else:

        ench_results, labels, df = None, None, None

        return render_template('enchanter.html')


@limiter.exempt
@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run()
