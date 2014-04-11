#!/usr/bin/env python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab", log_level="info")
#print json.dumps(json.loads(ac.get_project(15)), indent=4, sort_keys=True)

print "Adding task to test project"
name = "Task Automatically created test 3"
body = "This task was automatically added vi the api"
print json.dumps(json.loads(ac.add_task(15, name, body)), indent=4,
                 sort_keys=True)
