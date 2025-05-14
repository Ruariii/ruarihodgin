# projects_model.py

import json

class ProjectModel:
    def __init__(self, json_path='projects.json'):
        with open(json_path, 'r') as f:
            self.projects = json.load(f)

    def get_all_projects(self):
        return self.projects

    def get_project_by_id(self, project_id):
        return next((p for p in self.projects if p['id'] == project_id), None)

    def get_next_project_id(self, current_id):
        ids = [p['id'] for p in self.projects]
        try:
            idx = ids.index(current_id)
            return ids[(idx + 1) % len(ids)]
        except ValueError:
            return None

    def get_previous_project_id(self, current_id):
        ids = [p['id'] for p in self.projects]
        try:
            idx = ids.index(current_id)
            return ids[(idx - 1) % len(ids)]
        except ValueError:
            return None
