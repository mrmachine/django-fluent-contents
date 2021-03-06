from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from fluent_contents.models import ContentItem, PlaceholderField, ContentItemRelation
from .managers import SharedContentManager


def _get_current_site():
    return Site.objects.get_current()


class SharedContent(TranslatableModel):
    """
    The parent hosting object for shared content
    """
    translations = TranslatedFields(
        title = models.CharField(_("Title"), max_length=200)
    )

    parent_site = models.ForeignKey(Site, editable=False, default=_get_current_site)
    slug = models.SlugField(_("Template code"), help_text=_("This unique name can be used refer to this content in in templates."))
    contents = PlaceholderField("shared_content", verbose_name=_("Contents"))

    # NOTE: settings such as "template_name", and which plugins are allowed can be added later.

    # Adding the reverse relation for ContentItem objects
    # causes the admin to list these objects when moving the shared content
    contentitem_set = ContentItemRelation()

    objects = SharedContentManager()

    class Meta:
        verbose_name = _("Shared content")
        verbose_name_plural = _("Shared content")
        unique_together = (
            ('parent_site', 'slug'),
        )

    def __unicode__(self):
        return self.title


class SharedContentItem(ContentItem):
    """
    The contentitem to include in a page.
    """
    shared_content = models.ForeignKey(SharedContent, verbose_name=_('Shared content'), related_name='shared_content_items')

    class Meta:
        verbose_name = _('Shared content')
        verbose_name_plural = _('Shared content')

    def __unicode__(self):
        return unicode(self.shared_content)
