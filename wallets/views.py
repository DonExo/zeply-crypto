from django.db.models import Count
from rest_framework import mixins, generics
from rest_framework.response import Response

from .models import CryptoAddress
from .serializers import CryptoAddressListRetrieveSerializer, CryptoAddressCreateSerializer, CryptoAddressListGroupedByTypeSerializer


class CryptoAddressListRetrieveView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = CryptoAddress.objects.all()
    serializer_class = CryptoAddressListRetrieveSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            # BONUS: Add sorting functionality in the LIST call.
            sort = request.query_params.get("sort", "False").lower() == "true"
            if sort:
                grouped_addresses = CryptoAddress.objects.values('type').annotate(count=Count('type')).order_by('type')
                response_data = []
                for group in grouped_addresses:
                    addresses = CryptoAddress.objects.filter(type=group['type'])
                    serializer = CryptoAddressListGroupedByTypeSerializer(
                        {'type': group['type'], 'addresses': addresses}
                    )
                    response_data.append(serializer.data)

                return Response(response_data)
            else:
                return self.list(request, *args, **kwargs)


class CryptoAddressCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = CryptoAddress.objects.all()
    serializer_class = CryptoAddressCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
