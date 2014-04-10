#!/usr/bin/env python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab")
print "... "
print json.dumps(json.loads(ac.get_info()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_project_labels()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_assignment_labels()), indent=4,
                 sort_keys=True)
print json.dumps(json.loads(ac.get_roles()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_project_roles()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_people()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_projects()), indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_archived_projects()),
                 indent=4, sort_keys=True)
print "... "
print json.dumps(json.loads(ac.get_status_messages()), indent=4, sort_keys=True)
