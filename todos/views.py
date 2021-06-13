import re
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors.base import openapi
from .serializers import TodoSerializer
from .models import Todo

class CustomNotNumberException(APIException):
    status_code = 400
    default_detail = '숫자 형태의 id 값을 작성해주세요.'


class BadRequestException(APIException):
    status_code = 400
    default_detail = 'request 요청 양식을 다시 확인해주세요.'


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
        'id': get_field('id', '할 일 항목 고유 id 값', openapi.TYPE_INTEGER),
        'title': get_field('title', '할 일 제목', openapi.TYPE_STRING),
        'content': get_field('contet', '할 일 내용', openapi.TYPE_STRING),
        'created_at': get_field('created_at', '할 일 생성 일자', openapi.TYPE_STRING),
        'updated_at': get_field('updated_at', '할 일 수정 일자', openapi.TYPE_STRING),
        'is_completed': get_field('is_completed', '할 일 완료 여부', openapi.TYPE_BOOLEAN),
    }


def get_todo_list_success_response():
    return openapi.Schema(
        'success_response',
        type = openapi.TYPE_ARRAY,
        items = openapi.Items(
            type = openapi.TYPE_OBJECT,
            properties = get_todo_list_property()
        )
    )


def get_todo_detail_success_response():
    return openapi.Schema(
        'success_response',
        type = openapi.TYPE_OBJECT,
        description = 'id 값과 매칭되는 할 일 항목을 찾은 경우',
        properties = get_todo_list_property()
    )


def check_necessary_parameter(request_data):
    request_form = request_data

    if 'is_completed' in request_form:
        request_form.pop('is_completed')
    
    if 'title' not in request_form or 'content' not in request_form:
        raise BadRequestException()

    class EmptyTitleException(APIException):
        status_code = 400
        default_detail = '할 일 제목을 1자 이상 작성해주세요.'

    if request_form['title'] == '':
        raise EmptyTitleException()

    class EmptyContentException(APIException):
        status_code = 400
        default_detail = '할 일 내용을 1자 이상 작성해주세요.'


    if request_form['content'] == '':
        raise EmptyContentException()


@swagger_auto_schema(
    method = 'get',
    operation_id = '전체 Todo List 불러오기',
    operation_description = '전체 Todo List 불러오는 API',
    tags = ['Todos'],
    responses = {
        200: openapi.Schema(
            type = openapi.TYPE_OBJECT,
            description = '전체 할 일 목록을 정상적으로 불러온 경우',
            properties = {
                'data': get_todo_list_success_response(),
                'todo_count': openapi.Schema(
                    type = openapi.TYPE_INTEGER,
                    description = '할 일 갯수',
                ),
            }
        ),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@swagger_auto_schema(
    method = 'post',
    operation_id = 'Todo 생성',
    operation_description = '할 일 생성하는 API("is_completed"는 Frontend에서 요청시 포함하지 않아도 됨)',
    tags = ['Todos'],
    request_body = TodoSerializer,
    responses = {
        201: openapi.Schema(
            'success_response',
            type = openapi.TYPE_OBJECT,
            description = '할 일 등록이 정상적으로 성공한 경우',
            properties = get_todo_list_property()
        ),
        400: get_error_response('제목 또는 내용이 empty string이거나 잘못된 요청을 한 경우'),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@api_view(['GET', 'POST'])
def todos(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        response_dict = dict()

        response_dict['data'] = serializer.data
        response_dict['todo_count'] = len(serializer.data)

        return Response(response_dict)

    elif request.method == 'POST':
        check_necessary_parameter(request.data)

        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)

        raise BadRequestException()


@swagger_auto_schema(
    method = 'get',
    operation_id = '특정 Todo 항목 불러오기',
    operation_description = 'id 값을 받아서 특정 Todo 항목을 불러오는 API',
    tags = ['Todos'],
    manual_parameters = [openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description = '할 일 항목의 고유 id 값',
        type = openapi.TYPE_STRING,
    )],
    responses = {
        200: get_todo_detail_success_response(),
        400: get_error_response('id 값에 숫자 이외의 다른 타입의 값이 포함되어 있는 경우'),
        404: get_error_response('id 값과 매칭되는 할 일 항목을 못 찾은 경우'),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@swagger_auto_schema(
    method = 'patch',
    operation_id = '특정 Todo 항목 수정',
    operation_description = '특정 할 일을 수정하는 API(해당 API에서는 제목과 내용만 수정하고, 할 일 완료 여부는 별도 API로 요청)',
    tags = ['Todos'],
    request_body = TodoSerializer,
    responses = {
        201: openapi.Schema(
            'success_response',
            type = openapi.TYPE_OBJECT,
            description = '할 일 수정이 정상적으로 성공한 경우',
            properties = get_todo_list_property()
        ),
        400: get_error_response('클라이언트측에서 잘못 요청한 경우'),
        404: get_error_response('id 값과 매칭되는 할 일 항목을 못 찾은 경우'),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@swagger_auto_schema(
    method = 'delete',
    operation_id = '특정 Todo 항목 삭제하기',
    operation_description = 'id 값을 받아서 특정 Todo 항목을 삭제하는 API',
    tags = ['Todos'],
    manual_parameters = [openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description = '할 일 항목의 고유 id 값',
        type = openapi.TYPE_STRING,
    )],
    responses = {
        204: 'id 값과 매칭되는 할 일 항목을 찾아서 삭제하는데 성공한 경우',
        400: get_error_response('id 값에 숫자 이외의 다른 타입의 값이 포함되어 있는 경우'),
        404: get_error_response('id 값과 매칭되는 할 일 항목을 못 찾은 경우'),
        500: get_error_response('서버에서 에러가 발생한 경우'),
    }
)
@api_view(['GET', 'PATCH', 'DELETE'])
def todo_detail(request, id):
    if not(re.match('^\d+$', str(id))):
        raise CustomNotNumberException()

    todo = get_object_or_404(Todo, pk=id)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        check_necessary_parameter(request.data)

        serializer = TodoSerializer(data=request.data, instance=todo)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
        
    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=204)