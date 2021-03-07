from flask import Flask, jsonify, render_template, url_for, request, redirect
import data_returns

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if len(request.files) > 0:
            uploaded_file = request.files["filename"]
            if uploaded_file.filename != "":
                uploaded_file.save(r"uploads/" + "datafile.csv")
    return render_template("index.html")
    
@app.route("/vendornames")
def vendors():
    return jsonify(data_returns.vendor_list("datafile.csv"))

@app.route("/dates")
def dates():
    return jsonify(data_returns.date_values("datafile.csv"))

@app.route("/filtered_data", methods=["POST"])
def filtered_data():
    if "vendor" in request.json:
        vendor = request.json['vendor']
        date = request.json['date']
        return data_returns.filtered_data("datafile.csv", vendor, date)
    return {}

@app.route("/plotdata", methods=["POST"])
def data():
    if "plotme" in request.json:
        vendor = request.json['vendor']
        date = request.json['date']   
        return data_returns.plotdata("datafile.csv", vendor, date)
    return {}

if __name__ == "__main__":
    app.run(debug=True)
