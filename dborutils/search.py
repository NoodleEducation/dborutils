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
    value = re.sub(u'À|Á|Â|Ã|Ä|Å', u'A', value)
    value = re.sub(u'à|á|â|ã|ä|å', u'a', value)
    value = re.sub(u'È|É|Ê|Ë', u'E', value)
    value = re.sub(u'è|é|ê|ë', u'e', value)
    value = re.sub(u'ì|í|î|ï', u'i', value)
    value = re.sub(u'ñ', u'n', value)
    value = re.sub(u'Ñ', u'N', value)
    value = re.sub(u'ó|ō|ö', u'o', value)
    value = re.sub(u'Ó|Ō|Ö', u'O', value)
    value = re.sub(u'ù|ú|ü', u'u', value)
    value = re.sub(u'Ù|Ú|Ü', u'U', value)

    # Replace underscores with space.
    value = re.sub('_', ' ', value)

    # Replace non-word values with dash[-]. A word is digit, letter or
    # underscore.
    value = re.sub('\W+', '-', value)

    # Replace multiple dashes with single dash
    value = re.sub('\-{2,}', '-', value)

    # Strip any trailing dashes[-] and lowercase, return that value.
    return value.strip('-').lower()
