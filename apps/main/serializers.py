from pyexpat import model
from rest_framework.serializers import ModelSerializer
from apps.main.models import Alumn, Company, Job, Applications


class AlumnSerializer(ModelSerializer):
    class Meta:
        model = Alumn
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "workplace": instance.workplace,
            "ubication": instance.ubication,
            "job_type": instance.job_type,
            "description": instance.description,
            "salary": instance.salary,
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "company": {
                "id": instance.id_company.id,
                "name": instance.id_company.user.name,
                "photo": instance.id_company.user.photo.url,
            }
        }


class JobUpdateSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'workplace', 'ubication',
                  'job_type', 'description', 'salary', 'status']


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Applications
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "status": instance.status,
            "message": instance.message,
            'interview_date': instance.interview_date if instance.interview_date == None else instance.interview_date.strftime("%Y-%m-%d %H:%M"),
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "job": {
                'id': instance.id_job.id,
                'title': instance.id_job.title,
                'status': instance.id_job.status,
                'company_name': instance.id_job.id_company.user.name,
                'company_phto': instance.id_job.id_company.user.photo.url,
            },
            "alumn": {
                'id': instance.id_alumn.id,
                'name': instance.id_alumn.user.name,
                'photo': instance.id_alumn.user.photo.url,
                'cv': instance.id_alumn.cv.url
            }
        }


class ApplicationUpdateSerializer(ModelSerializer):
    class Meta:
        model = Applications
        fields = ['status','message', 'interview_date', ]
