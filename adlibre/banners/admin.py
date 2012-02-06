from django.contrib import admin

from adlibre.banners.models import BannerImage, Banner

class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'dimentions')
    list_filter = ('image',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'date_created')
    list_filter = ('name',)


admin.site.register(BannerImage, BannerImageAdmin)
admin.site.register(Banner, BannerAdmin)