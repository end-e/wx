# -*-  coding:utf-8 -*-
# !/usr/bin/env python
from celery import Celery

app = Celery('tasks', broker='redis://localhost')


@app.tasks
def add(x, y):
    return x + y
