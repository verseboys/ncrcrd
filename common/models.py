from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel
from wagtail.core.blocks import CharBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import Http404

class GenericPage(Page):
    class Meta:
        abstract = True
        verbose_name = '公共页面模板/普通页面'

    content = StreamField([
        # 在各站点定制页面中可以添加更多 block，此处代码仅为演示。
        # 这里列出的 block 不影响数据库中的内容，数据库中，StreamField 存的是 json，
        # 这里左边的是 json 中的 key，仅用于告诉 wagtail 该使用什么类来渲染内容
        ('title', CharBlock(label='文章标题', icon='snippet')),
        ('paragraph', RichTextBlock(label='文章段落')),
        ])

    show_sidebar = models.BooleanField(default=False, verbose_name='显示侧边栏')
    show_breadcrumb = models.BooleanField(default=False, verbose_name='显示面包屑导航')
    breadcrumb_title = models.TextField(default='', blank=True,
            verbose_name='面包屑导航显示标题',
            help_text='不填时默认为页面标题',
            )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        MultiFieldPanel(
            [FieldRowPanel(
                [
                    FieldPanel('show_sidebar'),
                    FieldPanel('show_breadcrumb'),
                ]
            )],
            heading='页面属性',
        ),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('breadcrumb_title'),
    ]

    def serve(self, request):
        block_id = request.GET.get('block', None)
        if block_id:
            for block in self.content:
                if block.id == block_id:
                    return JsonResponse(data=block.value)
            raise Http404
        else:
            return super().serve(request)

class RedirectPage(Page):
    class Meta:
        abstract = True
        verbose_name = '公共页面模板/跳转页面'

    redirect_page = models.ForeignKey(
            Page,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='+',
            verbose_name='目标页面',
            )

    content_panels = Page.content_panels + [
        PageChooserPanel('redirect_page'),
    ]

    def serve(self, request):
        if self.redirect_page:
            return HttpResponseRedirect(self.redirect_page.get_url(request))
        else:
            raise Http404
