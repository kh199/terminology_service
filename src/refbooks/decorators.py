from rest_framework.response import Response


def response_format(cls):
    class DecoratedClass(cls):
        def list(self, request, *args, **kwargs):
            model_name = self.serializer_class.Meta.model.__name__
            response = super().list(request, *args, **kwargs)
            return Response({f"{model_name.lower()}s": response.data})

    return DecoratedClass
