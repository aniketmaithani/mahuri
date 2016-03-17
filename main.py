#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Author : Samar Acharya

from locust import HttpLocust, TaskSet, task, events
import logging
from logging.handlers import RotatingFileHandler
import json
import random
import os
import time

BACK_UP_COUNT = 20
MAX_LOG_BYTES = 1024 * 1024 * 5
LOG_PATH = "/tmp"
filename = "requests_success.log"
success_handler = RotatingFileHandler(filename=os.path.join(LOG_PATH, filename), maxBytes=MAX_LOG_BYTES*10, backupCount=BACK_UP_COUNT, delay=1)

formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
formatter.converter = time.gmtime
success_handler.setFormatter(formatter)

success_logger = logging.getLogger('request.success')
success_logger.propagate = False
success_logger.addHandler(success_handler)
with open("./config.json", "r") as f:
    config = f.read()
config = json.loads(config)


class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.perform_setup()

    def on_start(self):
        """ runs when the load test starts before any task is scheduled"""
        # self.run_get_tests()
        # self.run_post_tests()
        self.schedule_task(self.run_get_tests)
        self.schedule_task(self.run_post_tests)

    def success_request(request_type, name, response_time, response_length):
        """
        The format of data written is:
        DATETIME | LOGGER NAME | LOG LEVEL | HTTP METHOD TYPE | REQUEST NAME | RESPONSE TIME | RESPONSE LENGTH
        """
        msg = ' | '.join([str(request_type), name, str(response_time), str(response_length)])
        success_logger.error(msg)


    events.request_success += success_request

    def perform_setup(self):
        self.host = config.get("host", "")
        self.token = config.get("token", None)
        gets = config.get("gets", None)
        self.get_urls = []
        # ToDo: Add feature for replacing params and making dynamic requests
        params = config.get("params", None)

        if gets:
            for get in gets:
                abs_url = self.host + get
                self.get_urls.append(abs_url)

            # for param in params:
            #     if isinstance(param, list):
            #         for replace in params[param]:
            #             search = "{%s}" % (param)

        posts = config.get("posts", None)
        self.post_urls = []
        if posts:
            for post in posts:
                if not post.get("endpoint", None):
                    continue
                abs_url = self.host + post.get("endpoint")
                body_file = post.get("bodyFile", None)
                body = post.get("body", None)
                if body_file and os.path.isfile(body_file):
                    with open(body_file, 'r') as f:
                        body = f.read()

                content_type = post.get("content-type", None)
                if not content_type or not body:
                    continue
                if content_type == "application/json":
                    payload = json.dumps(json.loads(body))
                elif content_type == "application/x-www-form-urlencoded":
                    payload = post.get("payload", None)
                    if not payload:
                        continue

                elif content_type == "multipart/form-data":
                    payload = post.get("payload", None)
                    if not payload:
                        continue

                    key = payload.keys()[0]
                    file_to_upload = payload.values()[0]
                    # continue if there's no such file
                    if not os.path.isfile(file_to_upload):
                        continue
                    payload = {key: open(file_to_upload, 'rb')}

                self.post_urls.append({"url": abs_url, "payload": payload,
                                       "headers": {"Authorization": self.token,
                                                    "Content-Type": content_type
                                                  }
                                      })

        puts = config.get("puts", None)
        self.put_urls = []
        if puts:
            for put in puts:
                if not put.get("endpoint", None):
                    continue
                abs_url = self.host + put.get("endpoint")
                body_file = put.get("bodyFile", None)
                body = put.get("body", None)
                if body_file and os.path.isfile(body_file):
                    with open(body_file, 'r') as f:
                        body = f.read()

                content_type = put.get("content-type", None)
                if not content_type or not body:
                    continue
                if content_type == "application/json":
                    payload = json.dumps(json.loads(body))
                elif content_type == "application/x-www-form-urlencoded":
                    payload = put.get("payload", None)
                    if not payload:
                        continue

                elif content_type == "multipart/form-data":
                    payload = put.get("payload", None)
                    if not payload:
                        continue

                    key = payload.keys()[0]
                    file_to_upload = payload.values()[0]
                    # continue if there's no such file
                    if not os.path.isfile(file_to_upload):
                        continue
                    payload = {key: open(file_to_upload, 'rb')}

                self.put_urls.append({"url": abs_url, "payload": payload,
                                       "headers": {"Authorization": self.token,
                                                    "Content-Type": content_type
                                                  }
                                      })

        deletes = config.get("deletes", None)
        self.delete_urls = []
        if deletes:
            for delete in deletes:
                if not delete.get("endpoint", None):
                    continue
                abs_url = self.host + delete.get("endpoint")
                body_file = delete.get("bodyFile", None)
                body = delete.get("body", None)
                if body_file and os.path.isfile(body_file):
                    with open(body_file, 'r') as f:
                        body = f.read()

                content_type = delete.get("content-type", None)
                if not content_type or not body:
                    continue
                if content_type == "application/json":
                    payload = json.dumps(json.loads(body))
                elif content_type == "application/x-www-form-urlencoded":
                    payload = post.get("payload", None)
                    if not payload:
                        continue

                elif content_type == "multipart/form-data":
                    payload = delete.get("payload", None)
                    if not payload:
                        continue

                    key = payload.keys()[0]
                    file_to_upload = payload.values()[0]
                    # continue if there's no such file
                    if not os.path.isfile(file_to_upload):
                        continue
                    payload = {key: open(file_to_upload, 'rb')}

                self.delete_urls.append({"url": abs_url, "payload": payload,
                                       "headers": {"Authorization": self.token,
                                                    "Content-Type": content_type
                                                  }
                                      })

    @task(100)
    def run_get_tests(self):
        if not self.get_urls:
            return
        r = self.client.get(random.choice(self.get_urls),
                            headers={"Authorization": self.token}
                            )

    @task(100)
    def run_post_tests(self):
        if not self.post_urls:
            return
        rand_post_url = random.choice(self.post_urls)
        r = self.client.post(rand_post_url.get("url"),
                            data=rand_post_url.get("payload"),
                            headers=rand_post_url.get("headers")
                            )

    @task(100)
    def run_put_tests(self):
        if not self.put_urls:
            return
        rand_post_url = random.choice(self.put_urls)
        r = self.client.put(rand_post_url.get("url"),
                            data=rand_post_url.get("payload"),
                            headers=rand_post_url.get("headers")
                            )

    @task(100)
    def run_delete_tests(self):
        if not self.delete_urls:
            return
        rand_delete_url = random.choice(self.delete_urls)
        r = self.client.delete(rand_delete_url.get("url"),
                            data=rand_delete_url.get("payload"),
                            headers=rand_delete_url.get("headers")
                            )

class ApiLocust(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 1000
    host = config.get("host", None)
