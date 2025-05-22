# app.py

from flask import Flask, render_template, request, abort
from projects_model import ProjectModel
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
model = ProjectModel()
model.load_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/projects")
def contacts():
    search = request.args.get("q")
    if search is not None:
        all_projects  = model.search(search)
        all_projects.sort(key=lambda p: datetime.strptime(p.date, "%m/%Y"), reverse=True)
        if request.headers.get('HX-Trigger') == 'search':
            #render only rows
            return render_template("list.html", projects=all_projects)
    else:
        all_projects = model.all()
        all_projects.sort(key=lambda p: datetime.strptime(p.date, "%m/%Y"), reverse=True)
    return render_template('projects.html', projects=all_projects)
    
    
@app.route('/projects/count')
def projects_count():
    search = request.args.get("q")
    if search:
        print(search)
        count = len(model.search(search))
        print(count)
    else:
        count = model.count()
    return f"{count} project{'s' if count != 1 else ''} found"


@app.route('/project/<project_id>')
def project_detail(project_id):
    project = model.get_project_by_id(project_id)
    if not project:
        abort(404)
    next_id = model.get_next_project_id(project_id)
    prev_id = model.get_previous_project_id(project_id)
    return render_template('project.html', project=project, next_id=next_id, prev_id=prev_id)

if __name__ == '__main__':
    app.run(debug=True)
