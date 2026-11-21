from django.urls import reverse
from shop.models import Machine
from shop.utils.test_utils import PopulatedTestBase
from django.utils import timezone


class ShopTestCaseWithData(PopulatedTestBase):
    def setUp(self):
        super().setUp()
        self.async_client.force_login(self.user)


class ShopApiViewTest(ShopTestCaseWithData):

    async def test_successful_shop_post(self):
        ''' Verify new shop instance is created from successful post call
        '''
        url = reverse('shopapi:shop_api')

        payload = {
            'name': 'Sturgis & Sons',
        }

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Shop created')

    async def test_successful_shop_get(self):
        url = reverse('shopapi:shop_api')
        response = await self.async_client.get(
            url,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    async def test_successful_shop_patch(self):
        url = reverse('shopapi:shop_detail_api', kwargs={'shop_pk': self.shop.pk})
        new_name = 'Cloud 9 Ozark Highlands Distribution Center'
        response = await self.async_client.patch(
            url,
            data={'name': new_name},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

    async def test_successful_shop_delete(self):
        ''' Verify method not implemented '''
        url = reverse('shopapi:shop_detail_api', kwargs={'shop_pk': self.shop.pk})
        response = await self.async_client.delete(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )


class MachineApiTest(ShopTestCaseWithData):

    async def test_successful_machine_fetch(self):
        machine_names = [m.name for m in self.machines]
        url = reverse('shopapi:machine_api', kwargs={'shop_pk': self.shop.pk})
        response = await self.async_client.get(
            url,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        response_machines = [r['name'] for r in response.data]

        self.assertEqual(
            response_machines.sort(),
            machine_names.sort()
        )

    async def test_successful_machine_patch(self):
        update_machine = self.machines[0]

        new_name = 'Shop Bot 2.0'

        url = reverse(
            'shopapi:machine_detail_api',
            kwargs={
                    'shop_pk': self.shop.pk,
                    'machine_pk': update_machine.pk
                }
            )

        payload = {'name': new_name}

        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )

        await update_machine.arefresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_machine.name, new_name)

    async def test_successful_machine_post(self):
        new_name = 'Shop Bot 2.0'
        url = reverse(
            'shopapi:machine_api',
            kwargs={'shop_pk': self.shop.pk, }
            )

        payload = {'name': new_name}

        response = await self.async_client.post(
            url,
            data=payload,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        machine_exists = await Machine.objects.aget(pk=response.data['machine']['pk'])
        self.assertTrue(machine_exists)
        self.assertEqual(machine_exists.name, new_name)

    async def test_successful_machine_delete(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:machine_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'machine_pk': self.machines[0].pk
            }
        )
        response = await self.async_client.delete(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )


class MaintenanceScheduleApiTest(ShopTestCaseWithData):

    async def test_successful_maintenance_schedule_fetch(self):
        pass

    async def test_successful_maintenance_schedule_post(self):
        ''' Verify successful post to maintenance schedule creates a new item '''

        post_data = {
            'machine': self.machines[1].pk,
            'interval': 7,
            'description': 'this is a description',
            'name': 'item name',
            'start_date': timezone.localdate(),
        }

        url = reverse(
            'shopapi:maintenance_schedule_api',
            kwargs={
                'shop_pk': self.shop.pk,
            }
        )
        response = await self.async_client.post(
            url,
            data=post_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    async def test_successful_maintenance_schedule_patch(self):
        ''' Verify method not implemented '''
        test_item = self.maintenance_items[0]
        url = reverse(
            'shopapi:maintenance_schedule_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': test_item.pk,
            }
        )
        change_data = {
            'name': 'new name',
            'interval': 7
        }
        response = await self.async_client.patch(
            url,
            data=change_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        await test_item.arefresh_from_db()
        self.assertEqual(test_item.name, change_data['name'])
        self.assertEqual(test_item.interval, change_data['interval'])

    async def test_successful_maintenance_schedule_delete(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:maintenance_schedule_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.maintenance_items[0].pk,
            }
        )
        response = await self.async_client.delete(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )


class MaintenanceLogApiTest(ShopTestCaseWithData):

    async def test_successful_maintenance_log_fetch(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:log_item_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.maintenance_items[0].pk,
            }
        )
        response = await self.async_client.get(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )

    async def test_successful_maintenance_log_post(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:log_item_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.maintenance_items[0].pk,
            }
        )
        response = await self.async_client.post(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )

    async def test_successful_maintenance_log_patch(self):
        ''' Verify method not implemented '''
        log_entry = await self.maintenance_items[0].log_entries.afirst()
        url = reverse(
            'shopapi:log_item_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.maintenance_items[0].pk,
                'log_entry_pk': log_entry.pk,
            }
        )
        payload = {'status': 'done'}
        response = await self.async_client.patch(
            url,
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        await log_entry.arefresh_from_db()
        self.assertEqual(
            log_entry.status,
            'done'
        )
        # TODO self.assertEqual(log_entry.done_by, self.user)

    async def test_successful_maintenance_log_delete(self):
        ''' Verify method not implemented '''
        log_entry = await self.maintenance_items[0].log_entries.afirst()
        url = reverse(
            'shopapi:log_item_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'task_pk': self.maintenance_items[0].pk,
                'log_entry_pk': log_entry.pk,
            }
        )
        response = await self.async_client.delete(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )


class ShopUserApiTest(ShopTestCaseWithData):

    async def test_successful_current_shop_user_fetch(self):
        expected_response = {
            'pk': self.shop_user.pk,
            'name': self.shop_user.name
        }
        url = reverse(
            'shopapi:shop_user_api',
            kwargs={
                'shop_pk': self.shop.pk,
            }
        )
        response = await self.async_client.get(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        for key, val in expected_response.items():
            self.assertEqual(response.data[key], val)

    async def test_successful_all_shop_user_fetch(self):
        url = reverse(
            'shopapi:shop_user_list_api',
            kwargs={
                'shop_pk': self.shop.pk,
            }
        )
        response = await self.async_client.get(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.addtl_shop_users) + 1)

    async def test_successful_shop_user_post(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:shop_user_api',
            kwargs={
                'shop_pk': self.shop.pk,
            }
        )
        response = await self.async_client.post(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )

    async def test_successful_shop_user_patch(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:shop_user_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'shop_user_pk': self.addtl_shop_users[0].pk,
            }
        )
        response = await self.async_client.patch(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )

    async def test_successful_shop_user_delete(self):
        ''' Verify method not implemented '''
        url = reverse(
            'shopapi:shop_user_detail_api',
            kwargs={
                'shop_pk': self.shop.pk,
                'shop_user_pk': self.addtl_shop_users[0].pk,
            }
        )
        response = await self.async_client.delete(
            url,
            data={},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.data['message'],
            'This method is not implemented yet'
        )
