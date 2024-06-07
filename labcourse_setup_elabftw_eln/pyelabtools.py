import json
import elabapi_python
from elabapi_python.rest import ApiException

__APICLIENT__ = None

def connect(host: str, apikey: str):
    """Connect to eLabFTW server API.
    
    Parameters
    ----------
    host : str
        URL to V2 api on the eLabFTW server, 
        e.g. https://server/api/v2.
    apikey : str
        API key to be used in order to access the eLabFTW data.

    Returns
    -------
    None.

    """
    
    global __APICLIENT__
    
    # configure elabftw access
    conf = elabapi_python.Configuration()
    conf.api_key['api_key'] = apikey
    conf.api_key_prefix['api_key'] = 'Authorization'
    conf.host = host
    conf.debug = False
    conf.verify_ssl = True
    
    # connect to api
    __APICLIENT__ = elabapi_python.ApiClient(conf)
    __APICLIENT__.set_default_header(header_name='Authorization', 
                                     header_value=apikey)
    
    
def disconnect():
    """Disconnect from the eLabFTW server API
    
    Returns
    -------
    None.

    """
    
    global __APICLIENT__
    __APICLIENT__ = None

    
def get_currentteam():
    global __APICLIENT__
    apiteams = elabapi_python.TeamsApi(__APICLIENT__)
    return apiteams.read_team('current')
    

def get_userid(email: str):
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)
    users = apiusers.read_users()
    
    userid = None
    for user in users:
        if user.email == email:
            userid = user.userid
            break    
    
    return userid


def get_users():
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)

    return apiusers.read_users()


def get_user(userid: int):
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)

    return apiusers.read_user(userid)


def add_user_to_team(userid: int):
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)
    
    teamid = get_currentteam().id
    try:
        apiusers.patch_user(userid, body={'action': 'add', 'team': teamid})
    except ApiException as e:
        print('Error: userid ' + str(userid) + ' could not be added to team.')

    
def create_user_in_team(firstname: str, lastname: str, email: str):
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)
    
    user = {'firstname': firstname, 'lastname': lastname, 'email': email}
    userid = None
    try:
        response = apiusers.post_user_with_http_info(body=user)
        userid = int(response[2].get('Location').split('/').pop())
    except ApiException as e:
        if 'Someone is already using that email address' in str(e.body):
            userid = get_userid(email)
            add_user_to_team(userid)
        else:
            print('Error: user ' + email + ' could not be created.')
            
    return userid


def change_user_email(userid: int, email: str):
    # requires sysadmin rights
    global __APICLIENT__
    apiusers = elabapi_python.UsersApi(__APICLIENT__)
    
    apiusers.patch_user(userid, body={'email': email})


def create_group(groupname: str):
    global __APICLIENT__
    apigroups = elabapi_python.TeamgroupsApi(__APICLIENT__)
    
    teamid = get_currentteam().id
    response = apigroups.post_teamgroups_with_http_info(teamid, body={'name': groupname})
    
    return int(response[2].get('Location').split('/').pop())


def delete_group(groupid: int):
    global __APICLIENT__
    apigroups = elabapi_python.TeamgroupsApi(__APICLIENT__)
    
    teamid = get_currentteam().id
    apigroups.delete_teamgroup(teamid, groupid)


def get_groupid(name: str):
    global __APICLIENT__
    apigroups = elabapi_python.TeamgroupsApi(__APICLIENT__)
    
    teamid = get_currentteam().id
    groups = apigroups.read_team_teamgroups(teamid)
    
    groupid = None
    for group in groups:
        if group.name == name:
            groupid = group.id
            break
            
    return groupid


def get_groups():
    global __APICLIENT__
    apigroups = elabapi_python.TeamgroupsApi(__APICLIENT__)
    
    teamid = get_currentteam().id
    groups = apigroups.read_team_teamgroups(teamid)
    
    return groups

    
def add_user_to_group(groupid: int, userid: int):
    global __APICLIENT__
    apigroups = elabapi_python.TeamgroupsApi(__APICLIENT__)

    teamid = get_currentteam().id
    
    apigroups.patch_teamgroup(teamid, groupid, body={'how': 'add', 'userid': userid})


def create_experiment_category(name: str, color: str, default: bool=False):
    global __APICLIENT__
    apicategories = elabapi_python.ExperimentsCategoriesApi(__APICLIENT__)

    teamid = get_currentteam().id
    apicategories.post_team_one_expcat(teamid, body={'name': name, 'color': color, 'default': (1 if default else 0)})


def get_experiment_categories():
    global __APICLIENT__
    apicategories = elabapi_python.ExperimentsCategoriesApi(__APICLIENT__)

    teamid = get_currentteam().id
    response = apicategories.read_team_experiments_categories(teamid)
    return response


