from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path

import blogs.views

from blogs import views
from django.conf import settings
from django.conf.urls.static import static
from profiles import views as profiles_views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('', views.home_view, name='home'),
                  path('about/', views.about_view, name='about'),

                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                  path('addpost/', blogs.views.AddPost.as_view(), name='addpost'),
                  path('detailpost/edit/<int:pk>', blogs.views.UpdatePost.as_view(), name='updatepost'),
                  path('detailpost/<int:pk>', blogs.views.DetailPost.as_view(), name='detailpost'),
                  path('detailpost/<int:pk>/delete', blogs.views.DeletePost.as_view(), name='deletepost'),
                  path('detailpost/<int:pk>/comment', blogs.views.AddCommentPost.as_view(), name='addcomment'),

                  path('login/', profiles_views.login_register, name='login'),
                  path('profile/', profiles_views.ProfileSite.as_view(), name='profile'),
                  path('edit_profile/', profiles_views.update_profile, name='edit_profile'),

                  path('password/', profiles_views.PasswordChange.as_view(), name='changepass'),
                  path('logout/', profiles_views.LogoutSite.as_view(), name='logout'),
                    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  path('search', blogs.views.search_bar, name='search'),
                  path('detailpost/<int:pk>/del_comment', blogs.views.DeleteComment.as_view(), name='delcomment'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
