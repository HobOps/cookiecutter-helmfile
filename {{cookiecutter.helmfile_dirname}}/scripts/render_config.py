#!/usr/bin/env python
import os
import re
import tempfile
import yaml

#### Vars
path_releases = 'rendered/releases.yaml.gotmpl'

#### Functions
def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data"""
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def write_file(path, values):
    # Create directory
    directory = os.path.dirname(path)
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    # Write file
    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
    # with open(path, 'w') as outfile:
    with tempfile.NamedTemporaryFile(mode = "w+") as tempOutfile:
        yaml.dump(values, tempOutfile, default_flow_style=False, sort_keys=False)
        # Rewind
        tempOutfile.seek(0)
        # Replace placeholder with anchor
        with open(path, 'w') as outfile:
            for line in tempOutfile:
                outfile.write(line.replace("ANCHOR_PLACEHOLDER: ''", '<<: *default'))



# # Replace placeholders witn anchors
# with open (path_releases, 'r' ) as f:
#     content = f.read()
#     content_new = re.sub('(\d{2}|[a-yA-Y]{3})\/(\d{2})\/(\d{4})', r'\1-\2-\3', content, flags = re.M)

#### Load settings
with open("include/settings.yaml", "r") as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#### Create config file
data = dict()

# Repositories
data['repositories'] = list()
print('=========== Repositories ===========')
for key, value in settings['repositories'].items():
    data['repositories'].append(dict(
        name=key,
        url=value['url']
    ))
    print(key)

# Values
data['values'] = list()
print('=========== Values ===========')
for key, value in settings['charts'].items():
    temp = dict()
    temp[key] = dict(
        enabled=False
    )
    data['values'].append(temp)
    print(key)

# Releases
data['releases'] = list()
print('=========== Releases ===========')
for key, value in settings['charts'].items():
    temp = dict()

    # Name
    temp['name'] = key
    print(f"name: {key}")

    # Placeholder for anchor
    temp['ANCHOR_PLACEHOLDER'] = ''

    # Chart
    if 'chart' in value:
        temp['chart'] = value['chart']
    else:
        temp['chart'] = f"{settings['chartsPath']}/{key}/"

    # Condition
    temp['condition'] = f"{key}.enabled"

    # Version
    if 'version' in value:
        temp['version'] = value['version']
        print(f'version: {value["version"]}')

    # disableValidation
    if 'disableValidation' in value:
        temp['disableValidation'] = value['disableValidation']
        print(f'disableValidation: {value["disableValidation"]}')

    # disableValidationOnInstall
    if 'disableValidationOnInstall' in value:
        temp['disableValidationOnInstall'] = value['disableValidationOnInstall']
        print(f'disableValidationOnInstall: {value["disableValidationOnInstall"]}')

    # needs
    if 'needs' in value:
        temp['needs'] = value['needs']
        print(f'needs: {value["needs"]}')

    # namespace
    if 'namespace' in value:
        temp['namespace'] = value['namespace']
        print(f'namespace: {value["namespace"]}')

    data['releases'].append(temp)


    print('---')

#### Write file
# Write YAML
write_file(path_releases, data)
