from django.db import models
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from model_utils import Choices

import common.models as common
from . import blocks

class HomePage(common.GenericPage):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/首页'
    template = 'ncrcrd/homepage.html'

    # 首页不需要 content，这里继承 GenericPage，并设默认值为空，并且，
    # 该项不显示在编辑页面中
    content = StreamField([], null=True, blank=True, default=None)

    # 轮播图
    carousel = StreamField([
        ('carousel', blocks.CarouselItemBlock()),
        ], verbose_name='轮播图配置')

    # 要闻动态内容
    news = StreamField([
        ('news', blocks.NewsItemBlock()),
        ], verbose_name='要闻动态配置')

    # 要闻动态 More 链接到的页面
    more_news_page = models.ForeignKey(
            'wagtailcore.Page',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+',
            )

    content_panels = Page.content_panels + [
            StreamFieldPanel('carousel'),
            StreamFieldPanel('news'),
            PageChooserPanel('more_news_page'),
            ]


    # 只允许使用 HomePage 创建一个页面，方法见：https://stackoverflow.com/a/37168102/369018
    # 这里的两个限制：1、HomePage 不能成为其他类型页面的子页面 2、只能有一个
    parent_page_types = ['wagtailcore.Page']
    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super().can_create_at(parent) and not cls.objects.exists()

class ArticlePage(common.GenericPage):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/一般文章页'
    template = 'ncrcrd/article.html'

    content = StreamField([
        ('title', blocks.TitleBlock()),
        ('heading', blocks.HeadingBlock()),
        ('paragraph', blocks.ParagraphBlock()),
        ('image', blocks.ImageBlock()),
        ('person_card', blocks.PersonCardBlock()),
        ('organization_card', blocks.OrganizationCardBlock()),
        ('study_card', blocks.StudyCardBlock()),
        ('book_card', blocks.BookCardBlock()),
        ('table', TableBlock(label='表格')),
        ('table_corporation', TableBlock(label='协作单位表格', template='ncrcrd/blocks/table_corporation.html')),
        ('table_guide', TableBlock(label='指南规范表格', template='ncrcrd/blocks/table_guide.html')),
        ], verbose_name='正文')

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')

# 科研培训文章页
class CoursePage(common.GenericPage):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/科研培训文章页'
    template = 'ncrcrd/course.html'

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')

    # 卡片的标题、简介
    cover_title = models.TextField(verbose_name='封面标题')
    cover_introduction = models.TextField(verbose_name='封面介绍')
    # 封面图片，用于渲染科研培训文章列表页中的卡片
    cover_picture = models.ForeignKey(
            'wagtailimages.Image',
            on_delete=models.PROTECT,
            related_name='ncrcrd_course_cover_pictures',
            verbose_name='封面图片',
            )

    content = StreamField([
        ('title', blocks.TitleBlock()),
        ('heading', blocks.HeadingBlock()),
        ('paragraph', blocks.ParagraphBlock()),
        ('image', blocks.ImageBlock()),
        ('person_card', blocks.PersonCardBlock()),
        ('organization_card', blocks.OrganizationCardBlock()),
        ('study_card', blocks.StudyCardBlock()),
        ('book_card', blocks.BookCardBlock()),
        ('table', TableBlock()),
        ], verbose_name='正文')

    content_panels = [
            FieldPanel('cover_title'),
            FieldPanel('cover_introduction'),
            ImageChooserPanel('cover_picture'),
            ] + common.GenericPage.content_panels

# 科研培训列表页
class CourseListPage(Page):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/科研培训文章列表页'
    template = 'ncrcrd/course-list.html'

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')

    subpage_types = ['CoursePage']

    def get_context(self, request):
        context = super().get_context(request)

        all_articles = CoursePage.objects.live()

        paginator = Paginator(all_articles, 5)
        page = request.GET.get('page', 1)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['paginator'] = paginator

        return context

NEWS_CATEGORIES = Choices(
        ('来访专家', '来访专家'),
        ('海外交流', '海外交流'),
        ('会议报导', '会议报导'),
        ('新闻动态', '新闻动态'),
        ('科普宣教', '科普宣教'),
        )

