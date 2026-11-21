from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from appuser.views import ProtectedView
from shop.models import ShopUser
from shop.forms import (
    MaintenanceTaskForm,
    MaintenanceTaskEditForm,
    ShopForm,
    MachineForm,
    NotesForm,
)


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
            'machine_form': MachineForm(),
            'notes_form': NotesForm(),
        }
        return HttpResponse(template.render(context, request))


class MachineDashboard(ProtectedView):
    def get(self, request, *args, **kwargs):
        shop = ShopUser.objects.get(user=request.user, shop__pk=kwargs['shop_pk']).shop
        machine = get_object_or_404(shop.machine_set, pk=kwargs['machine_pk'])
        template = loader.get_template('shop/machine_dashboard.html')
        context = {
            'shop': shop,
            'schedule_item_form': MaintenanceTaskForm(machine=machine),
            'edit_form': MaintenanceTaskEditForm(),
            'machine': machine,
        }
        return HttpResponse(template.render(context, request))
