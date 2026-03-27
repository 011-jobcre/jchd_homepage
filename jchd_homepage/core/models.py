import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields

# ------------------------------------------------------------------


class Page(TranslatableModel):
    PAGE_TYPE_CHOICES = [
        ("basic_content", "Basic Content"),
        ("company_profile", "Company Profile"),
        ("greeting", "Greeting / Message"),
        ("history", "History Timeline"),
        ("global_network", "Global Network"),
    ]

    translations = TranslatedFields(
        # Example Title: "会社概要", "代表挨拶", "沿革", "経営方針", "グローバルネットワーク"
        title=models.CharField(
            verbose_name=_("タイトル"),
            max_length=200,
            help_text="ページのタイトルを入力します。",
        ),
    )

    # company-profile, greeting, history, management policies, global-network
    slug = models.SlugField(
        verbose_name=_("スラッグ"),
        max_length=200,
        unique=True,
        help_text="URLに使用されるスラッグを入力します。",
    )
    page_type = models.CharField(
        verbose_name=_("ページタイプ"),
        choices=PAGE_TYPE_CHOICES,
        default="basic_content",
        help_text="ページのタイプを選択します。",
    )
    order = models.PositiveIntegerField(
        verbose_name=_("並び順"),
        db_index=True,
        help_text="ページの表示順序を指定します。",
    )
    # Image for each page
    image = models.ImageField(
        verbose_name=_("イメージ"),
        upload_to="about_img/",
        blank=True,
        null=True,
        help_text="ページのイメージをアップロードします。",
    )
    is_published = models.BooleanField(
        verbose_name=_("公開済み"),
        default=True,
        help_text="ページを公開するかどうかを設定します。",
    )

    class Meta:
        verbose_name = _("企業情報")
        verbose_name_plural = _("企業情報一覧")
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} ({self.get_page_type_display()})"


class CompanyProfile(TranslatableModel):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="company_profiles"
    )

    translations = TranslatedFields(
        title=models.CharField(
            verbose_name=_("タイトル"),
            max_length=20,
            help_text="タイトルを入力します。",
        ),
        content=models.CharField(
            verbose_name=_("コンテンツ"), help_text="コンテンツを入力します。"
        ),
    )

    class Meta:
        verbose_name = _("会社概要")
        verbose_name_plural = _("会社概要一覧")

    def __str__(self):
        return f"{self.title}"


class HistoryEvent(TranslatableModel):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="history_events"
    )

    translations = TranslatedFields(
        event=models.TextField(
            verbose_name=_("イベント"), help_text="イベントを入力します。"
        )
    )

    current_year = datetime.date.today().year
    current_month = datetime.date.today().month

    YEAR_CHOICES = [(y, y) for y in range(1900, current_year + 5)]
    MONTH_CHOICES = [
        (1, _("1月")),
        (2, _("2月")),
        (3, _("3月")),
        (4, _("4月")),
        (5, _("5月")),
        (6, _("6月")),
        (7, _("7月")),
        (8, _("8月")),
        (9, _("9月")),
        (10, _("10月")),
        (11, _("11月")),
        (12, _("12月")),
    ]

    year = models.IntegerField(
        verbose_name=_("年"), choices=YEAR_CHOICES, default=current_year
    )

    month = models.IntegerField(
        verbose_name=_("月"), choices=MONTH_CHOICES, default=current_month
    )

    class Meta:
        verbose_name = _("沿革")
        verbose_name_plural = _("沿革一覧")
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.year}/{self.month}"


class Greeting(TranslatableModel):
    page = models.OneToOneField(
        Page, on_delete=models.CASCADE, related_name="greetings"
    )

    translations = TranslatedFields(
        ceo_name=models.CharField(
            verbose_name=_("代表取締役氏名"),
            max_length=100,
            default="CEO Name",
            help_text="代表取締役氏名を入力します。",
        ),
        message=CKEditor5Field(
            verbose_name=_("メッセージ"),
            help_text="メッセージを入力します。",
            config_name="extends",
        ),
    )

    ceo_image = models.ImageField(
        verbose_name=_("CEOイメージ"),
        upload_to="about_img/greeting_ceo_img/",
        blank=True,
        help_text="代表取締役のイメージをアップロードします。",
    )

    class Meta:
        verbose_name = _("代表挨拶")
        verbose_name_plural = _("代表挨拶一覧")

    def __str__(self):
        return f"Greeting for {self.page.title}"


