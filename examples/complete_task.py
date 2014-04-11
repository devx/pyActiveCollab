#!/usr/bin/env python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab", log_level="info")

print json.dumps(json.loads(ac.complete_task(15, 18)), indent=4,
                 sort_keys=True)
