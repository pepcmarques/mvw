from django.urls import path
from django.views.generic import TemplateView

from mvw.accounts.views import signup, update_user, delete_user, activate, forgotten_password, password_change, \
    sign_in, sign_out, list_users, create_user

app_name = 'accounts'

urlpatterns = [
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('signup/', signup, name='signup'),
    path('activate/<str:username>/<str:token>', activate, name='activate'),
    path('profile/', update_user, name='profile'),

    path('users', list_users, name='list_users'),
    path('create/', create_user, name='create_user'),
    path('update/', update_user, name='update_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),

    path('forgotten/', forgotten_password, name='forgotten'),
    path('forgotten/done/', TemplateView.as_view(template_name='forgotten_password_done.html'),
         name='forgotten_password_done'),
    path('password_change/<int:user_id>/', password_change, name='password_change'),
]

"""
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""
