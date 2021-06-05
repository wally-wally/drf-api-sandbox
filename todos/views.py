import re
from django.shortcuts import get_object_or_404
# from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors.base import openapi
from .serializers import TodoSerializer
from .models import Todo

class CustomNotNumberException(APIException):
    status_code = 400
    default_detail = '숫자 형태의 id 값을 작성해주세요.'


def get_field(parameter, description, type):
    return openapi.Schema(
        parameter,
        description = description,
        type = type,
    )


def get_error_response(description):
    detail_field = get_field('detail', '에러 내용', openapi.TYPE_STRING)

    status_code_field = get_field('status_code', '에러 상태 코드', openapi.TYPE_INTEGER)

    return openapi.Schema(
        'error_response',
        type = openapi.TYPE_OBJECT,
        description = description,
        properties = {
            'detail': detail_field,
            'status_code': status_code_field,
        }
    )


def get_todo_list_property():
    return {
        'id': get_field('id', '할일 항목 고유 id 값', openapi.TYPE_INTEGER),
        'title': get_field('title', '할일 제목', openapi.TYPE_STRING),
        'content': get_field('contet', '할일 내용', openapi.TYPE_STRING),
        'created_at': get_field('created_at', '할일 생성 일자', openapi.TYPE_STRING),
        'updated_at': get_field('updated_at', '할일 수정 일자', openapi.TYPE_STRING),
        'is_completed': get_field('is_completed', '할일 완료 여부', openapi.TYPE_BOOLEAN),
    }


def get_todo_list_success_response():
    return openapi.Schema(
        'success_response',
        type = openapi.TYPE_ARRAY,
        description = '전체 할일 목록을 정상적으로 불러온 경우',
        items = openapi.Items(
            type = openapi.TYPE_OBJECT,
            properties = get_todo_list_property()
        )
    )


def get_todo_detail_success_response():
    return openapi.Schema(
        'success_response',
        type = openapi.TYPE_OBJECT,
        description = 'id 값과 매칭되는 할일 항목을 찾은 경우',
        properties = get_todo_list_property()
    )


@swagger_auto_schema(
    method = 'get',
    operation_id = '전체 Todo List 불러오기',
    operation_description = '전체 Todo List 불러오는 API',
    tags = ['Todos'],
    responses = {
        200: get_todo_list_success_response(),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@api_view(['GET'])
def todo_list(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method = 'get',
    operation_id = '특정 Todo 항목 불러오기',
    operation_description = 'id 값을 받아서 특정 Todo 항목을 불러오는 API',
    tags = ['Todos'],
    manual_parameters = [openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description = '할일 항목의 고유 id 값',
        type = openapi.TYPE_STRING,
    )],
    responses = {
        200: get_todo_detail_success_response(),
        400: get_error_response('id 값에 숫자 이외의 다른 타입의 값이 포함되어 있는 경우'),
        404: get_error_response('id 값과 매칭되는 할일 항목을 못 찾은 경우'),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@api_view(['GET'])
def todo_detail(request, id):
    if not(re.match('^\d+$', str(id))):
        raise CustomNotNumberException()

    todo = get_object_or_404(Todo, pk=id)
    serializer = TodoSerializer(todo)
    return Response(serializer.data)


# TODO: class 기반의 viewset으로 구성

# class TodoViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer

#     @action(detail=False, methods=['get'])
#     def todo_list(self, request):
#         """
#         전체 Todo List 불러오는 API
#         """
#         serializer = self.serializer_class(self.querySet, many=True)
#         return Response(serializer.data)


#     @action(detail=False, methods=['get'])
#     def todo_detail(self, request, todo_pk):
#         """
#         id 값을 받아서 특정 Todo 항목을 불러오는 API
#         (숫자 이외 값을 전송하면 400 에러 발생)
#         """
#         if not(re.match('^\d+$', str(todo_pk))):
#             raise CustomNotNumberException()

#         todo = get_object_or_404(self.querySet, pk=todo_pk)
#         serializer = self.serializer_class(todo)
#         return Response(serializer.data)