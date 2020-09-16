# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.venue.behaviors import ILocation
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.event.dx.interfaces import IDXEvent
from plone.app.uuid.utils import uuidToObject
from plone.event.interfaces import IEventAccessor
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer
from .utils import join_nonempty


@adapter(IDXEvent)
@implementer(IEventAccessor)
class VenueEventAccessor(EventAccessor):
    def __init__(self, context):
        super(VenueEventAccessor, self).__init__(context)
        del self._behavior_map["location"]

    @property
    def _location_link_template(self):
        return u'<a class="pat-plone-modal" href="{url}" title="{address}">{title}</a>'  # noqa

    @property
    def _default_location_template(self):
        return u"<span>{location}</span>"

    @property
    def default_location(self):
        location = getattr(self.context, "location", "")
        if not location:
            return ""
        return self._default_location_template.format(location=location)

    @property
    def location(self):
        context = self.context

        location_behavior = ILocation(context, None)
        if not location_behavior:
            return self.default_location
        location_ref = location_behavior.location_ref
        if not location_ref:
            return self.default_location

        location_notes = location_behavior.location_notes
        location = location_ref.to_object
        if not location:
            return self.default_location

        meta_basic = IBasic(location, None)
        add = IAddress(location, None)

        ret = u""
        if meta_basic and add:
            # I'm a location reference.
            # Create a link with href, title and urltext.

            # construct url to location
            site = getSite()
            location_url = location.absolute_url()
            site_path = u"/".join(site.getPhysicalPath())
            location_path = u"/".join(location.getPhysicalPath())
            if site_path not in location_path:
                # location in different site - cannot directly open it
                location_url = u"{0}/@@venue_view?uid={1}".format(
                    site.absolute_url(), location.UID()
                )

            country = get_pycountry_name(add.country)
            ret = self._location_link_template.format(  # noqa
                url=location_url,
                address=join_nonempty(
                    (
                        add.street,
                        join_nonempty((add.zip_code, add.city), sep=u" "),
                        country,
                    ),
                    sep=u", ",
                ),
                title=meta_basic.title,
            )

        ret = safe_unicode(ret)
        location_notes = safe_unicode(location_notes)
        if location_url:
            location_url = u'<a href="{0}">{0}</a>'.format(location_url)
        ret = join_nonempty([ret, location_notes, location_url], u". ")

        return ret

    @location.setter
    def location(self, value):
        acc = ILocation(self.context)
        acc.location_notes = safe_unicode(value)
