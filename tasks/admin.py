from django.contrib import admin
from tasks.models import Task
from django.contrib.auth.models import User

# Register Task model.
admin.site.register(Task)
# Register User model.
admin.site.register(User)
