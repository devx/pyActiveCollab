#!/usr/bin/env python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab", log_level="info")
#print "... "
#print json.dumps(json.loads(ac.get_info()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_project_labels()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_assignment_labels()), indent=4,
#                 sort_keys=True)
#print json.dumps(json.loads(ac.get_roles()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_project_roles()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_people()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_projects()), indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_archived_projects()),
#                 indent=4, sort_keys=True)
#print "... "
#print json.dumps(json.loads(ac.get_status_messages()), indent=4, sort_keys=True)

print json.dumps(json.loads(ac.get_project(15)), indent=4, sort_keys=True)

print "Adding task to test project"
name = "Task Automatically created"
body = "This task was automatically added vi the api"
print json.dumps(json.loads(ac.add_task(15, name, body)), indent=4,
                 sort_keys=True)
