from __future__ import absolute_import, unicode_literals

from .scrapers import parser_hh, scrape_contacts

from celery import shared_task


url = "https://rostov.hh.ru/search/vacancy?clusters=true&enable_snippets=true&order_by=publication_time&search_period=1&only_with_salary=true&from=cluster_compensation&showClusters=true"


@shared_task
def scrape_ads():
    parser_hh(url)
    return

@shared_task
def contacts_collector():
    scrape_contacts()
    return
