from django.contrib import sitemaps
from django.urls import reverse


class StaticViewi18nSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'monthly'
    i18n = True

    def items(self):
        return ['index', ]

    def location(self, item):
        return reverse(item)

