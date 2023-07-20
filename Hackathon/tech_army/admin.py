from django.contrib import admin

from .models import Society,SharedTextarea,Notice,Activity
admin.site.register(Society)
admin.site.register(SharedTextarea)
admin.site.register(Notice)
admin.site.register(Activity)
