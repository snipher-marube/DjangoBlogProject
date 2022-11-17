from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
import markdown
from django.urls import reverse_lazy

from .models import Post

class LatestPostsFeed(Feed):
    title = 'snipherDev blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of snipherDev.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_update(self, item):
        return item.publish
