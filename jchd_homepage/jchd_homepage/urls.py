from core.views import AboutView, ContactConfirmView, ContactView, HomeView, NewsView
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

urlpatterns += i18n_patterns(
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.about_list, name="about"),
    path("about/<slug:slug>/", AboutView.page_detail, name="page_detail"),
    path("news/", NewsView.news_list, name="news"),
    re_path(
        r"^news/(?P<slug>[-\w\u3000-\u9FFF]+)/$",
        NewsView.news_detail,
        name="news_detail",
    ),
    path("contact/", ContactView.as_view(), name="contact"),
    path("contact/confirm/", ContactConfirmView.as_view(), name="contact_confirm"),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
