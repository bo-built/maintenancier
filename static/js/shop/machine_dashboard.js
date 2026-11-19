document.addEventListener('alpine:init', () => {
    Alpine.data('machineApp', () => ({
        log_loading: true,
        log_entries: [],
        machine: {},
        selectedTask: null,
        createTaskModal: null,

        openTaskModal() {
            this.createTaskModal.show();
        },

        closeTaskModal() {
            this.createTaskModal.hide();
        },

        async submitNewTask(formEl) {
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
                const response = await fetch(this.machine.shop_schedule_api_url, {
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
                this.machine.maintenance_items.push(data.item)
                this.closeTaskModal();

            } catch (error) {
                console.error('Failed to create maintenance item:', error);
            }
        },

        setSelectedTask(target) {
            if (this.selectedTask == target) {
                this.selectedTask = false;
            } else {
                this.selectedTask = target;
            }
        },

        async fetchLog() {
            try {
                const response = await fetch(this.machine.maintenance_history_api);
                this.log_entries = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('log_loading').classList.add('hidden');
                document.getElementById('log_loaded').classList.remove('hidden');
            }
        },

        async initDashoard(url) {

            this.createTaskModal = new bootstrap.Modal(this.$refs.createTaskModal);
            this.$refs.createTaskModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });

            this.machine_detail_api = url;

            try {
                const response = await fetch(this.machine_detail_api);
                this.machine = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                this.fetchLog();
            }
        },

    }));
});