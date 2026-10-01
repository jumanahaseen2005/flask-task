from flask import Flask, render_template, request,jsonify
import pandas as pd
from services.analyzer import analyze_data


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    file = request.files["file"]

    df = pd.read_csv(file)

    df, class_average, top_performer, pass_percentage = analyze_data(df)

    students = df.to_dict("records")

    return render_template(
        "results.html",
        students=students,
        class_average=class_average,
        top_performer=top_performer,
        pass_percentage=pass_percentage
    )


@app.route("/api/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    students = data["students"]

    df = pd.DataFrame(students)

    df, class_average, top_performer, pass_percentage = analyze_data(df)

    results = df.to_dict("records")
    # results = []
# for student in df.to_dict("records"):
# results.append({
#         "name": student["name"],
#         "python": student["python"],
#         "java": student["java"],
#         "html": student["html"],
#         "css": student["css"],
#         "Total": student["Total"],
#         "Average": student["Average"],
#         "Grade": student["Grade"]
#     })

    return jsonify({
        "class_average": class_average,
        "top_performer": top_performer,
        "pass_percentage": pass_percentage,
        "students": results
    })


if __name__ == "__main__":
    app.run(debug=True)