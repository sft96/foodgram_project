from rest_framework import viewsets

from recipes.models import Tag

from api.permissions import ReadOnly
from api.serializer.tags import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (ReadOnly,)
