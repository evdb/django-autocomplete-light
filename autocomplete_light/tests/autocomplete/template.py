from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.template import Template, Context

from .case import *
from ..apps.autocomplete_test_case_app.models import User, Group


class AutocompleteMock(autocomplete_light.AutocompleteModelTemplate):
    limit_choices = 2
    choices = User.objects.all()
    search_fields = ('username', 'email')

    choice_template = u'<li data-value="{{ choice.pk }}">{{ choice }}</li>'
    autocomplete_template = u''.join([
        u'{% load autocomplete_light_tags %}',
        u'<ul>',
        u'{% for choice in choices %}',
        u'{{ choice|autocomplete_light_choice_html:autocomplete }}',
        u'{% endfor %}',
        u'</ul>',
    ])

    def render_template_context(self, template, extra_context=None):
        context = self.get_base_context()
        context.update(extra_context or {})

        template = Template(template)
        return template.render(Context(context))


class AutocompleteModelTemplateTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteMock

    def setUp(self):
        User.objects.all().delete()
        self.abe = User(username='Abe', email='sales@example.com')
        self.jack = User(username='Jack', email='jack@example.com')
        self.james = User(username='James', email='sales@example.com')
        self.john = User(username='John', email='sales@example.com')

        self.abe.save()
        self.jack.save()
        self.james.save()
        self.john.save()

    def get_choices_for_values_tests(self):
        return []

    def get_choices_for_request_tests(self):
        return []

    def get_validate_tests(self):
        return []

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'expected': u''.join([
                    u'<ul>',
                    u'<li data-value="%s">%s</li>' % (
                        self.jack.pk, force_text(self.jack)),
                    u'<li data-value="%s">%s</li>' % (
                        self.james.pk, force_text(self.james)),
                    u'</ul>',
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': u''.join([
                    u'<ul>',
                    u'<li data-value="%s">%s</li>' % (
                        self.abe.pk, force_text(self.abe)),
                    u'<li data-value="%s">%s</li>' % (
                        self.jack.pk, force_text(self.jack)),
                    u'</ul>',
                ])
            },
        )

    def get_widget_tests(self):
        return []
