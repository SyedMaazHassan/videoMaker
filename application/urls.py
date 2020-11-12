from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('confirmation/<code>', views.confirmation, name="confirmation"),
    path('send-code', views.sendAgain, name="send-code"),
    path('send_code_again', views.send_code_again, name="send_code_again"),
    path("login_validation", views.login_validation, name="login_validation"),

    path("reset-password", views.reset_password, name="reset-password"),
    path("change-password/<code>", views.change_password, name="change-password"),

    path("admin-panel", views.admin_panel, name="admin-panel"),

    path("add-product", views.add_product, name="add-product"),

    path("add-user-fields", views.add_user_fields, name="add-user-fields"),

    path("product/<id>", views.show_product, name="product")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
