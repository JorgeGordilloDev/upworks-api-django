from django.db.models import CharField, EmailField, ImageField, BooleanField, DateTimeField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords


roles_choices = (
    ('regular', 'Regular'),
    ('company', 'Company'),
    ('admin', 'Admin'),
)

status_choices = (
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('bloqueado', 'Bloqueado'),
    ('eliminado', 'Eliminado'),
)

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **other_fields):
        if not email:
            raise ValueError('Debe proporcionar una dirección de correo electrónico')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField('email address', max_length=255, unique=True, null=False, blank=False)
    name = CharField('name',max_length=100)
    photo = ImageField('photo', upload_to='users/', default='users/default.png')
    role = CharField('role', choices=roles_choices, max_length=10, blank=False, default='regular')
    status = CharField('status', choices=status_choices, max_length=10, blank=False, default='active')
    created_at = DateTimeField('created_at', auto_now=False, auto_now_add=True, editable=False)

    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    historical = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_role(self, role):
        return self.role == role

