document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardApp', () => ({
        machines: [],
        machines_loading: true,
        schedule: {},
        shop: {},
        user: {},
        dismissTaskModal: null,
        dismissTargetGroup: [],
        dismissTargetTask: {'name': 'tmp'},
        createMachineModal: null,

        openMachineModal() {
            this.createMachineModal.show();
        },

        closeMachineModal() {
            this.createMachineModal.hide();
        },

        async submitNewMachine(formEl) {
            const formData = new FormData(formEl);
            const payload = Object.fromEntries(formData.entries());

            Object.keys(payload).forEach((key) => {
                if (payload[key] === '') {
                    payload[key] = null;
                }
            });

            formEl.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
                payload[cb.name] = cb.checked;
            });
            try {
                const response = await fetch(this.shop.machine_api_url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                if (!response.ok) {
                    console.error('Validation errors:', data);
                    return;
                }

                formEl.reset();
                const select = document.getElementById('id_machine');
                const option = new Option(data.machine.name, data.machine.pk, true, true);
                select.add(option);
                this.machines.push(data.machine);
                this.closeMachineModal();

            } catch (error) {
                console.error('Failed to create maintenance item:', error);
            }
        },

        confirmDismissTask(dismissTargetGroup, dismissTargetTask) {
            this.dismissTargetGroup = dismissTargetGroup;
            this.dismissTargetTask = dismissTargetTask;
            this.dismissTaskModal.show();
        },

        closeDismissTask() {
            this.dismissTargetGroup = [];
            this.dismissTargetTask = {'name': 'tmp'};
            this.dismissTaskModal.hide();
        },

        async dismissTask() {
            try {
                var payload = {
                    status: 'dismissed',
                }
                const response = await fetch(this.dismissTargetTask.api_url, {
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
                Object.assign(this.dismissTargetTask, updatedTask.log_item);
                this.dismissTargetGroup.items = this.dismissTargetGroup.items.filter(
                    item => item.pk !== this.dismissTargetTask.pk);
                this.closeDismissTask();
            } catch (error) {
                // 3. Roll back the UI if the server request fails
                task.status = previousStatus;
                console.error('Failed to update task status:', error);
            }
        },

        async fetchThisUser() {
            try {
                const response = await fetch(this.shop.shopuser_api_url);
                this.user = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('loading_machines').classList.add('hidden');
                document.getElementById('machines_loaded').classList.remove('hidden');
            }
        },

        async fetchMachines() {
            try {
                const response = await fetch(this.shop.machine_api_url);
                this.machines = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('loading_machines').classList.add('hidden');
                document.getElementById('machines_loaded').classList.remove('hidden');
            }
        },

        async fetchToDoSchedule() {
            try {
                const response = await fetch(this.shop.schedule_api_url);
                this.schedule = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('schedule_loading').classList.add('hidden');
                document.getElementById('schedule_loaded').classList.remove('hidden');
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

            this.dismissTaskModal = new bootstrap.Modal(this.$refs.dismissTaskModal);
            this.$refs.dismissTaskModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });


            this.createMachineModal = new bootstrap.Modal(this.$refs.createMachineModal);
            this.$refs.createMachineModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });


            try {
                const response = await fetch(shop_api_url);
                this.shop = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                this.fetchMachines();
                this.fetchToDoSchedule();
                this.fetchThisUser();
            }
        },

    }));
});