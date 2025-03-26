from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import Task
from tasks.api.serializers import TaskSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from tasks.api.serializers import (
    UserAuthSerializer,
    UserSerializer,
)

# Used to get the updated user model
User = get_user_model()


class UserRegisterView(APIView):
    """
    API to register a new user.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User registered successfully",
                    "token": token.key,
                    "status": True,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "error": serializer.errors,
                "status": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginView(APIView):
    """
    API to log in a user and return a token.
    """

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            user_email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response(
                    {
                        "error": "User does not found.",
                        "status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if authenticate(request.data, username=user_email, password=password):
                # Get or create a token for the user
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "message": "Login successful",
                        "token": token.key,
                        "status": True,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "error": "Invalid email or password",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "error": serializer.errors,
                "status": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class TaskCreateView(APIView):
    """
    Create a new task
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "status": True,
                    "message": "Task created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "error": serializer.errors,
                "status": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class TaskAssignView(APIView):
    """
    Assign a task to one or more users
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {
                    "error": "Task not found.",
                    "status": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserAuthSerializer(data=request.data, fields=["email"])
        if serializer.is_valid():
            user_email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response(
                    {
                        "error": "User does not found.",
                        "status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            task.assigned_users.add(user.id)
            task.save()
            return Response(
                {
                    "message": "Task assigned successfully.",
                    "status": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "data": serializer.errors,
                    "status": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTasksView(APIView):
    """
    Retrieve tasks assigned to a specific user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserAuthSerializer(data=request.query_params, fields=["email"])
        if serializer.is_valid():
            user_email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response(
                    {
                        "error": "User does not found.",
                        "status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            tasks = user.tasks.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "status": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "data": serializer.errors,
                    "status": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
