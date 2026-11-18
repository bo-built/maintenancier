document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardApp', () => ({
        machines: [],
        machines_loading: true,
        schedule: {},
        shop: {},
        user: {},

        async fetchThisUser(user_api_url) {
            try {
                const response = await fetch(user_api_url);
                this.user = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('loading_machines').classList.add('hidden');
                document.getElementById('machines_loaded').classList.remove('hidden');
            }
        },

        async fetchMachines(machine_api_url) {
            try {
                const response = await fetch(machine_api_url);
                this.machines = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('loading_machines').classList.add('hidden');
                document.getElementById('machines_loaded').classList.remove('hidden');
            }
        },

        async fetchToDoSchedule(schedule_api_url) {
            try {
                const response = await fetch(schedule_api_url);
                this.schedule = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('schedule_loading').classList.add('hidden');
                document.getElementById('schedule_loaded').classList.remove('hidden');
            }
        },

        async dismissTask(group, task) {
            dismiss = window.confirm('Dismiss "' + task.item_name +'"?');
            if(dismiss) {
                try {
                    var payload = {
                        status: 'dismissed',
                    }
                    const response = await fetch(task.api_url, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify(payload),
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error ${response.status}`);
                    }

                    // 2. Sync with the exact data returned by Django
                    const updatedTask = await response.json();
                    Object.assign(task, updatedTask.log_item);
                    group.items = group.items.filter(item => item.pk !== task.pk);
                } catch (error) {
                    // 3. Roll back the UI if the server request fails
                    task.status = previousStatus;
                    console.error('Failed to update task status:', error);
                }
            }
        },

        async updateTaskStatus(task, isChecked) {
            /*
                When a task status toggle switch is clicked, send a patch to the
                API that changes the tasks status. The front end should then know
                that the specific task object status has changed
            */
            const previousStatus = task.status;
            const newStatus = isChecked ? 'done' : 'pending';

            // 1. Optimistically update the UI immediately
            task.status = newStatus;
            try {
                var payload = {
                    status: newStatus,
                    done_by: this.user,
                }
                const response = await fetch(task.api_url, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }

                // 2. Sync with the exact data returned by Django
                const updatedTask = await response.json();
                Object.assign(task, updatedTask.log_item);
            } catch (error) {
                // 3. Roll back the UI if the server request fails
                task.status = previousStatus;
                console.error('Failed to update task status:', error);
            }
        },

        async initDashoard(shop_api_url) {
            try {
                const response = await fetch(shop_api_url);
                this.shop = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                this.fetchMachines(this.shop.machine_api_url);
                this.fetchToDoSchedule(this.shop.schedule_api_url);
                this.fetchThisUser(this.shop.shopuser_api_url);
            }
        },

    }));
});