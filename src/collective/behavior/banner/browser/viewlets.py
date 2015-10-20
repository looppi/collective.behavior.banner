# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.behavior.banner.slider import ISlider
from plone.app.layout.viewlets import ViewletBase


class SliderViewlet(ViewletBase):
    """ Slider viewlet """
    slider_template = ViewPageTemplateFile('jyu_slider.pt')

    def index(self):
        return self.slider_template()

    def banners(self):
        context = aq_inner(self.context)

        slider = ISlider(context, None)
        if slider is not None:
            return [x.to_object for x in slider.slider_relation]

        for parent in self.parents:
            slider = ISlider(parent, None)
            if slider is not None:
                return [x.to_object for x in slider.slider_relation]
        return None

    @property
    def parents(self):
        """Parents of the context

        Generator to walk the acquistion chain of object, considering that it
        could be a function.

        >>> for obj in self.parents:
        >>>    pass

        See: http://plone.org/documentation/manual/developer-manual/archetypes/
        appendix-practicals/b-org-creating-content-types-the-plone-2.5-way/
        writing-a-custom-pas-plug-in
        """
        context = aq_inner(self.context)

        while context is not None:
            yield context

            funcObject = getattr(context, "im_self", None)
            if funcObject is not None:
                context = aq_inner(funcObject)
            else:
                # Don't use aq_inner() since portal_factory (and probably
                # other)things, depends on being able to wrap itself in a fake
                # context.
                context = aq_parent(context)