class GlobalNetworkLocation(TranslatableModel):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="global_networks"
    )

    translations = TranslatedFields(
        # e.g., 本社, 東京営業所
        name=models.CharField(
            verbose_name=_("拠点名"), max_length=200, help_text="拠点名を入力します。"
        ),
        address=models.CharField(
            verbose_name=_("住所"), max_length=200, help_text="住所を入力します。"
        ),
    )
    # 〒824-0005
    postal_code = models.CharField(
        verbose_name=_("郵便番号"),
        max_length=8,
        blank=True,
        null=True,
        help_text="郵便番号を入力します。",
    )
    # 行橋市中央3丁目5番25号
    phone = models.CharField(
        verbose_name="TEL",
        max_length=50,
        blank=True,
        null=True,
        help_text="電話番号を入力します。",
    )
    # https://maps.google.com/?q=行橋市中央3丁目5番25号
    map_url = models.URLField(
        verbose_name="Google Maps URL",
        blank=True,
        null=True,
        help_text="Google Maps URL を入力します。",
    )
    order = models.PositiveIntegerField(
        verbose_name=_("並び順"),
        default=0,
        help_text="拠点の表示順序を指定します。",
    )

    class Meta:
        verbose_name = _("拠点")
        verbose_name_plural = _("拠点一覧")
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.order:
            last_order = (
                GlobalNetworkLocation.objects.filter(page=self.page)
                .order_by("-order")
                .first()
            )
            self.order = last_order.order + 1 if last_order else 1
        return super().save(*args, **kwargs)


class BasicContent(TranslatableModel):
    page = models.OneToOneField(
        Page, on_delete=models.CASCADE, related_name="basic_contents"
    )

    translations = TranslatedFields(
        basic_content=CKEditor5Field(
            verbose_name=_("基本コンテンツ"),
            help_text="ページの基本コンテンツを入力します。",
            null=True,
            blank=True,
            config_name="extends",
        ),
    )

    class Meta:
        verbose_name = _("基本コンテンツ")
        verbose_name_plural = _("基本コンテンツ一覧")

    def __str__(self):
        return f"Basic Content for {self.page.title}"


class News(models.Model):
    title = models.CharField(
        verbose_name=_("タイトル"),
        max_length=200,
        help_text="ニュースのタイトルを入力します。",
    )
    slug = models.SlugField(
        verbose_name=_("スラッグ"),
        max_length=100,
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text="URLに使用されるスラッグを入力します。",
    )
    order = models.PositiveIntegerField(
        verbose_name=_("並び順"),
        db_index=True,
        help_text="ニュースの表示順序を指定します。",
    )
    date = models.DateField(
        verbose_name=_("日付"), default=timezone.now, help_text="日付を入力します。"
    )
    content = CKEditor5Field(
        verbose_name=_("内容"),
        help_text="ニュースの内容を入力します。",
        config_name="extends",
    )
    is_published = models.BooleanField(
        verbose_name=_("公開済み"),
        default=True,
        help_text="ニュースを公開するかどうかを設定します。",
    )
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日", auto_now=True)

    @property
    def is_recent(self):
        # Check if the news is within the last 7 days
        now = timezone.now().date()
        return now - datetime.timedelta(days=7) <= self.date <= now

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not set
            # Format 1: YYYY-MM-DD-title
            date_str = self.date.strftime("%Y-%m-%d")
            base_slug = f"{date_str}-{slugify(self.title, allow_unicode=True)}"

            self.slug = base_slug

            # Check if the slug already exists
            original_slug = self.slug
            counter = 1
            while News.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("ニュース")
        verbose_name_plural = _("ニュース一覧")
        ordering = ["-order", "-date"]

    def __str__(self):
        return self.title


# ------------------------------------------------------------------


