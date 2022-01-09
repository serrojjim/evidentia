import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost"


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/coordinator/certificate")


class DefDiploma(SequentialTaskSet):

    def on_start(self):
        with open('users.json') as f:
            self.users = json.loads(f.read())
        self.user = choice(list(self.users.items()))

    @task
    def login(self):
        username, password = self.user
        self.token = self.client.post("/login_p/", {
            "username": username,
            "password": password,
        }).json()

    @task
    def diploma(self):
        self.client.get("/coordinator/certificate", json.dumps({
            "nombreDiploma": "TestDiploma",
            "name" : "Roberto",
            'mailto' : 'miguenieva2000@gmail.com',
            'course' : 'Ciberseguridad',
            'score' : 'nº1',
            'diplomaGenerar' : 'Diploma Comité Registro',
            'date':'01/01/2021'
        }))


    def on_quit(self):
        self.user = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Diplomas(HttpUser):
    host = HOST
    tasks = [DefDiploma]
    wait_time= between(3,5)