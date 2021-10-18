# pylint: disable=C0301
"""
############### Admin.py ################
A file for the admin functions like admin/userpermission/change

"""

import constants as const
from error import AccessError, InputError
from server_data_class import Server_data

from auth import auth_register

def admin_userpermission_change(server_data, token, u_id, permission_id):
    """
    admin_userpermission_change
    A function that takes in the server_data and necessary informations,
    determines if they are valid and change the target user's permission
    in the server_data

    Input:
    - (str) token
    - (str) u_id
    - (int) permission_id

    Output:
    - {}
    """
    # Check for any input/access errors
    if not server_data.does_user_exist(u_id):
        raise InputError(description="u_id does not exist")

    if not permission_id in (const.PERMISSION_GLOBAL_OWNER, const.PERMISSION_GLOBAL_MEMBER):
        raise InputError(description="permission_id does not exist")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Token invalid")

    # Obtain u_id from the token
    u_id_from = session_obj.get_token_user(token)
    user_obj_from = server_data.get_user_by_id(u_id_from)
    if user_obj_from.global_permission_id != const.PERMISSION_GLOBAL_OWNER:
        raise AccessError(description="User is not an owner")

    # All errors checks out, perform action
    user_obj = server_data.get_user_by_id(u_id)
    user_obj.global_permission_id = permission_id

    return {}


if __name__ == "__main__":
    SERVER_DATA = Server_data()
    RT1 = auth_register(SERVER_DATA, "steven@gmail.com", "1234567", "as", "ad")
    RT2 = auth_register(SERVER_DATA, "richard@gmail.com", "1234567", "a1", "ad")

    admin_userpermission_change(SERVER_DATA, RT1["token"], RT2["u_id"], const.PERMISSION_GLOBAL_OWNER)

    USER = SERVER_DATA.get_user_by_id(RT2["u_id"])
    print(USER.global_permission_id)
