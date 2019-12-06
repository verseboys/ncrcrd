# Generated by Django 2.1.4 on 2019-01-15 16:19

from django.db import migrations, models
import django.db.models.deletion
import ncrcrd.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('ncrcrd', '0007_auto_20190115_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaperListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('show_sidebar', models.BooleanField(default=True, verbose_name='显示侧边栏')),
                ('show_breadcrumb', models.BooleanField(default=True, verbose_name='显示面包屑导航')),
            ],
            options={
                'verbose_name': '呼吸疾病中心页面模板/论文列表页',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PaperPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField([('title', wagtail.core.blocks.CharBlock(icon='snippet', label='文章标题')), ('paragraph', wagtail.core.blocks.RichTextBlock(label='文章段落'))])),
                ('show_sidebar', models.BooleanField(default=False, verbose_name='显示侧边栏')),
                ('show_breadcrumb', models.BooleanField(default=False, verbose_name='显示面包屑导航')),
                ('introduction', models.TextField(verbose_name='论文介绍')),
                ('magazine', models.TextField(verbose_name='期刊名称')),
                ('published_at', models.DateField(help_text='精确到年份即可', verbose_name='发布年份')),
                ('authors', models.TextField(help_text='多位作者请用分隔符分割', verbose_name='作者')),
                ('link', models.URLField(blank=True, verbose_name='论文链接')),
            ],
            options={
                'verbose_name': '呼吸疾病中心页面模板/论文信息页',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='content',
            field=wagtail.core.fields.StreamField([('title', ncrcrd.blocks.TitleBlock()), ('heading', ncrcrd.blocks.HeadingBlock()), ('paragraph', ncrcrd.blocks.ParagraphBlock()), ('image', ncrcrd.blocks.ImageBlock()), ('person_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='照片')), ('name', wagtail.core.blocks.CharBlock(label='姓名')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('organization_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='Logo')), ('name', wagtail.core.blocks.CharBlock(label='名字')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('study_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('type', wagtail.core.blocks.CharBlock(label='项目类型')), ('leader', wagtail.core.blocks.CharBlock(label='负责人')), ('description', wagtail.core.blocks.CharBlock(label='项目简介')), ('page', wagtail.core.blocks.PageChooserBlock(label='内页链接', required=False)), ('status', wagtail.core.blocks.ChoiceBlock(choices=[('ongoing', '进行中'), ('finished', '已完成')], label='项目状态'))])), ('book_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('author', wagtail.core.blocks.CharBlock(label='作者')), ('description', wagtail.core.blocks.CharBlock(label='内容简介')), ('link', wagtail.core.blocks.URLBlock(label='外部链接', required=False)), ('picture', wagtail.images.blocks.ImageChooserBlock(label='封面图片'))])), ('table', wagtail.contrib.table_block.blocks.TableBlock())], verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='coursepage',
            name='content',
            field=wagtail.core.fields.StreamField([('title', ncrcrd.blocks.TitleBlock()), ('heading', ncrcrd.blocks.HeadingBlock()), ('paragraph', ncrcrd.blocks.ParagraphBlock()), ('image', ncrcrd.blocks.ImageBlock()), ('person_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='照片')), ('name', wagtail.core.blocks.CharBlock(label='姓名')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('organization_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='Logo')), ('name', wagtail.core.blocks.CharBlock(label='名字')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('study_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('type', wagtail.core.blocks.CharBlock(label='项目类型')), ('leader', wagtail.core.blocks.CharBlock(label='负责人')), ('description', wagtail.core.blocks.CharBlock(label='项目简介')), ('page', wagtail.core.blocks.PageChooserBlock(label='内页链接', required=False)), ('status', wagtail.core.blocks.ChoiceBlock(choices=[('ongoing', '进行中'), ('finished', '已完成')], label='项目状态'))])), ('book_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('author', wagtail.core.blocks.CharBlock(label='作者')), ('description', wagtail.core.blocks.CharBlock(label='内容简介')), ('link', wagtail.core.blocks.URLBlock(label='外部链接', required=False)), ('picture', wagtail.images.blocks.ImageChooserBlock(label='封面图片'))])), ('table', wagtail.contrib.table_block.blocks.TableBlock())], verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='newslistpage',
            name='category_name',
            field=models.TextField(choices=[('来访专家', '来访专家'), ('海外交流', '海外交流'), ('会议报导', '会议报导'), ('新闻动态', '新闻动态'), ('科普宣教', '科普宣教')], help_text='如需添加新的分类，请与开发沟通', verbose_name='文章分类'),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='category_name',
            field=models.TextField(choices=[('来访专家', '来访专家'), ('海外交流', '海外交流'), ('会议报导', '会议报导'), ('新闻动态', '新闻动态'), ('科普宣教', '科普宣教')], help_text='如需添加新的分类，请与开发沟通', verbose_name='文章分类'),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='content',
            field=wagtail.core.fields.StreamField([('title', ncrcrd.blocks.TitleBlock()), ('heading', ncrcrd.blocks.HeadingBlock()), ('paragraph', ncrcrd.blocks.ParagraphBlock()), ('image', ncrcrd.blocks.ImageBlock()), ('person_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='照片')), ('name', wagtail.core.blocks.CharBlock(label='姓名')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('organization_card', wagtail.core.blocks.StructBlock([('picture', wagtail.images.blocks.ImageChooserBlock(label='Logo')), ('name', wagtail.core.blocks.CharBlock(label='名字')), ('description', wagtail.core.blocks.CharBlock(label='简介'))])), ('study_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('type', wagtail.core.blocks.CharBlock(label='项目类型')), ('leader', wagtail.core.blocks.CharBlock(label='负责人')), ('description', wagtail.core.blocks.CharBlock(label='项目简介')), ('page', wagtail.core.blocks.PageChooserBlock(label='内页链接', required=False)), ('status', wagtail.core.blocks.ChoiceBlock(choices=[('ongoing', '进行中'), ('finished', '已完成')], label='项目状态'))])), ('book_card', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='标题')), ('author', wagtail.core.blocks.CharBlock(label='作者')), ('description', wagtail.core.blocks.CharBlock(label='内容简介')), ('link', wagtail.core.blocks.URLBlock(label='外部链接', required=False)), ('picture', wagtail.images.blocks.ImageChooserBlock(label='封面图片'))])), ('table', wagtail.contrib.table_block.blocks.TableBlock())], verbose_name='正文'),
        ),
    ]
