from django.contrib import admin
from .models import Profile, Student

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'registration_number', 'department', 'semester', 'status', 'created_at')
    list_filter = ('department', 'status')
    search_fields = ('full_name', 'registration_number')
