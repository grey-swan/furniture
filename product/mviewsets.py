import ujson as json

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.renderers import status
from rest_framework.response import Response

from .utils import db_query


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


# class MyModelViewSet(mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      mixins.ListModelMixin,
#                      MyGenericViewSet):
#     collection_name = ''
#
#     def get_base_name(self, operate):
#         return 'db.collection("%s")%s' % (self.collection_name, operate)
#
#     def get_queryset(self):
#         queryset = self.get_base_name('.get()')
#
#         queryset = db_query('get', queryset)
#         return queryset
#
#     def get_object(self):
#         queryset = self.get_base_name('.doc({cid}).get()')
#
#         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#         pk = '"%s"' % self.kwargs[lookup_url_kwarg]
#
#         items = db_query('get', queryset.format(cid=pk))
#         obj = items[0] if items else None
#
#         return obj
#
#     def perform_create(self, serializer):
#         queryset = self.get_base_name('.add({query})')
#
#         query = {'data': dict(serializer.validated_data)}
#         db_query('add', queryset.format(query=json.dumps(query)))
#
#     def perform_update(self, serializer):
#         queryset = self.get_base_name('.doc({cid}).update({query})')
#
#         cid = '"%s"' % serializer.instance.get('_id')
#         data = {'data': dict(serializer.validated_data)}
#
#         db_query('update', queryset.format(cid=cid, query=json.dumps(data)))
#
#     def perform_destroy(self, instance):
#         queryset = self.get_base_name('.doc({cid}).remove()')
#
#         cid = '"%s"' % instance.get('_id')
#
#         db_query('delete', queryset.format(cid=cid))


class MyModelViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     MyGenericViewSet):
    collection_name = ''

    def encode_params(self):
        params = {}
        query_params = self.request.query_params
        for key in query_params.keys():
            val = self.request.query_params.get(key, '')
            if val:  # 有值才作为检索条件
                params[key] = val
            # if '__' in val:
            #     opt, v = val.split('__')
            #
            #     if v:
            #         if opt == 'like':  # 模糊查询
            #             params[key] = {'$regex': v, '$options': 'i'}
            #         elif opt == 'in':  # in查询，查询项用逗号分隔
            #             params[key] = {'$in': v.split(',')}
            # elif val:  # 有值才作为检索条件
            #     params[key] = val

        return params

    def get_queryset(self):
        where = self.encode_params()
        params = {'collection': self.collection_name, 'type': 'get', 'where': where}
        queryset = db_query(params)
        return queryset

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        pk = self.kwargs[lookup_url_kwarg]

        params = {'collection': self.collection_name, 'type': 'doc', '_id': pk}
        obj = db_query(params)

        return obj

    def perform_create(self, serializer):
        params = {'collection': self.collection_name, 'type': 'add', 'data': dict(serializer.validated_data)}
        db_query(params)

    def perform_update(self, serializer):
        pk = serializer.data.get('_id')
        params = {'collection': self.collection_name, 'type': 'update', '_id': pk, 'data': dict(serializer.validated_data)}
        db_query(params)

    def perform_destroy(self, instance):
        pk = instance.get('_id', '')
        params = {'collection': self.collection_name, 'type': 'delete', '_id': pk}
        db_query(params)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.get('data', []), many=True)

        result = {
            'data': serializer.data,
            'next': None,
            'previous': None,
            'count': queryset.get('total', 0),
            'num_pages': queryset.get('totalPage', 1),
            'page': queryset.get('page', 1),
            'per_page': queryset.get('pageSize', 16),
        }

        return Response(result)

