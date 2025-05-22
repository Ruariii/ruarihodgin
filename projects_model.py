# projects_model.py

import json
import time

class ProjectModel:

    db = {}

    def __init__(self, id_=None, title=None, date=None, description=None, keywords=None, image=None):
        self.id = id_
        self.title = title
        self.date = date
        self.description = description
        self.keywords = keywords
        self.image = image

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    @classmethod
    def load_db(cls):
        with open('projects.json', 'r') as projects_file:
            projects = json.load(projects_file)
            cls.db.clear()
            for c in projects:
                cls.db[c['id']] = ProjectModel(c['id'], c['title'], c['date'], c['description'], c['keywords'], c['image'])

    @classmethod
    def count(cls):
        time.sleep(2)
        return len(cls.db)
    

    @classmethod
    def find(cls, id_):
        id_ = int(id_)
        c = cls.db.get(id_)

        return c

    @classmethod
    def all(cls):
        return list(cls.db.values())

    @classmethod
    def search(cls, text):
        text = text.lower()
        result = list()
        for c in cls.db.values():
            match_title = c.title is not None and text in c.title.lower()
            match_date = c.date is not None and text in c.date
            match_keywords = c.keywords is not None and any(text in kw.lower() for kw in c.keywords or [])
            if match_title or match_date or match_keywords:
                result.append(c)
        return result