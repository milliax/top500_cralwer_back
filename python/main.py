from src.fetch_data import fetch_list
from flask import Flask, request, send_from_directory
import pandas as pd
#from dotenv import load_dotenv
from src.utils import time_parser
from src.plot_drawer import draw_cores, draw_countability, draw_country, draw_energy, draw_manufacturer
# load_dotenv()
import multiprocessing
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)
# test route
@app.route("/")
def home():
    return "Good"
# actual route
@app.route("/callback", methods=["POST"])
async def callback():
    #jsons = request.get_json()
    date = time_parser(int(request.json["time"]))
    """ Getting the initial data parallelly"""
    print("deploy jobs")
    results = []
    # creating multiprocessing pool
    pool = multiprocessing.Pool(5)
    # deploying works
    input = [{
        "year": date["year"],
        "month": date["month"],
        "page": page
    } for page in range(1, 6)]
    
    results = pool.map_async(fetch_list, input)

    """ Collecting data """
    results.wait()
    seperated_DF = []
    for page in range(1, 6):
        location = "python/dataframe{page}.csv".format(page=page)
        dataframe = pd.read_csv(location)
        seperated_DF.append(dataframe)
        
    allDF = pd.concat(seperated_DF, ignore_index=True)

    """ returning pictures """
    files = []
    for e in request.json["methods"]:
        file = {}
        if e == "country":
            file["mode"] = "Country"
            file["src"] = draw_country(allDF)
            file["note"] = None
            files.append(file)
        elif e == "energy":
            file["mode"] = "Energy"
            file["src"] = draw_energy(allDF)
            file["note"] = "Top500.org上並不是每一台超級電腦都有這一項數據，因此這項分析可能失準"
            files.append(file)
        elif e == "manufacturer":
            file["mode"] = "Manufacturer"
            file["src"] = draw_manufacturer(allDF)
            file["note"] = None
            files.append(file)
        elif e=="countability":
            file["mode"] = "Countability"
            file["src"] = draw_countability(allDF)
            file["note"] = None
            files.append(file)
        elif e=="cores":
            file["mode"] = "Cores"
            file["src"] = draw_cores(allDF)
            file["note"] = None
            files.append(file)

    return jsonify(files)


@app.get("/shutdown")
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."


@app.get("/picture/<path:path>")
def send_picture(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    # main()
    app.run(host="0.0.0.0", port=7999, use_reloader=False, debug=False)
