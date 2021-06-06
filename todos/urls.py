from rest_framework import permissions
# from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title = "Todo API",
      default_version = 'v1',
      description = "Frontend 에서 Backend와 api 통신 연습을 위한 서비스 입니다.",
      terms_of_service = "https://www.google.com/policies/terms/",
      contact = openapi.Contact(email="wallys0213@gmail.com"),
      license = openapi.License(name="Wally License"),
   ),
   public = True,
   permission_classes = (permissions.AllowAny,),
)

# router = DefaultRouter()
# router.register(r'todos',views.TodoViewSet)

urlpatterns = [
    path('todos/', views.todos, name="todo-list"),
    path('todos/<id>/', views.todo_detail, name="todo-detail"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# + router.urls
