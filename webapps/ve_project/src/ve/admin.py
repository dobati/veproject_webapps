from django.contrib import admin
from .models import UserInput
from .models import GeneralEnEs
from .models import SubsEnEs
from .models import EuconstEnEs
from .models import ThelittleprinceEnEs
from .models import ip

class TranslationsAdminG(admin.ModelAdmin):
    class Meta:
        model = ip
admin.site.register(ip, TranslationsAdminG)

class TranslationsAdminG(admin.ModelAdmin):
    fields = ['id','source', 'target', 'level', 'detok', 'tok']
    class Meta:
        model = GeneralEnEs
admin.site.register(GeneralEnEs, TranslationsAdminG)


class TranslationsAdminM(admin.ModelAdmin):
    fields = ['id','source', 'target', 'level', 'detok', 'tok']
    class Meta:
        model = SubsEnEs
admin.site.register(SubsEnEs, TranslationsAdminM)


class TranslationsAdminL(admin.ModelAdmin):
    fields = ['id','source', 'target', 'level', 'detok', 'tok']
    class Meta:
        model = EuconstEnEs
admin.site.register(EuconstEnEs, TranslationsAdminL)


class TranslationsAdminB(admin.ModelAdmin):
    fields = ['id','source', 'target', 'level', 'detok', 'tok']
    class Meta:
        model = ThelittleprinceEnEs
admin.site.register(ThelittleprinceEnEs, TranslationsAdminB)


class UserInputAdmin(admin.ModelAdmin):
    class Meta:
        model = UserInput
admin.site.register(UserInput, UserInputAdmin)
