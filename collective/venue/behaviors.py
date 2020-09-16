# -*- coding: utf-8 -*-
from collective.venue import messageFactory as _
from collective.venue.utils import get_base_path
from plone import api
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from z3c.relationfield.schema import RelationChoice


@provider(IContextAwareDefaultFactory)
def default_location(context):
    """Provide default location.
    """
    default = api.portal.get_registry_record('collective.venue.default_venue')
    return default or ''


@provider(IFormFieldProvider)
class ILocation(model.Schema):

    location_ref = RelationChoice(
        title=_(u'label_event_location', default=u'Location'),
        description=_(
            u'description_event_location',
            default=u'Select a location.'),
        required=False,
        missing_value='',
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'location_ref',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['Venue'],
        }
    )

    location_notes = schema.Text(
        title=_(
            u'label_event_location_notes',
            default=u'Location notes'),
        description=_(
            u'description_event_location_notes',
            default=u'One-time location or additional Information.'),
        required=False,
        default=None,
    )
    directives.fieldset(
        'venue',
        label=_(u'fieldset_venue'),
        fields=['location_ref', 'location_notes']
    )


@provider(IContextAwareDefaultFactory)
def default_organizer(context):
    """Provide default organizer.
    """
    default = api.portal.get_registry_record(
        'collective.venue.default_organizer'
    )
    return default or ''


@provider(IFormFieldProvider)
class IOrganizer(model.Schema):

    organizer_ref = RelationChoice(
        title=_(u'label_event_organizer', default=u'Organizer'),
        description=_(
            u'description_event_organizer',
            default=u'Select an organizer.'),
        required=False,
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'organizer_ref',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Venue'],
        }
    )

    organizer_notes = schema.Text(
        title=_(
            u'label_event_organizer_notes',
            default=u'Organizer notes'),
        description=_(
            u'description_event_organizer_notes',
            default=u'One-time organizer or additional Information.'),
        required=False,
        default=None,
    )
    directives.fieldset(
        'venue',
        label=_(u'fieldset_venue'),
        fields=['organizer_ref', 'organizer_notes'],
        order=10,
    )
