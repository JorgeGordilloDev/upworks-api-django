from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from apps.main.serializers import *
from rest_framework.decorators import action


class AlumnViewSet(GenericViewSet):
    serializer_class = AlumnSerializer
    model = Alumn

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self):
        return self.model.objects.filter(user__id=self.kwargs['pk'])

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)

    def retrieve(self, reques, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message': '', 'error': 'Unidad de Medida no encontrada!'}, status=400)

    def create(self, request):
        alumn_serializer = self.serializer_class(data=request.data)
        if alumn_serializer.is_valid():
            alumn_serializer.save()
            data = {
                'status': 201,
                'message': 'Registro creado correctamente',
                'data': alumn_serializer.data
            }
            return Response(data)
        data = {
            'status': 400,
            'message': 'Se produjo un error al crear el registro',
            'data': None
        }
        return Response(data)

    def update(self, request, pk):
        if not self.get_object().exists():
            return Response({
                'status': 404,
                'message': 'No se encontro el elemento solicitado',
                'data': None
            })

        alumn_serializer = self.serializer_class(
            instance=self.get_object().get(), data=request.data)
        if alumn_serializer.is_valid():
            alumn_serializer.save()
            return Response({
                'status': 200,
                'message': 'Registro actualizado correctamente',
                'data': alumn_serializer.data
            })

        return Response({
            'status': 400,
            'message': 'Se produjo un error al actualizar los datos',
            'data': None
        })

    @action(detail=True, methods=['get'])
    def apllications(self, request, pk):
        data = Applications.objects.filter(
            id_alumn__user__id=pk,).exclude(status='eliminado')
        data = ApplicationSerializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)


class CompanyViewSet(GenericViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(user__id=self.kwargs['pk'])

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)

    def retrieve(self, reques, pk):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message': '', 'error': 'Compañia no encontrada!'}, status=400)

    def create(self, request):
        company_serializer = self.serializer_class(data=request.data)
        if company_serializer.is_valid():
            company_serializer.save()
            data = {
                'status': 201,
                'message': 'Registro creado correctamente',
                'data': company_serializer.data
            }
            return Response(data)
        data = {
            'status': 400,
            'message': 'Se produjo un error al crear el registro',
            'data': None
        }
        return Response(data)

    def update(self, request, pk):
        if not self.get_object().exists():
            return Response({
                'status': 404,
                'message': 'No se encontro el elemento solicitado',
                'data': None
            })

        company_serializer = self.serializer_class(
            instance=self.get_object().get(), data=request.data)
        if company_serializer.is_valid():
            company_serializer.save()
            return Response({
                'status': 200,
                'message': 'Registro actualizado correctamente',
                'data': company_serializer.data
            })

        return Response({
            'status': 400,
            'message': 'Se produjo un error al actualizar los datos',
            'data': None
        })

    @action(detail=True, methods=['get'])
    def jobs(self, request, pk):
        data = Job.objects.filter(
            id_company__user__id=pk).exclude(status='eliminado')
        data = JobSerializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)

    @action(detail=True, methods=['get'])
    def applications(self, request, pk):
        data = Applications.objects.filter(
            id_job__id_company__user__id=pk).exclude(status='eliminado')
        data = ApplicationSerializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data, status=200)


class JobViewSet(GenericViewSet):
    serializer_class = JobSerializer
    update_serializer_class = JobUpdateSerializer
    model = Job
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.exclude(status='eliminado')
        return self.queryset

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)

    def retrieve(self, reques, pk):
        job = self.get_object(pk)
        job_serializer = self.serializer_class(job)
        data = {
            'msg': 'OK',
            'data': job_serializer.data
        }
        return Response(data, status=200)

    def create(self, request):
        job_serializer = self.serializer_class(data=request.data)
        if job_serializer.is_valid():
            job_serializer.save()
            data = {
                'status': 201,
                'message': 'Registro creado correctamente',
                'data': job_serializer.data
            }
            return Response(data, status=201)
        data = {
            'status': 400,
            'message': 'Se produjo un error al crear el registro',
            'data': None
        }
        return Response(data, status=400)

    def update(self, request, pk):
        job = self.get_object(pk=pk)
        job_serializer = self.update_serializer_class(job, data=request.data)

        if job_serializer.is_valid():
            job_serializer.save()
            return Response({
                'status': 200,
                'message': 'Empleo actualizado correctamente',
                'data': job_serializer.data
            }, status=200)

        return Response({
            'status': 400,
            'message': 'Se produjo un error al actualizar los datos',
            'data': None
        }, status=400)

    def destroy(self, request, pk):
        job = self.get_object(pk=pk)
        job.status = 'eliminado'
        job.save()
        return Response({
            'message': 'Empleo eliminado correctamente'
        })

    @action(detail=True, methods=['get'])
    def apllications(self, request, pk):
        data = Applications.objects.filter(
            id_job=pk).exclude(status='eliminado')
        data = ApplicationSerializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)


class ApplicationViewSet(GenericViewSet):
    serializer_class = ApplicationSerializer
    update_serializer_class = ApplicationUpdateSerializer
    model = Applications
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.exclude(status='eliminado')
        return self.queryset

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        data = {
            'msg': 'OK',
            'data': data.data
        }
        return Response(data)

    def retrieve(self, reques, pk):
        application = self.get_object(pk)
        application_serializer = self.serializer_class(application)
        data = {
            'msg': 'OK',
            'data': application_serializer.data
        }
        return Response(data, status=200)

    def create(self, request):
        application_serializer = self.serializer_class(data=request.data)
        if application_serializer.is_valid():
            application_serializer.save()
            data = {
                'status': 201,
                'message': 'Registro creado correctamente',
                'data': application_serializer.data
            }
            return Response(data, status=201)
        data = {
            'status': 400,
            'message': 'Se produjo un error al crear el registro',
            'erros': application_serializer.errors,
            'data': None
        }
        return Response(data, status=400)

    def update(self, request, pk):
        application = self.get_object(pk=pk)
        application_serializer = self.update_serializer_class(application, data=request.data)

        if application_serializer.is_valid():
            application_serializer.save()
            return Response({
                'status': 200,
                'message': 'Postulación actualizada correctamente',
                'data': application_serializer.data
            }, status=200)

        return Response({
            'status': 400,
            'message': 'Se produjo un error al actualizar los datos',
            'data': None
        }, status=400)

    def destroy(self, request, pk):
        application = self.get_object(pk=pk)
        application.status = 'eliminado'
        application.save()
        return Response({
            'message': 'Postulacion eliminada correctamente'
        })