def get_experiment_categoryid(name: str):
    categories = get_experiment_categories()
    for category in categories:
        if category.title == name:
            return category.id
    return None


def delete_experiment_category(id: int):
    global __APICLIENT__
    apicategories = elabapi_python.ExperimentsCategoriesApi(__APICLIENT__)

    teamid = get_currentteam().id
    apicategories.delete_expcat(teamid, id)
        

def delete_all_experiment_categories():
    categories = get_experiment_categories()
    for category in categories:
        delete_experiment_category(category.id)


def create_experiment_status(name: str, color: str, default: bool=False):
    global __APICLIENT__
    apistatus = elabapi_python.ExperimentsStatusApi(__APICLIENT__)

    teamid = get_currentteam().id
    apistatus.post_team_one_expstatus(teamid, body={'name': name, 'color': color, 'default': (1 if default else 0)})


def read_experiment_status(id: int):
    global __APICLIENT__
    apistatus = elabapi_python.ExperimentsStatusApi(__APICLIENT__)

    teamid = get_currentteam().id
    response = apistatus.read_team_one_expstatus(teamid, id)
    return response


def get_experiment_statuses():
    global __APICLIENT__
    apistatus = elabapi_python.ExperimentsStatusApi(__APICLIENT__)

    teamid = get_currentteam().id
    response = apistatus.read_team_experiments_status(teamid)
    return response


def get_experiment_statusid(name: str):
    statuses = get_experiment_statuses()
    for status in statuses:
        if status.title == name:
            return status.id
    return None


def delete_experiment_status(id: int):
    global __APICLIENT__
    apistatus = elabapi_python.ExperimentsStatusApi(__APICLIENT__)

    teamid = get_currentteam().id
    apistatus.delete_expstatus(teamid, id)
        

def delete_all_experiment_statuses():
    statuses = get_experiment_statuses()
    for status in statuses:
        delete_experiment_status(status.id)


def create_template_step(templateid: int, name: str):
    global __APICLIENT__
    apisteps = elabapi_python.StepsApi(__APICLIENT__)

    apisteps.post_step('experiments_templates', templateid, body={'body': name})


def create_template(template_json):
    global __APICLIENT__
    apitemplates = elabapi_python.ExperimentsTemplatesApi(__APICLIENT__)

    response = apitemplates.post_experiment_template_with_http_info(body={'title': template_json['title']})
    templateid = int(response[2].get('Location').split('/').pop())

    if 'steps' in template_json:
        steps_json = template_json['steps']
        del template_json['steps']
    else:
        steps_json = None

    apitemplates.patch_experiment_template(templateid, body=template_json)

    if steps_json is not None:
        for step in steps_json:
            create_template_step(templateid, step['body'])

    return templateid


def get_templateid(title: str):
    global __APICLIENT__
    apitemplates = elabapi_python.ExperimentsTemplatesApi(__APICLIENT__)
    
    templates = apitemplates.read_experiments_templates()
    
    templateid = None
    for template in templates:
        if template.title == title:
            templateid = template.id
            break
            
    return templateid
    

def create_experiment_from_template(templateid: int, title: str, tags, groups_readaccess, groups_writeaccess):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)
    
    response = apiexperiments.post_experiment_with_http_info(body={'category_id': templateid, 'tags': tags})
    expid = int(response[2].get('Location').split('/').pop())
    
    canread = json.dumps({"base": 20, "teams": [], "users": [], "teamgroups": groups_readaccess})
    canwrite = json.dumps({"base": 20, "teams": [], "users": [], "teamgroups": groups_writeaccess})
    apiexperiments.patch_experiment(expid, body={'title': title, 'canread': canread, 'canwrite': canwrite})
    
    return expid


def update_experiment(expid: int, fieldname: str, value):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)

    apiexperiments.patch_experiment(expid, body={fieldname: value})
    
    
def link_experiment_to_experiment(expid: int, linkid: int):
    global __APICLIENT__
    apilinks = elabapi_python.LinksToExperimentsApi(__APICLIENT__)
    
    apilinks.post_entity_experiments_links('experiments', expid, linkid)


def update_experiment_metadata(expid: int, fieldname: str, value: str):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)

    apiexperiments.patch_experiment(expid, body={'action': 'updatemetadatafield', fieldname: value})


def delete_experiment(expid: int):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)
    
    apiexperiments.delete_experiment(expid)
    
    
def get_experiments(searchstr: str=''):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)
    
    return apiexperiments.read_experiments(q=searchstr, limit=9999)


def get_experiment(expid: int):
    global __APICLIENT__
    apiexperiments = elabapi_python.ExperimentsApi(__APICLIENT__)
    
    return apiexperiments.get_experiment(expid)
