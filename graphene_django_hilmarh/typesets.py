class RelayTypeSet:
    object_type = None

    permission_classes = None
    throttle_classes = None

    operations = {}

    filterset_class = None

    @classmethod
    def get_operations(cls):
        assert cls.operations is not None, (
            "'%s' should either include a `operations` attribute, "
            "or override the `get_operations()` method." % cls.__name__
        )

        return cls.operations

    @classmethod
    def get_permissions(cls, operation):
        """
        Instantiates and returns the list of permissions.
        """
        return cls.permission_classes

    @classmethod
    def get_throttles(cls, operation):
        """
        Instantiates and returns the list of throttles.
        """
        return cls.throttle_classes

    @classmethod
    def get_object_type(cls, operation):
        assert cls.object_type is not None, (
            "'%s' should either include a `object_type` attribute, "
            "or override the `get_object_type()` method." % cls.__name__
        )

        return cls.object_type

    @classmethod
    def get_filterset_class(cls):
        return cls.filterset_class
