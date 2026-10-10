from fusion.registry import Module, SidebarItem, Permission, RoleGrant

module = Module(name='elm', title='Employee Leave Management')

sidebar_items = [
    SidebarItem(name='my_leave', title='My Leave', url='/my-leave'),
    SidebarItem(name='leave_tasks', title='Leave Tasks', url='/leave-tasks')
]

permissions = [
    Permission(name='view_my_leave', title='View My Leave'),
    Permission(name='manage_leave_tasks', title='Manage Leave Tasks')
]

role_grants = [
    RoleGrant(role='manager', permissions=['view_my_leave', 'manage_leave_tasks']),
    RoleGrant(role='employee', permissions=['view_my_leave'])
]