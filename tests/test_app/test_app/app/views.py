# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from graphene_django_hilmarh.views import GraphQLAPIView
from tests.test_app.test_app.throttles import (
    ThrottleOne,
    ThrottleTwo,
    ThrottleFive,
    ThrottleSeven,
    ThrottleNine,
    ThrottleTen,
)


class CustomGraphQLAPIView(GraphQLAPIView):
    pass


class AuthGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AdminGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]


class AdminResolverGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = []
    resolver_permission_classes = [IsAdminUser]


class ThrottleGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ThrottleOne]


class ThrottleResolverGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    resolver_throttle_classes = [ThrottleTwo]


class ThrottleResolverTwoGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    resolver_throttle_classes = [ThrottleFive]


class ThrottleResolverThreeGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    resolver_throttle_classes = [ThrottleSeven]


class ThrottleResolverFourGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    resolver_throttle_classes = [ThrottleNine]


class ThrottleResolverFiveGraphQLAPIView(GraphQLAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    resolver_throttle_classes = [ThrottleTen]
