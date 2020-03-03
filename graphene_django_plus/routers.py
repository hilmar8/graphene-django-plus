from graphene_django_plus.fields import (
    SpriklConnectionField,
    SpriklFilterConnectionField,
)
from graphene_django_plus.relay.node import SpriklNode


class TestRouter:
    def __init__(self):
        self.registry = []

    def register(self, field_name, field_type):
        self.registry.append((field_name, field_type))

    def get_properties(self):
        ret = []

        for field_name, field_type in self.registry:
            operations = field_type.get_operations()
            filterset_class = field_type.get_filterset_class()

            if "get" in operations:
                operation_name = (
                    operations["get"] if operations["get"] is not None else field_name
                )
                permission_classes = field_type.get_permissions("get")
                throttle_classes = field_type.get_throttles("get")
                ret.append(
                    (
                        operation_name,
                        SpriklNode.Field(
                            field_type.get_object_type("get"),
                            permission_classes=permission_classes,
                            throttle_classes=throttle_classes,
                        ),
                    )
                )

            if "list" in operations:
                operation_name = (
                    operations["list"] if operations["list"] is not None else field_name
                )
                permission_classes = field_type.get_permissions("list")
                throttle_classes = field_type.get_throttles("list")
                if filterset_class is not None:
                    ret.append(
                        (
                            operation_name,
                            SpriklFilterConnectionField(
                                field_type.get_object_type("list"),
                                filterset_class=filterset_class,
                                permission_classes=permission_classes,
                                throttle_classes=throttle_classes,
                            ),
                        )
                    )
                else:
                    ret.append(
                        (
                            operation_name,
                            SpriklConnectionField(
                                field_type.get_object_type("list"),
                                permission_classes=permission_classes,
                                throttle_classes=throttle_classes,
                            ),
                        )
                    )

        return ret

    def query(self):
        # TODO: Query fields must be a mapping (dict / OrderedDict) with field names
        #       as keys or a function which returns such a mapping.
        #       ergo... registry must not be empty.

        class Query:
            pass

        for k, v in self.get_properties():
            setattr(Query, k, v)

        return Query
