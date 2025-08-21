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
    # Pass all projects so we can show their images in the carousel
    all_projects = model.all()
    all_projects.sort(key=lambda p: datetime.strptime(p.date, "%m/%Y"), reverse=True)
    return render_template('index.html', projects=all_projects)

@app.route("/projects")
def projects():
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


@app.route('/about')
def about():
    # Pass all projects so we can show their images in the carousel
    all_projects = model.all()
    all_projects.sort(key=lambda p: datetime.strptime(p.date, "%m/%Y"), reverse=True)
    return render_template('about.html', projects=all_projects)

    
    
@app.route('/projects/count')
def projects_count():
    search = request.args.get("q")
    if search:
        count = len(model.search(search))
    else:
        count = model.count()
    return f"{count} project{'s' if count != 1 else ''} found"


@app.route('/project/<project_id>')
def project_detail(project_id=0):
    id_ = int(project_id)
    project = model.find(id_)
    if not project:
        abort(404)

    next_id = model.find(id_ + 1)
    prev_id = model.find(id_ - 1)

    # Find related projects (sharing keywords)
    related = []
    if project.keywords:
        for other in model.all():
            if other.id != project.id and other.keywords:
                if set(project.keywords) & set(other.keywords):
                    related.append(other)

    # Optional: sort related projects by number of shared keywords (descending)
    related.sort(key=lambda p: len(set(project.keywords) & set(p.keywords)), reverse=True)

    return render_template('project.html', project=project, next_id=next_id, prev_id=prev_id, related_projects=related)


if __name__ == '__main__':
    app.run()
