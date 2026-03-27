# core/admin.py
from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from parler.admin import (
    TranslatableAdmin,
    TranslatableStackedInline,
    TranslatableTabularInline,
)

from .models import (
    BasicContent,
    CompanyProfile,
    GlobalNetworkLocation,
    Greeting,
    HistoryEvent,
    MenuItem,
    News,
    Page,
    SiteConfiguration,
)


class CompanyProfileInline(TranslatableTabularInline):
    model = CompanyProfile
    extra = 1
    fields = ("title", "content")


class GreetingInline(TranslatableStackedInline):
    model = Greeting
    extra = 1
    fields = ("ceo_name", "message", "ceo_image")


class HistoryEventInline(TranslatableTabularInline):
    model = HistoryEvent
    extra = 1
    fields = ("year", "month", "event")


class GlobalNetworkLocationInline(TranslatableStackedInline):
    model = GlobalNetworkLocation
    extra = 1
    fields = ("name", "postal_code", "address", "phone", "order", "map_url")


class BasicContentInline(TranslatableStackedInline):
    model = BasicContent
    extra = 1
    fields = ("basic_content",)


@admin.register(Page)
class PageAdmin(SortableAdminMixin, TranslatableAdmin):
    list_display = ("title", "page_type", "slug", "is_published", "order")
    fields = ("title", "slug", "page_type", "image", "is_published")

    inlines = [
        CompanyProfileInline,
        HistoryEventInline,
        GreetingInline,
        GlobalNetworkLocationInline,
        BasicContentInline,
    ]

    class Media:
        js = ("admin/js/dynamic_inline.js",)


@admin.register(News)
class NewsAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "slug", "date", "is_published", "order")
    fields = ("title", "slug", "date", "content", "is_published")


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(TranslatableAdmin):
    list_display = ("company_name",)
    fields = (
        "company_name",
        "company_postal_code",
        "company_address",
        "company_phone",
        "company_email",
        "contact_email",
        "logo_image",
        "map_embed",
        "banner_slogan",
        "banner_description",
    )

    readonly_fields = ("pk",)  # edit ignored

    def has_add_permission(self, request, obj=None):
        # when model has data, not allow add
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # when model has data, not allow delete
        if self.model.objects.exists():
            return False
        return True


@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, TranslatableAdmin):
    list_display = ("name", "prefix", "is_active", "site_config", "order")
    fields = ("name", "prefix", "is_active", "image", "site_config")
