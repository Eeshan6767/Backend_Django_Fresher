from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import User, Flag

from django.contrib.admin import AdminSite
class AccessAdminSite(AdminSite):
    site_header = 'Access Control Administration'

admin.site = AccessAdminSite()

class FlagForm(forms.ModelForm):
    """
    FlagForm is a Django ModelForm for the Flag model. 
    It presents checkboxes for "SMS," "WhatsApp," and "URL Shortener" flags. 
    """
    sms = forms.BooleanField(label='SMS', required=False)
    whatsapp = forms.BooleanField(label='WhatsApp', required=False)
    url_shortner = forms.BooleanField(label='URL Shortener', required=False)
    class Meta:
        model = Flag
        fields = '__all__'

class CustomFlagInlineFormSet(BaseInlineFormSet):
    """
    CustomFlagInlineFormSet is a specialized Django formset derived from BaseInlineFormSet. 
    It blocks the delete option for forms and offers custom save behavior. 
    It extracts checkbox data for "SMS," "WhatsApp," and "URL Shortener" flags 
    from each form's cleaned data. These flags are applied to model instances before
    being saved to maintain the desired state in the Django admin interface.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.can_delete = False
    
    def save(self, commit=True):
        for form in self.forms:
            instance = form.instance
            user_flags = {
                "sms": form.cleaned_data.get("sms", False),
                "whatsapp": form.cleaned_data.get("whatsapp", False),
                "url_shortner": form.cleaned_data.get("url_shortner", False),
            }
            instance.user_flags = user_flags
            instance.save()
        super().save(commit)

class FlagsInline(admin.TabularInline):
    model = Flag
    exclude = ["user_flags"]
    form = FlagForm
    extra = 0
    formset = CustomFlagInlineFormSet


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_name", "user_email", 'get_sms_flag', 'get_whatsapp_flag', 'get_url_flag']

    def get_sms_flag(self, obj):
        flag_instance, _ = Flag.objects.get_or_create(user_id=obj)
        return flag_instance.user_flags.get('sms', False)
    get_sms_flag.boolean = True

    def get_whatsapp_flag(self, obj):
        flag_instance, _ = Flag.objects.get_or_create(user_id=obj)
        return flag_instance.user_flags.get('whatsapp', False)
    get_whatsapp_flag.boolean = True

    def get_url_flag(self, obj):
        flag_instance, _ = Flag.objects.get_or_create(user_id=obj)
        return flag_instance.user_flags.get('url_shortner', False)
    get_url_flag.boolean = True

    inlines = [FlagsInline]
    exclude = ["user_password", "user_id", "user_balance"]

admin.site.register(User, UserAdmin)

