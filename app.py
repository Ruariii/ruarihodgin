# app.py

from flask import Flask, render_template, abort
from projects_model import ProjectModel

app = Flask(__name__)
model = ProjectModel()
model.load_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    all_projects = model.all()
    print(all_projects)
    return render_template('projects.html', projects=all_projects)

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
