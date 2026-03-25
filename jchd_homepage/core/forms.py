import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact


class ContactForm(forms.ModelForm):
    agree = forms.BooleanField(
        required=True,
        error_messages={
            "required": _("送信するにはプライバシーポリシーへの同意が必要です。")
        },
    )

    email_confirm = forms.EmailField(
        label=_("メールアドレス(確認)"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("確認のため、もう一度入力してください"),
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
            }
        ),
    )

    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            "last_name": forms.TextInput(attrs={"placeholder": _("姓")}),
            "first_name": forms.TextInput(attrs={"placeholder": _("名")}),
            "last_name_kana": forms.TextInput(attrs={"placeholder": _("セイ")}),
            "first_name_kana": forms.TextInput(attrs={"placeholder": _("メイ")}),
            "email": forms.EmailInput(
                attrs={"placeholder": _("例: example@domain.com")}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": _("例: 03-1111-1111")}
            ),
            "detail": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
            "contact_method": forms.RadioSelect(),
            "phone_type": forms.RadioSelect(),
            "content_type": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Assign a general CSS class (excluding inputs, textareas, and selects)
        common_classes = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"

        for field_name, field in self.fields.items():
            # 1.1 Remove label suffix
            field.label_suffix = ""

            # 1.2 Assign a general CSS class
            if not isinstance(field.widget, forms.RadioSelect):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (
                    f"{common_classes} {existing_classes}".strip()
                )
            else:
                # 1.3 Assign a specific CSS class for RadioSelect
                if field_name in ["contact_method", "phone_type"]:
                    # Horizontal layout for contact_method and phone_type
                    field.widget.attrs["class"] = "inline-flex gap-6"
                elif field_name == "content_type":
                    # Vertical layout for content_type
                    field.widget.attrs["class"] = "flex-col inline-flex gap-3"

    def clean(self):
        cleaned_data = super().clean()

        # Email confirm
        email = cleaned_data.get("email")
        email_confirm = cleaned_data.get("email_confirm")

        if email and email_confirm and email != email_confirm:
            self.add_error(
                "email_confirm",
                _("メールアドレスが一致しません。もう一度入力してください。"),
            )

        # Free email
        if email:
            free_domains = [
                "gmail.com",
                "yahoo.co.jp",
                "yahoo.com",
                "hotmail.com",
                "outlook.com",
            ]
            domain = email.split("@")[-1].lower()
            if domain in free_domains:
                self.add_error(
                    "email",
                    _(
                        "フリーメールアドレスはご利用いただけません。会社・学校のメールアドレスをご利用ください。"
                    ),
                )

        # if choosed "採用に関するお問い合わせ", age is required
        content_type = cleaned_data.get("content_type")
        age = cleaned_data.get("age")
        if content_type == "recruit" and age is None:
            self.add_error(
                "age", _("採用に関するお問い合わせの場合、年齢の入力は必須です。")
            )

        return cleaned_data

    # Custom validation
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        # Regex cho số điện thoại Nhật (di động hoặc bàn)
        if not re.match(r"^(0\d{1,4}-\d{1,4}-\d{4}|0\d{9,10})$", phone):
            raise forms.ValidationError(_("有効な電話番号を入力してください。"))
        return phone

    def clean_last_name_kana(self):
        data = self.cleaned_data.get("last_name_kana")
        if not re.match(r"^[ァ-ヶー]+$", data):
            raise forms.ValidationError(_("全角カタカナで入力してください。"))
        return data

    def clean_first_name_kana(self):
        data = self.cleaned_data.get("first_name_kana")
        if not re.match(r"^[ァ-ヶー]+$", data):
            raise forms.ValidationError(_("全角カタカナで入力してください。"))
        return data
