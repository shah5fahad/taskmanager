from rest_framework import serializers
from tasks.models import Task, User


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "phone_number",
            "designation",
            "access_level",
        ]
        
    # Uses Django’s built-in password hashing
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    assigned_user_ids = serializers.ListField(
        write_only=True, child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "task_type",
            "status",
            "assigned_users",
            "assigned_user_ids",
        ]

    def create(self, validated_data):
        user_ids = validated_data.pop("assigned_user_ids", [])
        task = Task.objects.create(**validated_data)
        task.assigned_users.set(user_ids)
        return task

    def update(self, instance, validated_data):
        user_ids = validated_data.pop("assigned_user_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if user_ids is not None:
            instance.assigned_users.set(user_ids)
        instance.save()
        return instance
