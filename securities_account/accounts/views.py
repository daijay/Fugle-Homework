# accounts/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccountApplicationForm
from .models import AccountApplication


def register(request, is_superuser=False):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if is_superuser:
                user.is_superuser = True
                user.is_staff = True
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'title': '建立管理員帳號' if is_superuser else '註冊',
        'button_text': '建立' if is_superuser else '註冊'
    })


@login_required
def apply_account(request):
    # 檢查是否已經有申請紀錄
    if AccountApplication.objects.filter(user=request.user).exists():
        return redirect('view_my_applications')

    if request.method == 'POST':
        form = AccountApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "申請已提交！")
            return redirect('view_my_applications')
    else:
        form = AccountApplicationForm()
    return render(request, 'accounts/apply.html', {'form': form,'title': '帳號申請表單',})

@login_required
def view_my_applications(request):
    #申請紀錄頁面
    apps = AccountApplication.objects.filter(user=request.user).order_by('-submitted_at')
    # 如果有任何一筆通過，直接跳轉到恭喜頁
    if apps.filter(status='APPROVED').exists():
        return redirect('approved_page')
    return render(request, 'accounts/my_applications.html', {'applications': apps})

@login_required
def supplement_info(request, app_id):
    #補件頁面
    app = get_object_or_404(AccountApplication, id=app_id, user=request.user)
    if request.method == 'POST':
        form = AccountApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            app.status = 'PENDING'
            app.save()
            messages.success(request, "補件完成，等待審核。")
            return redirect('view_my_applications')
    else:
        form = AccountApplicationForm(instance=app)
    return render(request, 'accounts/apply.html', {'form': form,'title': '資料補件',})

@login_required
def approved_page(request):
    #通過申請頁面
    approved = AccountApplication.objects.filter(user=request.user, status='APPROVED').order_by('-updated_at').first()
    if approved:
        return render(request, 'accounts/approved.html', {'application': approved})
    else:
        return redirect('view_my_applications')