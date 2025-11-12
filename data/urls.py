from django.urls import path, include
from data import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # APIs
    path("birth/", views.BirthViews.as_view()),
    path("birth/<int:pk>/", views.BirthViews.as_view()),
    path("social/", views.SocialViews.as_view()),
    path("social/<int:pk>/", views.SocialViews.as_view()),
    path("education/", views.EducationViews.as_view()),
    path("education/<int:pk>/", views.EducationViews.as_view()),
    path("totalinfo/", views.TotalInfoViews.as_view()),
    path("totalinfo/<int:pk>/", views.TotalInfoViews.as_view()),
    path("company/", views.CompanyViews.as_view()),
    path("company/<int:pk>/", views.CompanyViews.as_view()),

    path('companyv2/', views.company_template_view, name='company-html'),
    path('companyv2/<int:pk>/', views.company_template_view, name='company-html'),

    # 🔥 schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)