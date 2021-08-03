from flask import Flask, render_template


# Create Flask's `app` object
app = Flask(
    __name__,
    template_folder="templates"
)


@app.route("/")
def hello():
    return render_template("index.html")