class Prefecture(models.TextChoices):
    # Hokkaido
    HOKKAIDO = "hokkaido", _("北海道")

    # Tohoku
    AOMORI = "aomori", _("青森県")
    IWATE = "iwate", _("岩手県")
    MIYAGI = "miyagi", _("宮城県")
    AKITA = "akita", _("秋田県")
    YAMAGATA = "yamagata", _("山形県")
    FUKUSHIMA = "fukushima", _("福島県")

    # Kanto
    IBARAKI = "ibaraki", _("茨城県")
    TOCHIGI = "tochigi", _("栃木県")
    GUNMA = "gunma", _("群馬県")
    SAITAMA = "saitama", _("埼玉県")
    CHIBA = "chiba", _("千葉県")
    TOKYO = "tokyo", _("東京都")
    KANAGAWA = "kanagawa", _("神奈川県")

    # Chubu
    NIIGATA = "niigata", _("新潟県")
    TOYAMA = "toyama", _("富山県")
    ISHIKAWA = "ishikawa", _("石川県")
    FUKUI = "fukui", _("福井県")
    YAMANASHI = "yamanashi", _("山梨県")
    NAGANO = "nagano", _("長野県")
    GIFU = "gifu", _("岐阜県")
    SHIZUOKA = "shizuoka", _("静岡県")
    AICHI = "aichi", _("愛知県")

    # Kansai
    MIE = "mie", _("三重県")
    SHIGA = "shiga", _("滋賀県")
    KYOTO = "kyoto", _("京都府")
    OSAKA = "osaka", _("大阪府")
    HYOGO = "hyogo", _("兵庫県")
    NARA = "nara", _("奈良県")
    WAKAYAMA = "wakayama", _("和歌山県")

    # Chugoku
    TOTTORI = "tottori", _("鳥取県")
    SHIMANE = "shimane", _("島根県")
    OKAYAMA = "okayama", _("岡山県")
    HIROSHIMA = "hiroshima", _("広島県")
    YAMAGUCHI = "yamaguchi", _("山口県")

    # Shikoku
    TOKUSHIMA = "tokushima", _("徳島県")
    KAGAWA = "kagawa", _("香川県")
    EHIME = "ehime", _("愛媛県")
    KOCHI = "kochi", _("高知県")

    # Kyushu / Okinawa
    FUKUOKA = "fukuoka", _("福岡県")
    SAGA = "saga", _("佐賀県")
    NAGASAKI = "nagasaki", _("長崎県")
    KUMAMOTO = "kumamoto", _("熊本県")
    OITA = "oita", _("大分県")
    MIYAZAKI = "miyazaki", _("宮崎県")
    KAGOSHIMA = "kagoshima", _("鹿児島県")
    OKINAWA = "okinawa", _("沖縄県")


# ------------------------------------------------------------------


class Contact(models.Model):
    company_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("学校名 / 法人名")
    )

    last_name = models.CharField(max_length=50, verbose_name=_("姓"))
    first_name = models.CharField(max_length=50, verbose_name=_("名"))
    last_name_kana = models.CharField(max_length=50, verbose_name=_("セイ"))
    first_name_kana = models.CharField(max_length=50, verbose_name=_("メイ"))

    age = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("年齢"))
    gender = models.CharField(
        max_length=10,
        choices=[("male", _("男性")), ("female", _("女性"))],
        blank=True,
        verbose_name=_("性別"),
    )

    email = models.EmailField(verbose_name=_("メールアドレス"))
    email_confirm = models.EmailField(verbose_name=_("メールアドレス(確認)"))
    contact_method = models.CharField(
        max_length=10,
        choices=[("email", _("メール")), ("phone", _("電話"))],
        default="email",
        verbose_name=_("ご連絡方法"),
    )

    phone_number = models.CharField(max_length=20, verbose_name=_("電話番号"))
    phone_type = models.CharField(
        max_length=10,
        choices=[("home", _("自宅")), ("work", _("勤務先")), ("mobile", _("携帯"))],
        default="home",
        verbose_name=_("電話種別"),
    )

    prefecture = models.CharField(
        max_length=50,
        choices=Prefecture.choices,
        verbose_name=_("都道府県"),
        blank=True,
    )
    contact_time = models.CharField(
        max_length=50,
        choices=[
            ("nothing", _("特に希望なし")),
            ("morning", _("午前")),
            ("afternoon", _("午後")),
            ("evening", _("夕方以降")),
        ],
        default="nothing",
        verbose_name=_("時間帯"),
    )

    content_type = models.CharField(
        max_length=50,
        choices=[
            ("service", _("サービスに関するお問い合わせ")),
            ("recruit", _("採用に関するお問い合わせ")),
            ("other", _("その他")),
        ],
        default="service",
        verbose_name=_("内容"),
    )
    detail = models.TextField(verbose_name=_("詳細"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("送信日時"))
    is_processed = models.BooleanField(
        verbose_name=_("対応済み"),
        default=False,
        help_text=_("対応済みかどうかを指定します。"),
    )

    class Meta:
        verbose_name = "お問い合わせ"
        verbose_name_plural = "お問い合わせ一覧"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.get_content_type_display()}"


