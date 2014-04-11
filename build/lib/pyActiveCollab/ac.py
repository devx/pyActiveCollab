#import json
import requests
import os
import logging
from pprint import pprint


class activeCollab(object):
    """
    This library interacts with Active Collab 3.x/4.x.
    """

    _USER_NAME = None
    _API_KEY = None
    _URL = None

    def __init__(self, config=None, key=None, user_name=None,
                 url=None, log_level="error", log_file=""):
        """
        Initialize an object to load authentication information and the
        endpoint
        """
        LOGGING_LEVELS = {'critical': logging.CRITICAL,
                          'error': logging.ERROR,
                          'warning': logging.WARNING,
                          'info': logging.INFO,
                          'debug': logging.DEBUG}
        loglevel = LOGGING_LEVELS.get(log_level, logging.NOTSET)

        logging.basicConfig(level=loglevel, filename=log_file,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing %s" % __name__)

        if config:
            self.load_config(config)
        elif None in (key, user_name, url):
            pprint("We could not set your keys")
        else:
            self._API_KEY = key
            self._USER_NAME = user_name
            self._URL = url

    def load_config(self, config_file):
        """
        Reads and parses a config file that is provided,  If no file path is
        pass it will look for the file in "~/.ActiveCollab".
        """

        import ConfigParser

        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.expanduser(config_file)))
            self._API_KEY = config.get('config', 'KEY')
            self._USER_NAME = config.get('config', 'USER')
            self._URL = config.get('config', 'URL')
        except:
            pprint("Could not parse your config file")
            pass

    def call_api(self, ac_method, parameters=None):
        ac_url = (self._URL + "?auth_api_token=" + self._API_KEY +
                  "&path_info=" + ac_method + "&format=json")
        if parameters:
            r = requests.post(ac_url, data=parameters)
            self.log(str(ac_method), r)
        else:
            r = requests.get(ac_url)
            self.log(str(ac_method), r)
        return r.text

    def get_info(self):
        """
        Returns system information about the installation you are working with.
        This information includes system versions; info about logged in users;
        the mode the API is in etc.
        """
        return self.call_api('info')

    def get_project_labels(self):
        """
        Lists all available project labels.
        """
        return self.call_api('info/labels/project')

    def get_assignment_labels(self):
        """
        Lists all available assignment labels. These labels are used by tasks
        and subtasks.
        """
        return self.call_api('info/labels/assignment')

    def get_roles(self):
        """
        Lists all system roles and role details (permissions included).
        """
        return self.call_api('info/roles')

    def get_project_roles(self):
        """
        Lists all project roles and displays their permissions.
        """
        return self.call_api('info/roles/project')

    def get_people(self):
        """
        Lists all active companies that are defined in People section.
        """
        return self.call_api('people')

    def add_company(self, name):
        """
        This command will create a new company. If operation was successful,
        system will return details of the newly created company.
        """
        params = {
            'status_update[name]': name,
            'submitted': 'submitted'
        }
        return self.call_api('people/add-company', params)

    # Untested queries

    def get_company(self, company_id):
        """
        Displays the properties of a specific company.
        """
        return self.call_api('people/%s' % company_id)

    def get_user(self, company_id, user_id):
        """
        Shows details of a specific user account.
        """
        return self.call_api('people/%s/users/%s' % (company_id, user_id))

    def get_projects(self):
        """
        Display all, non-archived projects that this user has access to.
        In case of administrators and project managers, system will return
        all non-archived projects and properly populate is_member flag value
        (when 0, administrator and project manager can see and manage the
        project, but they are not
        directly involved with it).
        """
        return self.call_api('projects')

    def get_archived_projects(self):
        """
        Display all archived projects that this user has access to. In case of
        administrators and project managers, system will return all archived
        projects and properly populate is_member flag value (when 0,
        administrator and project manager can see and manage the project, but
        they are not directly involved with it).
        """
        return self.call_api('projects/archive')

    def get_project(self, project_id):
        """
        Shows properties of the specific project.
        """
        return self.call_api('projects/%s' % project_id)

    def get_project_people(self, project_id):
        """
        Displays the list of people involved with the project and the
        permissions included in their Project Role. Project Permissions are
        organized per module and have four possible values:

        0 - no access;
        1 - has access, but can't create or manage objects;
        2 - has access and permission to create objects in a given module;
        3 - has access, creation and management permissions in a given module.
        """
        return self.call_api('projects/%s/people' % project_id)

    def get_project_tasks(self, project_id):
        """
        Lists all open and completed, non-archived tasks from a project.
        project_id can be a project ID.

        Tasks
        Task fields:

        name (string) - Task name. A value for this field is required when
            a Task is created,
        body (text) - Full task description,
        visibility (integer) - Object visibility. 0 is private and 1 is normal
            visibility,
        category_id (integer) - Object category,
        label_id (integer) - Object label,
        milestone_id (integer) - ID of the parent milestone,
        priority (integer) - Priority can have one of five integer values,
        ranging from -2 (lowest) to 2 (highest). 0 is normal,
        assignee_id (integer) - User assigned to the Task,
        other_assignees (array) - People assigned to the Task,
        due_on (date) - Task due date,``
        """
        return self.call_api('/projects/%s/tasks' % project_id)

    def get_archived_project_tasks(self, project_id):
        """
        Displays all archived tasks from this project.
        project_id can be a project ID.
        """
        return self.call_api('/projects/%s/tasks/archive' % project_id)

    def add_task(self, project_id, name, body=None):
        """
        Create a new task in the given project.
        """
        params = {
            'task[name]': name,
            'task[body]': body,
            'submitted': 'submitted'
        }
        return self.call_api('/projects/%s/tasks/add' % project_id, params)

    def complete_task(self, project_id, task_id):
        """
        Complete task in the project.
        """
        params = {
            'submitted': 'submitted'
        }
        return self.call_api('/projects/%s/tasks/%s/complete' %
                            (project_id, task_id), params)

    def get_tasks(self, project_id):
        """
        Displays all task for a specific project
        """
        return self.call_api('/projects/%s/tasks' % project_id)

    def get_task(self, project_id, task_id):
        """
        Displays details for a specific task.
        """
        return self.call_api('/projects/%s/tasks/%s' % (project_id, task_id))

    def get_discussions(self, project_id):
        """ discussions
        Discussion fields:

        name (string) - Discussion topic. This field is required when topic
        is created,
        body (string) - First message body (required),
        category_id (integer) - Discussion category id,
        visibility (integer) - Discussion visibility. 0 is private and 1 is
        normal visibility,
        milestone_id (integer) - ID of parent milestone.

        Displays all non-archived discussions in a project.
        """
        return self.call_api('/projects/%s/discussions')

    def get_discussion(self, project_id, discussion_id):
        """
        Display discussion details.
        """
        return self.call_api('/projects/%s/discussions/%s' %
                            (project_id, discussion_id))

    def get_times_and_expenses_by_project(self, project_id, limit=0):
        """
        Time & Expenses

        This command will display last 300 time records and expenses in a
            given project. If you wish to return all time records and expenses
            from a project, set limit to 1.
        """
        return self.call_api('projects/%s/tracking&dont_limit_result=%s' %
                             (project_id, limit))

    def add_time_to_project(self, project_id, value, user_id, record_date,
                            job_type_id):
        """
        Adds a new time record to the time log in a defined project.
        """
        params = {
            'time_record[value]': value,
            'time_record[user_id]': user_id,
            'time_record[record_date]': record_date,
            'time_record[job_type_id]': job_type_id,
            'submitted': 'submitted',
        }
        return self.call_api('projects/%s/tracking/time/add' %
                             project_id, params)

    def add_time_to_task(self, project_id, task_id, value, user_id,
                         record_date, job_type_id, billable_status, summary):
        """
        Adds a new time record to the time log in a defined project
            task.
        """
        params = {
            'time_record[value]': value,
            'time_record[user_id]': user_id,
            'time_record[record_date]': record_date,
            'time_record[job_type_id]': job_type_id,
            'time_record[billable_status]': billable_status,
            'time_record[summary]': summary,
            'submitted': 'submitted',
        }
        return self.call_api('projects/%s/tasks/%s/tracking/time/add' %
                            (project_id, task_id), params)

    def get_time_record(self, project_id, record_id):
        """
        Displays time record details.
        """
        return self.call_api('projects/%s/tracking/time/%s' %
                            (project_id, record_id))

    def get_status_messages(self):
        """
        Lists the 50 most recent status messages.
        """
        return self.call_api('status')

    def add_status_message(self, message):
        """
        This command will submit a new status message.
        Example request:
            status_update[message]=New status message
            submitted=submitted
        """
        params = {
            'status_update[message]': message,
            'submitted': 'submitted'
        }
        return self.call_api('status/add', params)

    def get_subtasks(self, project_id):
        """
        Subtasks
        List of available subtask fields:

        body (text) - The subtasktask name. A value for this field is required
        when a new task is added;
        assignee (integer) - Person assigned to the object.
        priority (integer) - Priority can have five integer values ranging from
        -2 (lowest) to 2 (highest). 0 is normal;
        label_id (date) - Label id of the subtask;
        due_on (date) - When the subtask is due;

        Displays all subtasks for a given project object in a specific
        project.
        """
        return self.call_api('/projects/%s/subtasks' % project_id)

    def get_subtask(self, project_id, subtask_id):
        """
        Displays subtask details.
        """
        return self.call_api('/projects/%s/subtasks/%s' %
                            (project_id, subtask_id))

    def add_comment(self, context, message):
        """
        Comments
        """
        params = {
            'comment[body]': message,
            'submitted': 'submitted'
        }
        return self.call_api('%s/comments/add' % context, params)

    def add_comment_to_task(self, project_id, task_id, message):
        """
        Add comment to task.
        """
        context = '/projects/%s/tasks/%s' % (project_id, task_id)
        return self.add_comment(context, message)

    def get_comments(self, project_id, task_id):
        return self.call_api('/projects/%s/tasks/%s/comments' %
                            (project_id, task_id))

    def log(self, pre_pend, response):
        self.logger.info(pre_pend + " : HTTP RESPONSE CODE - " +
                         str(response.status_code))
        self.logger.info(pre_pend + " : " + str(response.url))
        self.logger.debug(pprint(response.url))
