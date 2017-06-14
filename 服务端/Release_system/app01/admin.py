from django.contrib import admin

# Register your models here.
from .models import *


class Useradmin(admin.ModelAdmin):
    list_display = ('username', 'headImg', 'service_type', 'updatetime')
    search_fields = ('username', 'headImg', 'service_type', 'updatetime')
    list_filter = ('username', 'headImg', 'service_type', 'updatetime')


class userproadmin(admin.ModelAdmin):
    list_display = ('user', 'name',)
    search_fields = ('user', 'name',)
    list_filter = ('user', 'name',)


class his_reladmin(admin.ModelAdmin):
    list_display = ('host', 'host_group', 'filename', 'service_type', 'status', 'relea_time')
    search_fields = ('host', 'host_group', 'filename', 'service_type', 'status', 'relea_time')
    list_filter = ('host', 'host_group', 'filename', 'service_type', 'status', 'relea_time')


class host_listadmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip', 'host_group', 'updatetime',)
    search_fields = ('hostname', 'ip', 'host_group', 'updatetime',)
    list_filter = ('hostname', 'ip', 'host_group', 'updatetime',)


class service_typeadmin(admin.ModelAdmin):
    list_display = ('service_name', 'demo_path', 'install_type', 'updatetime','service_processname')
    search_fields = ('service_name', 'demo_path', 'install_type', 'updatetime','service_processname')
    list_filter = ('service_name', 'demo_path', 'install_type', 'updatetime','service_processname')


class server_ip_and_portadmin(admin.ModelAdmin):
    list_display = ('server_ip', 'server_port',)
    search_fields = ('server_ip', 'server_port',)
    list_filter = ('server_ip', 'server_port',)


admin.site.register(User, Useradmin)
admin.site.register(userpro, userproadmin)
admin.site.register(host_list, host_listadmin)
admin.site.register(service_type, service_typeadmin)
admin.site.register(his_rel, his_reladmin)
admin.site.register(his_rool, his_reladmin)
admin.site.register(server_ip_and_port, server_ip_and_portadmin)