# ------------------------------------------------------------------


class SiteConfiguration(TranslatableModel):
    translations = TranslatedFields(
        company_name=models.CharField(
            verbose_name=_("会社名"),
            max_length=200,
            help_text="会社名を入力します。",
        ),
        company_address=models.CharField(
            verbose_name=_("住所"), max_length=200, help_text="住所を入力します。"
        ),
        banner_slogan=CKEditor5Field(
            verbose_name=_("バナーのスローガン"),
            help_text="バナーのスローガンを入力します。",
            config_name="extends",
            null=True,
            blank=True,
        ),
        banner_description=CKEditor5Field(
            verbose_name=_("バナーの説明文"),
            help_text="バナーの説明文を入力します。",
            config_name="extends",
            null=True,
            blank=True,
        ),
    )

    company_postal_code = models.CharField(
        verbose_name=_("郵便番号"), max_length=8, help_text="郵便番号を入力します。"
    )
    company_phone = models.CharField(
        verbose_name="TEL",
        max_length=50,
        help_text="電話番号を入力します。",
    )
    company_email = models.EmailField(
        verbose_name=_("メールアドレス"),
        max_length=50,
        help_text="メールアドレスを入力します。",
    )
    logo_image = models.ImageField(
        verbose_name=_("ロゴイメージ"),
        upload_to="logo/",
        blank=True,
        null=True,
        help_text="ロゴ画像をアップロードします。",
    )
    map_embed = models.TextField(
        verbose_name=_("Google Maps埋め込みコード"),
        blank=True,
        null=True,
        help_text="Google Maps埋め込みコードを入力します。",
    )
    contact_email = models.CharField(
        verbose_name=_("お問い合わせ通知用メールアドレス"),
        max_length=255,
        help_text="お問い合わせがあった際に通知を送信するメールアドレスを入力します。複数を指定する場合はカンマ(,)で区切ってください。",
    )

    # ----------------- Singleton pattern -----------------
    _singleton_instance = None

    @classmethod
    def get_solo(cls):
        # Don't cache for translatable models to ensure language switching works properly
        instance, created = cls.objects.get_or_create(pk=1)
        if created:
            # can set default values here if needed
            pass
        return instance

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        type(self)._singleton_instance = None

    # -----------------

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = _("サイト構成")
        verbose_name_plural = _("サイト構成一覧")


# ------------------------------------------------------------------


class MenuItem(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            max_length=100,
            verbose_name=_("メニュー項目"),
            help_text="メニュー項目を入力します。",
        ),
    )

    site_config = models.ForeignKey(
        SiteConfiguration,
        verbose_name=_("サイト構成"),
        on_delete=models.CASCADE,
        related_name="menu_items",
        default=SiteConfiguration.get_solo,
        help_text="メニュー項目を入力します。",
    )
    prefix = models.CharField(
        max_length=200,
        blank=True,
        help_text="Prefix を入力します。 e.g., about, news, contact, etc.",
    )
    is_active = models.BooleanField(
        verbose_name=_("表示する"),
        default=True,
        help_text="メニュー項目を表示するかどうかを選択します。",
    )
    image = models.ImageField(
        verbose_name=_("イメージ"),
        upload_to="menu_img/",
        blank=True,
        null=True,
        help_text="メニュー項目のイメージをアップロードします。",
    )

    order = models.PositiveIntegerField(
        verbose_name=_("並び順"),
        db_index=True,
        help_text="メニュー項目の並び順を入力します。",
    )

    class Meta:
        verbose_name = _("メニュー項目")
        verbose_name_plural = _("メニュー項目一覧")
        ordering = ["order"]

    def __str__(self):
        return self.name


# ------------------------------------------------------------------
