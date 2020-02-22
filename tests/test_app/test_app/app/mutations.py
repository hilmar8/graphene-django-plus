from graphene_django_hilmarh.relay.mutation import SerializerClientIDCreateMutation
from tests.test_app.test_app.app.serializers import CreateRelayBookSerializer


class CreateRelayBookMutation(SerializerClientIDCreateMutation):
    class Meta:
        serializer_class = CreateRelayBookSerializer
        name = "CreateRelayBookPayload"
