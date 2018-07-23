#!/usr/bin/python

# Copyright (c) 2018 Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: ftd_bridge_group_interface
short_description: Manages BridgeGroupInterface objects on Cisco FTD devices
version_added: "2.7"
author: "Cisco Systems, Inc."
options:
  operation:
    description:
      - Specified the name of the operation to execute in the task.
    required: true
  register_as:
    description:
      - Specifies Ansible fact name that is used to register received response from the FTD device.
  bridgeGroupId
    description:
      - For Internal use.
  description
    description:
      - An optional UTF-8 sting, from 0 to 200 characters. The string cannot include HTML tags, semi-colons(;), or carriage returns.<br>Field level constraints: length must be between 0 and 200 (inclusive), must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  filter
    description:
      - The criteria used to filter the models you are requesting. It should have the following format: {field}{operator}{value}[;{field}{operator}{value}]. Supported operators are: "!"(not equals), ":"(equals), "<"(null), "~"(similar), ">"(null). Supported fields are: "name".
  hardwareName
    description:
      - A mandatory UTF-8 string for the PhysicalInterfaces and SubInterfaces, which normally specifies the type of Interface along with the Interface number. The string cannot contain HTML tags.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  id
    description:
      - A unique string identifier assigned by the system when the object is created. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete (or reference) an existing object.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  ipv4
    description:
      - An optional IPv4 object assigned to an interface in Firepower Device Manager. This object specifies Interface configuration for an IPv4 address.
  ipv6
    description:
      - An optional IPv6 object assigned to an interface in Firepower Device Manager. This object specifies Interface configuration for an IPv6 address.
  limit
    description:
      - An integer representing the maximum amount of objects to return. If not specified, the maximum amount is 10
  monitorInterface
    description:
      - A mandatory boolean object which specifies if the Interface needs to be monitored or not.<br>Field level constraints: cannot be null. (Note: Additional constraints might exist)
  name
    description:
      - An optional ASCII string, from 0 to 48 characters, representing the name of the interface. The string can only include lower case characters (a-z), numbers (0-9), underscore (_), dot (.), and plus/minus (+,-). The name can only start with an alpha numeric character.
  offset
    description:
      - An integer representing the index of the first requested object. Index starts from 0. If not specified, the returned objects will start from index 0
  selectedInterfaces
    description:
      - A set of zero/one or more Physical Interfaces, objects that are grouped together to form a bridge group.<br>Allowed types are: [PhysicalInterface, SubInterface]
  sort
    description:
      - The field used to sort the requested object list
  type
    description:
      - A UTF8 string, all letters lower-case, that represents the class-type. This corresponds to the class name.
  version
    description:
      - A unique string version assigned by the system when the object is created or modified. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete an existing object. As the version will change every time the object is modified, the value provided in this identifier must match exactly what is present in the system or the request will be rejected.
"""

EXAMPLES = """
- name: Fetch BridgeGroupInterface with a given name
  ftd_bridge_group_interface:
    operation: "getBridgeGroupInterfaceByName"
    name: "Ansible BridgeGroupInterface"

- name: Create a BridgeGroupInterface
  ftd_bridge_group_interface:
    operation: 'addBridgeGroupInterface'
    description: "From Ansible with love"
    name: "Ansible BridgeGroupInterface"
    type: "bridgegroupinterface"
"""

RETURN = """
response:
  description: HTTP response returned from the API call.
  returned: success
  type: dict
error_code:
  description: HTTP error code returned from the server.
  returned: error
  type: int
msg:
  description: Error message returned from the server.
  returned: error
  type: dict
