"""test_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path

from graphene_django_hilmarh.validators import (
    DocumentDepthValidator,
    DisableIntrospectionValidator,
)
from tests.test_app.test_app.app.views import CustomGraphQLAPIView
from tests.test_app.test_app.schema import schema


class CustomDepthValidator(DocumentDepthValidator):
    max_depth = 2


urlpatterns = [
    re_path(
        r"^graphql-introspection",
        CustomGraphQLAPIView.as_view(
            graphene_schema=schema,
            graphene_validation_classes=[DisableIntrospectionValidator],
        ),
        name="graphql-introspection",
    ),
    re_path(
        r"^graphql-depth",
        CustomGraphQLAPIView.as_view(
            graphene_schema=schema, graphene_validation_classes=[CustomDepthValidator],
        ),
        name="graphql-depth",
    ),
    re_path(
        r"^graphql",
        CustomGraphQLAPIView.as_view(graphene_schema=schema),
        name="graphql",
    ),
]
