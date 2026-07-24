from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    CRUD for Todo:
    GET    /api/todos/        -> list
    POST   /api/todos/        -> create
    GET    /api/todos/{id}/   -> retrieve
    PUT    /api/todos/{id}/   -> update
    PATCH  /api/todos/{id}/   -> partial update
    DELETE /api/todos/{id}/   -> delete
    """
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
