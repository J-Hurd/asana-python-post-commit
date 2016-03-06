#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright (c) 2016 Floyd Hightower (https://github.com/fhightower)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------
# Written: 10.24.2015

"""This is a python git hook (post-commit) script that closes a given asana task.  This code was developed based on the bash script version available here: https://github.com/Spaceman-Labs/asana-post-commit."""

import os
import re
import requests

from git import *

git_config_file_directory = "/PATH/TO/GIT/CONFIG/.gitconfig"
bitbucket_repo_directory = "</PATH/TO/REPOSITORY/>"

"""Get the asana api token from the .gitconfig file"""
#(the form in the config file is: asana-token = xyzpdqxyzpdq...)
with open(git_config_file_directory) as f:
    for line in f:
        if "asana-token" in line.strip():
            api_token = line.strip().split("= ")[1]

"""Set regex patterns for matching commit statements"""
# regex pattern to recognize a story number
taskid_pattern = '#([0-9]*)'
# regex pattern to recognize a "closing this ticket" word
closes_pattern = '([Ff]ix|[Cc]lose|[Cc]losing)'
# regex pattern to recognize an "and" word (eg "fixes #1, #2, and #3")
and_pattern = '([Aa]nd|&)'

"""Get the previous commit statement from the git log"""
repo = Repo(bitbucket_repo_directory)
commit_message = repo.heads[0].commit.message

"""Break the commit statement into words"""
words = commit_message.split()

"""Find all tasks referenced in the commit statement"""
closed = []
referenced = []
close = False

for word in words:
    # if the word is a task id, save it in the appropriate list
    result = re.findall(taskid_pattern, word)
    if (result):
        # if we are closing this task, add it to the closes list
        if (close == True):
            closed.append(result[0])
        # add the task to referenced list
        referenced.append(result[0])
    # if the word signals a closure to follow, set close to True
    elif (re.match(closes_pattern, word)):
        close = True
    # as long as the word is NOT 'and' we set close to False
    # if the input is 'and,' then skip this step and keep the state as it was
    elif (not re.match(and_pattern, word)):
        close = False

# designate the authentication to asana
auth = "Bearer " + api_token

"""Touch the stories of the tasks referenced in the commit statement (add a comment to the task)"""
for task in referenced:
    url = "https://app.asana.com/api/1.0/tasks/" + task + "/stories"
    data = {"text": commit_message}
    try:
        requests.post(url, headers={'Authorization': auth}, data=data)
    except Exception as e:
        pass

"""Close tasks that have been fixed"""
for task in closed:
    url = "https://app.asana.com/api/1.0/tasks/" + task
    data = {"completed": "true"}
    try:
        requests.put(url, data=data, headers={'Authorization': auth})
    except Exception as e:
        pass
