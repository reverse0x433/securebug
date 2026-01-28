from flask import Flask,render_template,request,redirect,url_for
from db import create_bug,assign_bug,change_bug_status,audit_log

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_bug", methods=["POST","GET"])
def create_bug_route():
    if request.method=="POST":
        try:
            title = request.form.get("title")
            description = request.form.get("description")
            severity = request.form.get("severity")
            reporter_id = int(request.form.get("reporter_id"))

            create_bug(title, description, severity, reporter_id)

            return redirect(url_for("home"))
        except Exception as e:
            return str(e)

    return render_template("create_bug.html")


@app.route("/assign_bug",methods=["POST","GET"])
def assign_bug_route():
    if request.method=="POST":
        try:
            bug_id = int(request.form.get("bug_id"))
            assignee_id = int(request.form.get("assignee_id"))
            actor_id = int(request.form.get("actor_id"))

            assign_bug(bug_id, assignee_id, actor_id)


            return redirect(url_for("home"))
        except Exception as e:
            return str(e)

    return render_template("assign_bug.html")


@app.route("/status",methods=["POST","GET"])
def change_status_route():
    if request.method=="POST":
        try:
            bug_id = int(request.form.get("bug_id"))
            new_status = request.form.get("new_status")
            actor_id = int(request.form.get("actor_id"))

            change_bug_status(bug_id, new_status, actor_id)
            return redirect(url_for("home"))
        except Exception as e:
            return str(e)

    return render_template("status.html")

if __name__=="__main__":
    app.run(debug=True)