"""
import json

from ansible.module_utils.basic import AnsibleModule, to_text
from ansible.module_utils.http import iterate_over_pageable_resource
from ansible.module_utils.misc import dict_subset, construct_module_result, copy_identity_properties
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.connection import Connection


class BridgeGroupInterfaceResource(object):

    def __init__(self, conn):
        self._conn = conn

    def addBridgeGroupInterface(self, params):
        body_params = dict_subset(params, ['bridgeGroupId', 'description', 'hardwareName', 'id', 'ipv4', 'ipv6', 'monitorInterface', 'name', 'selectedInterfaces', 'type', 'version'])

        return self._conn.send_request(
            url_path='/devices/default/bridgegroupinterfaces',
            http_method='POST',
            body_params=body_params,
        )

    def deleteBridgeGroupInterface(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/devices/default/bridgegroupinterfaces/{objId}',
            http_method='DELETE',
            path_params=path_params,
        )

    def editBridgeGroupInterface(self, params):
        path_params = dict_subset(params, ['objId'])
        body_params = dict_subset(params, ['bridgeGroupId', 'description', 'hardwareName', 'id', 'ipv4', 'ipv6', 'monitorInterface', 'name', 'selectedInterfaces', 'type', 'version'])

        return self._conn.send_request(
            url_path='/devices/default/bridgegroupinterfaces/{objId}',
            http_method='PUT',
            body_params=body_params,
            path_params=path_params,
        )

    def getBridgeGroupInterface(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/devices/default/bridgegroupinterfaces/{objId}',
            http_method='GET',
            path_params=path_params,
        )

    def getBridgeGroupInterfaceList(self, params):
        query_params = dict_subset(params, ['filter', 'limit', 'offset', 'sort'])

        return self._conn.send_request(
            url_path='/devices/default/bridgegroupinterfaces',
            http_method='GET',
            query_params=query_params,
        )

    def getBridgeGroupInterfaceByName(self, params):
        search_params = params.copy()
        search_params['filter'] = 'name:%s' % params['name']
        item_generator = iterate_over_pageable_resource(self.getBridgeGroupInterfaceList, search_params)
        return next(item for item in item_generator if item['name'] == params['name'])

    def upsertBridgeGroupInterface(self, params):
        def is_duplicate_name_error(err):
            err_msg = to_text(err.read())
            return err.code == 422 and "Validation failed due to a duplicate name" in err_msg

        try:
            return self.addBridgeGroupInterface(params)
        except HTTPError as e:
            if is_duplicate_name_error(e):
                existing_object = self.getBridgeGroupInterfaceByName(params)
                params = copy_identity_properties(existing_object, params)
                return self.editBridgeGroupInterface(params)
            else:
                raise e

    def editBridgeGroupInterfaceByName(self, params):
        existing_object = self.getBridgeGroupInterfaceByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.editBridgeGroupInterface(params)

    def deleteBridgeGroupInterfaceByName(self, params):
        existing_object = self.getBridgeGroupInterfaceByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.deleteBridgeGroupInterface(params)


def main():
    fields = dict(
        operation=dict(type='str', default='upsertBridgeGroupInterface', choices=['addBridgeGroupInterface', 'deleteBridgeGroupInterface', 'editBridgeGroupInterface', 'getBridgeGroupInterface', 'getBridgeGroupInterfaceList', 'getBridgeGroupInterfaceByName', 'upsertBridgeGroupInterface', 'editBridgeGroupInterfaceByName', 'deleteBridgeGroupInterfaceByName']),
        register_as=dict(type='str'),

        bridgeGroupId=dict(type='int'),
        description=dict(type='str'),
        filter=dict(type='str'),
        hardwareName=dict(type='str'),
        id=dict(type='str'),
        ipv4=dict(type='str'),
        ipv6=dict(type='str'),
        limit=dict(type='int'),
        monitorInterface=dict(type='bool'),
        name=dict(type='str'),
        objId=dict(type='str'),
        offset=dict(type='int'),
        selectedInterfaces=dict(type='list'),
        sort=dict(type='str'),
        type=dict(type='str'),
        version=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=fields)
    params = module.params

    try:
        conn = Connection(module._socket_path)
        resource = BridgeGroupInterfaceResource(conn)

        resource_method_to_call = getattr(resource, params['operation'])
        response = resource_method_to_call(params)

        result = construct_module_result(response, params)
        module.exit_json(**result)
    except HTTPError as e:
        err_msg = to_text(e.read())
        module.fail_json(changed=False, msg=json.loads(err_msg) if err_msg else {}, error_code=e.code)
    except Exception as e:
        module.fail_json(changed=False, msg=str(e))


if __name__ == '__main__':
    main()
