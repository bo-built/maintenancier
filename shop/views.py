from django.http import HttpResponse
from django.template import loader
from appuser.views import ProtectedView
from shop.models import ShopUser


class Dashboard(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('shop/dashboard.html')
        shops = ShopUser.get_user_shops(request.user)
        context = {
            'appuser': request.user.appuser,
            'shops': shops,
        }
        return HttpResponse(template.render(context, request))


class ShopDashboard(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('shop/dashboard.html')
        shop = ShopUser.objects.get(user=request.user, shop__pk=kwargs['shop_pk']).shop
        context = {
            'appuser': request.user.appuser,
            'shop': shop,
        }
        return HttpResponse(template.render(context, request))
