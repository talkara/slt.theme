from Products.CMFCore.utils import _checkPermission
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart.shopping.interfaces import IArticleAdapter
from collective.cart.shopping.interfaces import IShoppingSite
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from slt.theme.browser.interfaces import ISltThemeLayer
from slt.theme.interfaces import ICollapsedOnLoad
from slt.theme.interfaces import IFeedToShopTop
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface


grok.templatedir('viewlets')


class DocumentBylineViewlet(BaseDocumentBylineViewlet):
    """Document byline shown only for Site Admin and Manager."""

    def show(self):
        if _checkPermission('slt.theme: Show byline', self.context):
            return True


class BaseViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Base class for all the viewlet manager"""
    grok.baseclass()
    grok.layer(ISltThemeLayer)


class BaseViewlet(grok.Viewlet):
    """Base class for all the viewlet"""
    grok.baseclass()
    grok.layer(ISltThemeLayer)
    grok.require('zope2.View')


class ShopTopViewletManager(BaseViewletManager):
    """Viewlet manager for shop top page."""
    grok.context(IPloneSiteRoot)
    grok.name('slt.theme.shop.top.viewletmanager')


class ShopTopArticlesViewlet(BaseViewlet):
    """Viewlet to show articles."""
    grok.context(IPloneSiteRoot)
    grok.name('slt.theme.shop.top.articles')
    grok.template('shop-top-articles')
    grok.view(IViewView)
    grok.viewletmanager(ShopTopViewletManager)

    @property
    def articles(self):
        query = {
            'sort_on': 'feed_order',
            'sort_order': 'descending',
        }
        limit = getUtility(IRegistry)['slt.theme.articles_feed_on_top_page']
        if limit:
            query['sort_limit'] = limit
        res = []
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        for item in IShoppingSite(self.context).get_content_listing(IFeedToShopTop, **query):
            style_class = 'normal'
            if IArticleAdapter(item.getObject()).discount_available:
                style_class = 'discount'
            res.append({
                'description': item.Description(),
                'class': style_class,
                'feed_order': context_state.is_editable() and item.feed_order,
                'title': item.Title(),
                'url': item.getURL(),
            })
        return res


class AddressesViewletManager(BaseViewletManager):
    """Viewlet manager for listing addresses."""
    grok.context(Interface)
    grok.name('slt.theme.addresses.viewletmanager')


class AddressViewlet(BaseViewlet):
    """Viewlet to show address."""
    grok.context(Interface)
    grok.name('slt.theme.address')
    grok.template('address')
    grok.viewletmanager(AddressesViewletManager)

    @property
    def addresses(self):
        result = []
        for item in IContentListing(self.view.addresses):
            res = {
                'name': self._name(item),
                'organization': self._organization(item),
                'street': item.street,
                'city': self._city(item),
                'email': item.email,
                'phone': item.phone,
                'edit_url': '{}/edit'.format(item.getURL()),
            }
            result.append(res)
        return result

    def _name(self, item):
        return '{} {}'.format(item.first_name, item.last_name).strip()

    def _organization(self, item):
        org = item.organization
        if org:
            if item.vat:
                org = '{} {}'.format(item.organization, item.vat)
            return org.strip()

    def _city(self, item):
        city = item.city
        if item.post:
            city = '{} {}'.format(city, item.post)
        return city.strip()

    @property
    def class_collapsible(self):
        return getUtility(ICollapsedOnLoad)(len(self.view.addresses) > 4)


# class CheckOutViewlet(BaseCheckOutViewlet):
#     """Viewlet to display check out buttons."""
#     grok.layer(ISltThemeLayer)

    # def update(self):
    #     form = self.request.form
    #     if form.get('form.checkout') is not None:
    #         cart = IShoppingSite(self.context).cart
    #         # Update addresses.
    #         ICartAdapter(cart).add_address('billing')
    #     super(CheckOutViewlet, self).update()
