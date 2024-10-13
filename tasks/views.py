from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "priority", "due_date"]

    def get_queryset(self):
        # Each user can only access their own tasks
        return self.request.user.tasks.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically assign the logged-in user as the task owner

    @action(detail=True, methods=["post"])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == "Completed":
            return Response(
                {"detail": "Task is already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        task.mark_complete()
        return Response({"detail": "Task marked as complete."})

    @action(detail=True, methods=["post"])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == "Pending":
            return Response(
                {"detail": "Task is already pending."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        task.mark_incomplete()
        return Response({"detail": "Task marked as incomplete."})
