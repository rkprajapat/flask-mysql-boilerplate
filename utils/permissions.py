from utils.rules import VisitorRule, UserRule, AdminRule
from flask import session


class Permission:
    def check_permission(self):
        return 'user_id' in session
    # return check_permission


# @Permission()
def VisitorPermission():
    def rule(self):
        return VisitorRule()


# @Permission()
def UserPermission():
    def rule(self):
        return UserRule()


# @Permission()
def AdminPermission():
    # def rule(self):
    return AdminRule()
