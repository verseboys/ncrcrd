from wagtail.core.blocks import CharBlock, RichTextBlock, BooleanBlock, StructBlock, ChoiceBlock, PageChooserBlock,URLBlock
from wagtail.images.blocks import ImageChooserBlock

class TitleBlock(CharBlock):
    class Meta:
        label = '文章标题'
        icon = 'title'
        template = 'ncrcrd/blocks/title.html'

class HeadingBlock(CharBlock):
    class Meta:
        label = '段落标题'
        icon = 'openquote'
        template = 'ncrcrd/blocks/heading.html'

class ParagraphBlock(RichTextBlock):
    class Meta:
        label = '富文本段落'

class ImageBlock(ImageChooserBlock):
    class Meta:
        label = '图片'

class PersonCardBlock(StructBlock):
    picture = ImageChooserBlock(label='照片')
    name = CharBlock(label='姓名')
    description = CharBlock(label='简介')

    class Meta:
        template = 'ncrcrd/blocks/person_card.html'
        label = '专家名片'
        icon = 'user'

class OrganizationCardBlock(StructBlock):
    picture = ImageChooserBlock(label='Logo')
    name = CharBlock(label='名字')
    description = CharBlock(label='简介')

    class Meta:
        template = 'ncrcrd/blocks/organization_card.html'
        label = '机构名片'
        icon = 'site'

class StudyCardBlock(StructBlock):
    title = CharBlock(label='标题')
    type = CharBlock(label='项目类型')
    leader = CharBlock(label='负责人')
    description = CharBlock(label='项目简介')
    page = PageChooserBlock(label='内页链接', required=False)
    status = ChoiceBlock(label='项目状态', choices=[
        ('ongoing', '进行中'),
        ('finished', '已完成'),
        ])

    class Meta:
        template = 'ncrcrd/blocks/study_card.html'
        label = '研究项目卡片'
        icon = 'snippet'

class BookCardBlock(StructBlock):
    title = CharBlock(label='标题')
    author = CharBlock(label='作者')
    description = CharBlock(label='内容简介')
    link = URLBlock(label='外部链接',required=False)
    picture = ImageChooserBlock(label='封面图片')

    class Meta:
        template = 'ncrcrd/blocks/book_card.html'
        label = '专著卡片'
        icon = 'edit'

# 首页轮播图单个条目
class CarouselItemBlock(StructBlock):
    title = CharBlock(label='标题')
    picture = ImageChooserBlock(label='图片')
    page = PageChooserBlock(label='文章')

    class Meta:
        template = 'ncrcrd/blocks/carousel.html'
        label = '轮播条目'

# 首页要闻单个新闻链接
class NewsItemBlock(StructBlock):
    title = CharBlock(label='标题')
    page = PageChooserBlock(label='文章')

    class Meta:
        template = 'ncrcrd/blocks/news_chooser.html'
        label = '新闻链接'
