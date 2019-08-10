from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.renderers import status


class MyGenericViewSet(GenericViewSet):

    def dispatch(self, request, *args, **kwargs):
        response = super(MyGenericViewSet, self).dispatch(request, *args, **kwargs)

        data = response.data
        if response.status_code not in (200, 201, 204):
            msg = ''
            if isinstance(data, list):
                msg = '\n'.join(data)
            else:
                for k, v in response.data.items():
                    if isinstance(v, dict):
                        ke, va = v.popitem()
                    else:
                        ke, va = k, v
                    s = ': '.join([ke, va[0]]) if isinstance(va, list) else va
                    msg = '\n'.join([s, msg])
            r_data = {'status': 0, 'msg': msg, 'result': {}}
        else:
            if isinstance(data, list):
                r_data = {'status': 1, 'msg': '成功', 'result': {'data': data}}
            else:
                r_data = {'status': 1, 'msg': '成功', 'result': data}

        response.data = r_data
        response.status_code = status.HTTP_200_OK

        return response


class MyModelViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     MyGenericViewSet):
    pass


class MyScanModelViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         MyGenericViewSet):
    pass


class MyEditScanModelViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         MyGenericViewSet):
    pass


class MyCreateScanModelViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               MyGenericViewSet):
    pass


class MyNoDeleteModelViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             MyGenericViewSet):
    pass
