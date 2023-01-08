from django.db.models import Model, CharField, DateField, DateTimeField, TextField, BooleanField, FileField, FloatField, OneToOneField, ForeignKey, CASCADE
from apps.users.models import User, status_choices

workplace_choises = [
   ('remoto', 'Remoto'),
   ('presencial', 'Presencial'),
   ('hibrido', 'Hbrido'),
]

job_type_choides = [
   ('tiempo completo','Tiempo completo'),
   ('medio tiempo','Medio tiempo'),
   ('indeterminado','Iderterminado'),
   ('temporal','Temporal'),
   ('voluntariado','Voluntariado'),
   ('prácticas','Prácticas'),
]

application_status_choises = [
   ('postulado','Postulado'),
   ('visto','Visto'),
   ('programado para entrevistar','Programado para entrevistar'),
   ('aceptado','Aceptado'),
   ('rechazado','Rechazado'),
   ('eliminado', 'Eliminado')
]

class Alumn(Model):
   user = OneToOneField(User, on_delete=CASCADE)
   matricula = CharField("Matricula", max_length=6, null=False, unique=True)
   birthday = DateField("Fecha de nacimiento", null=True, blank=True)
   phone = CharField("Celular", max_length=10, null=True, blank=True)
   ocupation = CharField("Ocupacion", max_length=255, null=True)
   abstract = TextField("Resumen", null=True, blank=True)
   relocate = BooleanField("Recolocacion", default=False)
   cv = FileField("Curriculo", upload_to="alumn/cv", null=True)

   class Meta:
      db_table = 'ALUMN'
      verbose_name = 'Alumno'
      verbose_name_plural = 'Alumnos'

   def __str__(self):
      return self.user.name
   
   def get_email(self):
      return self.user.email

class Company(Model):
   user = OneToOneField(User, on_delete=CASCADE)
   birthday = DateField("Fecha de nacimiento", null=True, blank=True)
   country = CharField("País", max_length=55, null=True)
   address = CharField("Dirección", max_length=255, null=True)

   def __str__(self):
      return self.user.name

   class Meta:
      db_table = 'COMPANY'
      verbose_name = 'Compañia'
      verbose_name_plural = 'Compañias'
   

class Job(Model):
   id_company = ForeignKey(Company, on_delete=CASCADE)
   title = CharField('Titulo', max_length=55)
   workplace = CharField('Lugar de trabajo', max_length=10, choices=workplace_choises)
   ubication = CharField('Ubicación', max_length=55, null=False)
   job_type = CharField('Tipo de trabajo', max_length=15, choices=job_type_choides)
   description = TextField('Descripción')
   salary = FloatField('Salario')
   status = CharField('Estado', max_length=10, choices=status_choices, default='active', null=False)
   created_at = DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Fecha de creación')
   updated_at = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Fecha de modificaón')

   def __str__(self):
      return f'{self.id_company.__str__()} - {self.title}'

   class Meta:
      db_table = 'JOB'
      verbose_name = 'Empleo'
      verbose_name_plural = 'Empleos'


class Applications(Model):
   id_job = ForeignKey(Job, on_delete=CASCADE, verbose_name='Empleo')
   id_alumn = ForeignKey(Alumn, on_delete=CASCADE, verbose_name='Alumno')
   status = CharField(max_length=30, choices=application_status_choises, default='postulado', verbose_name='Estado')
   message = TextField(null=True, blank=True, verbose_name='Mensaje')
   interview_date = DateTimeField(verbose_name='Fecha para entrevista', null=True, blank=True, default=None)
   created_at = DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Fecha de creación')
   updated_at = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Fecha de modificaón')

   def __str__(self):
      return f'{self.id_job.title} - {self.id_alumn.__str__()}'