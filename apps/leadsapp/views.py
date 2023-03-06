from rest_framework import viewsets

from .models import Lead
from .serializers import LeadSerializer

from apps.users.permissions import IsLeadOwnerOrReadOnly


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (IsLeadOwnerOrReadOnly, )

    def get_queryset(self):
        project_id = self.request.query_params.get('projectid', None)
        if project_id is not None:
            return Lead.objects.filter(project_id=project_id)
        return self.queryset
