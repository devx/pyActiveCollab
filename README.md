pyActiveCollab
==============

Python bindings for Active Collab 3.x/4.x


### Example
List system information
```python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab")
print json.dumps(json.loads(ac.get_info()), indent=4, sort_keys=True)
```

# Change log level
To change the log level just initialialize your object with info, error, debug
```python
import pyActiveCollab as pyac
import json

ac = pyac.activeCollab("~/.activeCollab", log_level="debug")
print json.dumps(json.loads(ac.get_info()), indent=4, sort_keys=True)
```

# References

PHP API documentation:
  * https://activecollab.com/help/books/api/index.html
