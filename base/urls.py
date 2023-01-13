from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('add-track/', views.AddTrackView.as_view(), name="add_track"),
    path('update-track/', views.UpdateTrackView.as_view(), name="update_track"),
    path('delete-track/<int:id>', views.DeleteTrackView.as_view(), name="delete_track"),
    path('files/', views.FilesView.as_view(), name="get-files"),
    path('file/', csrf_exempt(views.FileView.as_view()), name="get-file"),
    path('init/',views.InitView.as_view(), name="init"),
    path('init-person/',views.InitView.as_view(), name="init-person"),
    
    
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/',TokenBlacklistView.as_view(), name="logout-api"),
    
    path('register/', csrf_exempt(views.RegisterView.as_view()), name="register"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete')
] 


