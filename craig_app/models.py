from django.db import models


class Search(models.Model):
    search_text = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_text

    class Meta:
        verbose_name_plural = 'Searches'
        # to correct the plural spelling of 'Search' in the admin interface
