from graphene_django.registry import Registry as GrapheneDjangoRegistry


registry = None


class Registry(GrapheneDjangoRegistry):
    def __init__(self):
        self._serializer_registry = {}
        super().__init__()

    def register_converted_serializer(self, serializer, converted):
        self._serializer_registry[serializer] = converted

    def get_converted_serializer(self, serializer):
        return self._serializer_registry.get(serializer)


def get_global_registry():
    global registry
    if not registry:
        registry = Registry()
    return registry


def reset_global_registry():
    global registry
    registry = None
