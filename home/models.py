from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from taggit.models import Tag
from wagtailcodeblocknocss.blocks import CodeBlock

from wagtail.snippets.models import register_snippet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    max_count = 1
    subpage_types=['BlogPage']

    def get_context(self, request):
        context = super().get_context(request)

        if(request.GET.get('tag')):
            tag = request.GET.get('tag')
            blogpages = BlogPage.objects.filter(tags__name=tag).order_by('-first_published_at')
        else:
            blogpages=BlogPage.objects.live().order_by('-first_published_at')

        paginator = Paginator(blogpages, 5)
        page = request.GET.get('page')

        try:
            resourcesBlogpages = paginator.page(page)
        except PageNotAnInteger:
            resourcesBlogpages = paginator.page(1)
        except EmptyPage:
            resourcesBlogpages = paginator.page(paginator.num_pages)


        context['blogpages'] = resourcesBlogpages
        context['getAllTags'] = Tag.objects.all()
        context['lastPosts'] = BlogPage.objects.live().order_by('-first_published_at')[:5]
        return context



class BlogPage(Page):
    date = models.DateField("Post date")
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    subpage_types = []
    parent_page_types = ['HomePage']

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('code' , CodeBlock(label='Code')),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        FieldPanel('tags')
    ]

    def get_context(self, request):
        context = super().get_context(request)

        context['getAllTags'] = Tag.objects.all()
        context['lastPosts'] = BlogPage.objects.live().order_by('-first_published_at')[:5]
        return context


@register_snippet
class Footer(models.Model):

    body = RichTextField()

    panels = [
        FieldPanel('body')
    ]

    class Meta:
        verbose_name = "Футер"
        verbose_name_plural = "Футеры"

    def __str__(self):
        return "Футер"
