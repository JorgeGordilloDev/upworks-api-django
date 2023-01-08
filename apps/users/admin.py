from django.contrib.auth.admin import sensitive_post_parameters_m, csrf_protect_m
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.db import router, transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   add_form_template = "admin/auth/user/add_form.html"
   change_user_password_template = None
   fieldsets = (
      (None, {"fields": ("email", "password")}),
      ("Personal info", {"fields": ("name", 'photo')}),
      ("Permissions",
         {
            "fields": (
               "is_staff",
               "role",
               "status",
               # "groups",
               # "user_permissions",
            ),
         },
      ),
      ("Important dates", {"fields": ("created_at",)}),
   )
   add_fieldsets = (
      (
         None,
         {
            "classes": ("wide",),
            "fields": ('name', "email", "password1", "password2", 'role'),
         },
      ),
   )
   form = UserChangeForm
   add_form = UserCreationForm
   change_password_form = AdminPasswordChangeForm
   list_display = ('id', "email", "name", 'role', 'status')
   list_display_links = ('email',)
   list_filter = ("role", "status")
   search_fields = ("name", "email")
   readonly_fields = ("created_at",)
   actions = None
   filter_horizontal = ()

   def get_fieldsets(self, request, obj=None):
      if not obj:
         return self.add_fieldsets
      return super().get_fieldsets(request, obj)
   
   def get_form(self, request, obj=None, **kwargs):
      defaults = {}
      if obj is None:
         defaults["form"] = self.add_form
      defaults.update(kwargs)
      return super().get_form(request, obj, **defaults)
   
   def lookup_allowed(self, lookup, value):
      return not lookup.startswith("password") and super().lookup_allowed(
         lookup, value
      )
   
   @sensitive_post_parameters_m
   @csrf_protect_m
   def add_view(self, request, form_url="", extra_context=None):
      with transaction.atomic(using=router.db_for_write(self.model)):
         return self._add_view(request, form_url, extra_context)

   def _add_view(self, request, form_url="", extra_context=None):
      if not self.has_change_permission(request):
         if self.has_add_permission(request) and settings.DEBUG:
            raise Http404(
               'Your user does not have the "Change user" permission. In '
               "order to add users, Django requires that your user "
               'account have both the "Add user" and "Change user" '
               "permissions set."
            )
         raise PermissionDenied
      if extra_context is None:
         extra_context = {}
      username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
      defaults = {
         "auto_populated_fields": (),
         "username_help_text": username_field.help_text,
      }
      extra_context.update(defaults)
      return super().add_view(request, form_url, extra_context)

   @sensitive_post_parameters_m
   def user_change_password(self, request, id, form_url=""):
      user = self.get_object(request, unquote(id))
      if not self.has_change_permission(request, user):
         raise PermissionDenied
      if user is None:
         raise Http404(
               "%(name)s object with primary key %(key)r does not exist."
               % {
                  "name": self.model._meta.verbose_name,
                  "key": escape(id),
               }
         )
      if request.method == "POST":
         form = self.change_password_form(user, request.POST)
         if form.is_valid():
               form.save()
               change_message = self.construct_change_message(request, form, None)
               self.log_change(request, user, change_message)
               msg = gettext("Password changed successfully.")
               messages.success(request, msg)
               update_session_auth_hash(request, form.user)
               return HttpResponseRedirect(
                  reverse(
                     "%s:%s_%s_change"
                     % (
                           self.admin_site.name,
                           user._meta.app_label,
                           user._meta.model_name,
                     ),
                     args=(user.pk,),
                  )
               )
      else:
         form = self.change_password_form(user)

      fieldsets = [(None, {"fields": list(form.base_fields)})]
      adminForm = admin.helpers.AdminForm(form, fieldsets, {})

      context = {
         "title": _("Change password: %s") % escape(user.get_username()),
         "adminForm": adminForm,
         "form_url": form_url,
         "form": form,
         "is_popup": (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
         "is_popup_var": IS_POPUP_VAR,
         "add": True,
         "change": False,
         "has_delete_permission": False,
         "has_change_permission": True,
         "has_absolute_url": False,
         "opts": self.model._meta,
         "original": user,
         "save_as": False,
         "show_save": True,
         **self.admin_site.each_context(request),
      }

      request.current_app = self.admin_site.name

      return TemplateResponse(
         request,
         self.change_user_password_template
         or "admin/auth/user/change_password.html",
         context,
      )
   
   def response_add(self, request, obj, post_url_continue=None):
      if "_addanother" not in request.POST and IS_POPUP_VAR not in request.POST:
         request.POST = request.POST.copy()
         request.POST["_continue"] = 1
      return super().response_add(request, obj, post_url_continue)