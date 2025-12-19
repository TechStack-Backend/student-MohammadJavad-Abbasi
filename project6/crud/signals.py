# crud/signals.py

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model



def create_groups_and_permissions(sender, **kwargs):

    Project = apps.get_model("crud", "Project")
    Developer = apps.get_model("crud", "Developer")
    Skill = apps.get_model("crud", "Skill")
    UserProfile = apps.get_model("accounts", "UserProfile")
    User = get_user_model()


    project_ct = ContentType.objects.get_for_model(Project)
    developer_ct = ContentType.objects.get_for_model(Developer)
    skill_ct = ContentType.objects.get_for_model(Skill)
    userprofile_ct = ContentType.objects.get_for_model(UserProfile)
    user_ct = ContentType.objects.get_for_model(User)



    def perms(codename_list, content_type):
        return Permission.objects.filter(
            codename__in=codename_list,
            content_type=content_type,
        )

    admin_group, _ = Group.objects.get_or_create(name="Admin")

    admin_group.permissions.set(
        list(perms(
            [
                "add_project",
                "change_project",
                "delete_project",
                "view_project",
                "approve_project",
            ],
            project_ct,
        ))

        + list(perms(
            [
                "add_developer",
                "change_developer",
                "delete_developer",
                "view_developer",
            ],
            developer_ct,
        ))

        + list(perms(
            [
                "add_skill",
                "change_skill",
                "delete_skill",
                "view_skill",
            ],
            skill_ct,
        ))

        + list(perms(
            [
                "add_userprofile",
                "change_userprofile",
                "delete_userprofile",
                "view_userprofile",
            ],
            userprofile_ct,
        ))

        + list(perms(
            [
                "add_user",
                "change_user",
                "delete_user",
                "view_user",
            ],
            user_ct,
        ))
    )


    manager_group, _ = Group.objects.get_or_create(name="Manager")

    manager_group.permissions.set(
        list(perms(
            [
                "add_project",
                "change_project",
                "view_project",
                "approve_project",
            ],
            project_ct,
        )) +
        list(perms(
            [
                "view_developer",
            ],
            developer_ct,
        ))
    )

    developer_group, _ = Group.objects.get_or_create(name="Developer")

    developer_group.permissions.set(
        list(perms(
            [
                "add_project",
                "view_project",
            ],
            project_ct,
        )) +
        list(perms(
            [
                "view_developer",
            ],
            developer_ct,
        ))
    )


post_migrate.connect(create_groups_and_permissions)
