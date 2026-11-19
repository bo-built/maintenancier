from django.http import HttpResponse
from django.template import loader
from appuser.views import ProtectedView
from shop.models import ShopUser
from shop.forms import MaintenanceScheduleItemForm, ShopForm, MachineForm


class Dashboard(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('shop/user_dashboard.html')
        context = {
            'new_shop_form': ShopForm()
        }
        return HttpResponse(template.render(context, request))


class ShopDashboard(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('shop/shop_dashboard.html')
        shop = ShopUser.objects.get(user=request.user, shop__pk=kwargs['shop_pk']).shop
        context = {
            'appuser': request.user.appuser,
            'shop': shop,
            'schedule_item_form': MaintenanceScheduleItemForm(shop=shop),
            'machine_form': MachineForm(),
        }
        return HttpResponse(template.render(context, request))