class NewsPage(common.GenericPage):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/新闻页'
    template = 'ncrcrd/news.html'

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')
    breadcrumb_title = models.TextField(default='新闻详情', blank=True,
            verbose_name='面包屑导航显示标题',
            help_text='不填时默认为页面标题',
            )

    # 文章分类。这里最好是使用 ForeignKey ，单独用一个表来维护分类列表。但那样的话，我们现在还需要
    # 额外开发一个管理分类列表的功能。目前我们暂时先直接保存明文，检索（新闻列表页）时直接用 LIKE
    # 语句去匹配。
    category_name = models.TextField(verbose_name='文章分类', choices=NEWS_CATEGORIES, help_text='如需添加新的分类，请与开发沟通')

    # 卡片的标题、简介
    cover_title = models.TextField(verbose_name='封面标题')
    cover_introduction = models.TextField(verbose_name='封面介绍')
    # 封面图片，用于渲染科研培训文章列表页中的卡片
    cover_picture = models.ForeignKey(
            'wagtailimages.Image',
            on_delete=models.PROTECT,
            related_name='ncrcrd_news_cover_pictures',
            verbose_name='封面图片',
            )

    publish_date = models.DateField(verbose_name='发布时间', help_text='这里控制的是显示出来的发布时间')

    content = StreamField([
        ('title', blocks.TitleBlock()),
        ('heading', blocks.HeadingBlock()),
        ('paragraph', blocks.ParagraphBlock()),
        ('image', blocks.ImageBlock()),
        ('person_card', blocks.PersonCardBlock()),
        ('organization_card', blocks.OrganizationCardBlock()),
        ('study_card', blocks.StudyCardBlock()),
        ('book_card', blocks.BookCardBlock()),
        ('table', TableBlock()),
        ], verbose_name='正文')

    content_panels = [
            MultiFieldPanel([
                FieldPanel('cover_title'),
                FieldPanel('cover_introduction'),
                ImageChooserPanel('cover_picture'),
                ], heading='卡片设置'),
            FieldPanel('category_name', widget=forms.Select()),
            FieldPanel('publish_date'),
            ] + common.GenericPage.content_panels

class NewsListPage(Page):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/新闻列表页'
    template = 'ncrcrd/news-list.html'

    category_name = models.TextField(verbose_name='文章分类', choices=NEWS_CATEGORIES, help_text='如需添加新的分类，请与开发沟通')

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')

    content_panels = Page.content_panels + [
        FieldPanel('category_name', widget=forms.Select()),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        all_articles = NewsPage.objects.live().order_by('-publish_date')

        paginator = Paginator(all_articles, 5)
        page = request.GET.get('page', 1)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['paginator'] = paginator

        return context

class RedirectPage(common.RedirectPage):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/跳转页面'

# 论文内页
class PaperPage(Page):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/论文信息页'
    template = 'ncrcrd/paper.html'

    # 卡片的标题、简介
    introduction = models.TextField(verbose_name='论文介绍')
    magazine = models.CharField(verbose_name='期刊名称',max_length=255)
    published_at = models.DateField(verbose_name='发布年份',help_text='精确到年份即可')
    authors = models.CharField(verbose_name='作者',help_text='多位作者请用分隔符分割',max_length=255)
    link = models.URLField(verbose_name='论文链接',blank=True)

    parent_page_types = ['PaperListPage']

    content_panels = Page.content_panels + [
            FieldPanel('introduction'),
            FieldPanel('magazine'),
            FieldPanel('link'),
            FieldPanel('published_at'),
            FieldPanel('authors'),
            ]

# 科研培训列表页
class PaperListPage(Page):
    class Meta:
        verbose_name = '呼吸疾病中心页面模板/论文列表页'
    template = 'ncrcrd/paper-list.html'

    show_sidebar = models.BooleanField(default=True, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=True, verbose_name='显示面包屑导航')

    subpage_types = ['PaperPage']

    def get_context(self, request):
        context = super().get_context(request)

        all_articles = PaperPage.objects.live()

        paginator = Paginator(all_articles, 5)
        page = request.GET.get('page', 1)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['paginator'] = paginator

        return context
