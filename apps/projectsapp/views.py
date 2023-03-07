from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import IsOwnerOrReadOnly

from .serializers import ProjectSerializer
from .models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('userid', None)
        if user_id is not None:
            return Project.objects.filter(user=user_id)
        return self.queryset
