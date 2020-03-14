from graphene_django_plus.relay.mutation import (
    SerializerClientIDCreateMutation,
    SerializerClientIDUpdateMutation,
)
from graphene_django_plus.relay.node import PlusNode
from tests.test_app.test_app.app.serializers import (
    CreateRelayBookSerializer,
    UpdateRelayBookSerializer,
)


class CreateRelayBookMutation(SerializerClientIDCreateMutation):
    class Meta:
        serializer_class = CreateRelayBookSerializer
        name = "CreateRelayBookPayload"


class UpdateRelayBookMutation(SerializerClientIDUpdateMutation):
    class Meta:
        serializer_class = UpdateRelayBookSerializer
        node_class = PlusNode
        partial = False
        name = "UpdateRelayBookPayload"


class UpdateRelayBookPartialMutation(SerializerClientIDUpdateMutation):
    class Meta:
        serializer_class = UpdateRelayBookSerializer
        node_class = PlusNode
        partial = True
        name = "UpdateRelayBookPartialPayload"
