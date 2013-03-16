# -*- coding: utf-8 -*-
from slt.theme.browser.viewlet import AddressViewlet
from slt.theme.tests.base import IntegrationTestCase

import mock


class AddressViewletTestCase(IntegrationTestCase):
    """TestCase for AddressViewlet"""

    def test_subclass(self):
        from slt.theme.browser.viewlet import BaseViewlet
        self.assertTrue(AddressViewlet, BaseViewlet)

    def test_context(self):
        from zope.interface import Interface
        self.assertEqual(getattr(AddressViewlet, 'grokcore.component.directive.context'), Interface)

    def test_name(self):
        self.assertEqual(getattr(AddressViewlet, 'grokcore.component.directive.name'), 'slt.theme.address')

    def test_template(self):
        self.assertEqual(getattr(AddressViewlet, 'grokcore.view.directive.template'), 'address')

    def test_viewletmanager(self):
        from slt.theme.browser.viewlet import AddressesViewletManager
        self.assertEqual(getattr(AddressViewlet, 'grokcore.viewlet.directive.viewletmanager'), AddressesViewletManager)

    def test_addresses(self):
        view = mock.Mock()
        instance = self.create_viewlet(AddressViewlet, view=view)
        view.addresses = []
        self.assertEqual(len(instance.addresses), 0)

        address1 = self.create_content('collective.cart.shopping.CustomerInfo', id='address1',
            first_name='FIRST1', last_name='LAST1', organization='ORGANIZATION1', city='CITY1', post='POST1',
            street='STREET1', email='EMAIL1', phone='PHONE1')

        view.addresses = [address1]
        self.assertEqual(len(instance.addresses), 1)
        self.assertEqual(instance.addresses, [{
            'city': 'CITY1 POST1',
            'edit_url': 'http://nohost/plone/address1/edit',
            'email': 'EMAIL1',
            'name': 'FIRST1 LAST1',
            'organization': 'ORGANIZATION1 FI',
            'phone': 'PHONE1',
            'street': 'STREET1'
        }])

    def test___name(self):
        instance = self.create_viewlet(AddressViewlet)
        item = mock.Mock()
        item.first_name = 'FIRST'
        item.last_name = 'LAST'
        self.assertEqual(instance._name(item), 'FIRST LAST')

    def test__organization(self):
        instance = self.create_viewlet(AddressViewlet)
        item = mock.Mock()
        item.organization = None
        item.vat = None
        self.assertIsNone(instance._organization(item))

        item.organization = 'ORGANIZATION'
        self.assertEqual(instance._organization(item), 'ORGANIZATION')

        item.vat = 'VAT'
        self.assertEqual(instance._organization(item), 'ORGANIZATION VAT')

    def test__city(self):
        instance = self.create_viewlet(AddressViewlet)
        item = mock.Mock()
        item.city = 'CITY'
        item.post = None
        self.assertEqual(instance._city(item), 'CITY')

        item.post = 'POST'
        self.assertEqual(instance._city(item), 'CITY POST')

    def test_class_collapsible(self):
        view = mock.Mock()
        instance = self.create_viewlet(AddressViewlet, view=view)
        view.addresses = []
        self.assertEqual(instance.class_collapsible, 'collapsible')

        view.addresses = [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]
        self.assertEqual(instance.class_collapsible, 'collapsible')

        view.addresses = [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]
        self.assertEqual(instance.class_collapsible, 'collapsible collapsedOnLoad')