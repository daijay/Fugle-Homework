from django.contrib import admin

from .models import AccountApplication


@admin.register(AccountApplication)
class AccountApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_name', 'status', 'submitted_at')
    list_filter = ('status',)
    actions = ['mark_approved', 'mark_rejected', 'mark_additional']

    @admin.action(description='通過申請')
    def mark_approved(self, request, queryset):
        for app in queryset:
            app.status = 'APPROVED'
            app.rejection_reason = ''
            app.additional_requirements = ''
            app.save()

    @admin.action(description='拒絕申請（預設原因：資料不符）')
    def mark_rejected(self, request, queryset):
        for app in queryset:
            app.status = 'REJECTED'
            app.rejection_reason = "資料不符"
            app.additional_requirements = ''
            app.save()

    @admin.action(description='請求補件（預設補件說明：請補充電話或地址）')
    def mark_additional(self, request, queryset):
        for app in queryset:
            app.status = 'ADDITIONAL'
            app.additional_requirements = "請補充電話或地址"
            app.save()
