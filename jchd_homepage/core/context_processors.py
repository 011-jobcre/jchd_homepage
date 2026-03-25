from .models import Page, SiteConfiguration


def about_pages(request):
    return {"pages": Page.objects.filter(is_published=True).order_by("order")}


def menu_pages(request):
    config = SiteConfiguration.get_solo()
    menu_items = config.menu_items.filter(is_active=True).order_by("order")

    return {
        "menu_items": {item.key: item for item in menu_items},
        "sorted_menu_items": list(menu_items),
    }
