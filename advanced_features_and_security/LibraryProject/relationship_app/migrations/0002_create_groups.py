from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def create_groups_and_permissions(apps, schema_editor):
    # Get models
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Get or create groups
    viewer_group, created = Group.objects.get_or_create(name='Viewers')
    editor_group, created = Group.objects.get_or_create(name='Editors')
    admin_group, created = Group.objects.get_or_create(name='Admins')
    
    # Get content type for Book model
    try:
        content_type = ContentType.objects.get(app_label='relationship_app', model='book')
    except ContentType.DoesNotExist:
        # If content type doesn't exist yet, we'll create permissions manually
        content_type = None
    
    # Define permission codenames and names
    permissions_data = [
        ('can_view_book', 'Can view book details'),
        ('can_create_book', 'Can create book'),
        ('can_edit_book', 'Can edit book'),
        ('can_delete_book', 'Can delete book'),
    ]
    
    # Get or create permissions
    permissions = {}
    for codename, name in permissions_data:
        try:
            if content_type:
                permission, created = Permission.objects.get_or_create(
                    content_type=content_type,
                    codename=codename,
                    defaults={'name': name}
                )
            else:
                # If content type doesn't exist, create permission without it
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    name=name,
                    content_type_id=1  # Using a default content type ID
                )
            permissions[codename] = permission
        except Exception as e:
            print(f"Error creating permission {codename}: {e}")
    
    # Make sure we have all required permissions
    if not all(permissions.values()):
        print("Warning: Not all permissions were created successfully")
        return
    
    # Assign permissions to groups
    # Viewers can only view books
    if 'can_view_book' in permissions:
        viewer_group.permissions.add(permissions['can_view_book'])
    
    # Editors can view, create, and edit books
    if all(perm in permissions for perm in ['can_view_book', 'can_create_book', 'can_edit_book']):
        editor_group.permissions.add(
            permissions['can_view_book'],
            permissions['can_create_book'],
            permissions['can_edit_book']
        )
    
    # Admins can do everything
    if all(perm in permissions for perm in ['can_view_book', 'can_create_book', 'can_edit_book', 'can_delete_book']):
        admin_group.permissions.add(
            permissions['can_view_book'],
            permissions['can_create_book'],
            permissions['can_edit_book'],
            permissions['can_delete_book']
        )

def remove_groups(apps, schema_editor):
    # Delete the groups we created
    Group.objects.filter(
        name__in=['Viewers', 'Editors', 'Admins']
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('relationship_app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, remove_groups),
    ]
