# -*- coding: utf-8 -*-

import re


def get_slug_label_facet_value(value):
    """
    Get slug/label facet value required for facets fields.
    :param value:
    :return:
    """
    return u"{0}->>{1}".format(landing_page_slugify(value), value)


def landing_page_slugify(value):
    """
    Custom slugify function for landing page urls, which allows us to create
    seo-friendly and human readable urls. It is vital that this stays
    consistent with the landing page slugifier in our Django app.
    """
    # Replace special characters with their English equivalent.
    value = re.sub('À|Á|Â|Ã|Ä|Å', 'A', value)
    value = re.sub('à|á|â|ã|ä|å', 'a', value)
    value = re.sub('È|É|Ê|Ë', 'E', value)
    value = re.sub('è|é|ê|ë', 'e', value)
    value = re.sub('ì|í|î|ï', 'i', value)
    value = re.sub('ñ', 'n', value)
    value = re.sub('Ñ', 'N', value)
    value = re.sub('ó|ō|ö', 'o', value)
    value = re.sub('Ó|Ō|Ö', 'O', value)
    value = re.sub('ù|ú|ü', 'u', value)
    value = re.sub('Ù|Ú|Ü', 'U', value)

    # Replace underscores with space.
    value = re.sub('_', ' ', value)

    # Replace non-word values with dash[-]. A word is digit, letter or
    # underscore.
    value = re.sub('\W+', '-', value)

    # Replace multiple dashes with single dash
    value = re.sub('\-{2,}', '-', value)

    # Strip any trailing dashes[-] and lowercase, return that value.
    return value.strip('-').lower()
