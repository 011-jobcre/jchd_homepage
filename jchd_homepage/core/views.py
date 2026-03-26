from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, View

from .forms import ContactForm
from .models import News, Page


class HomeView(ListView):
    template_name = "home.html"

    def get(self, request):
        # products = Product.objects.all()[:3]
        news = News.objects.all()[:3]
        return render(request, self.template_name, {"news": news})


class AboutView:
    def about_list(request):
        pages = Page.objects.filter(is_published=True)
        return render(request, "about_list.html", {"pages": pages})

    def page_detail(request, slug):
        page = get_object_or_404(Page, slug=slug, is_published=True)

        custom_breadcrumbs = [
            {"name": _("企業情報一覧"), "url": reverse("about")},
            {
                "name": page.title,
                "url": "",
            },
        ]

        context = {"page": page, "custom_breadcrumbs": custom_breadcrumbs}

        if page.page_type == "company_profile":
            context["profile_entries"] = page.company_profiles.all()
        elif page.page_type == "history":
            context["history_events"] = page.history_events.all()
        elif page.page_type == "global_network":
            context["global_networks"] = page.global_networks.all()
        elif page.page_type == "basic_content":
            page.greetings if hasattr(page, "basic_contents") else None
        elif page.page_type == "greeting":
            context["greetings"] = (
                page.greetings if hasattr(page, "greetings") else None
            )

        return render(request, "page_detail.html", context)


class NewsView:
    def news_list(request):
        news_list = News.objects.filter(is_published=True)

        paginator = Paginator(news_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "news_list": page_obj,
            "page_obj": page_obj,
        }

        return render(request, "news_list.html", context)

    def news_detail(request, slug):
        news_detail = get_object_or_404(News, slug=slug, is_published=True)

        custom_breadcrumbs = [
            {"name": _("ニュース一覧"), "url": reverse("news")},
            {
                "name": news_detail.title,
                "url": "",
            },
        ]

        # get next/previous news based on date
        try:
            next_news = news_detail.get_next_by_date()
        except News.DoesNotExist:
            next_news = None

        try:
            previous_news = news_detail.get_previous_by_date()
        except News.DoesNotExist:
            previous_news = None

        context = {
            "news_detail": news_detail,
            "next_news": next_news,
            "previous_news": previous_news,
            "custom_breadcrumbs": custom_breadcrumbs,
        }

        return render(request, "news_detail.html", context)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "contact.html", {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Lưu dữ liệu vào session để dùng ở trang confirm
            request.session["contact_data"] = request.POST
            return redirect("contact_confirm")
        return render(request, "contact.html", {"form": form})


class ContactConfirmView(View):
    def get(self, request):
        data = request.session.get("contact_data")
        if not data:
            return redirect("contact")

        form = ContactForm(data)
        return render(request, "contact_confirm.html", {"form": form, "data": data})

    def post(self, request):
        data = request.session.get("contact_data")
        if not data:
            return redirect("contact")

        form = ContactForm(data)
        if form.is_valid():
            form.save()
            del request.session["contact_data"]
            return render(request, "contact_success.html")
        return redirect("contact")
