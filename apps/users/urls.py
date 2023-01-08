from rest_framework.routers import DefaultRouter
from apps.users.views import *
from apps.main.views import *

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'alumns', AlumnViewSet, basename='alumnos')
router.register(r'companies', CompanyViewSet, basename='compañias')
router.register(r'jobs', JobViewSet, basename='jobs')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = router.urls