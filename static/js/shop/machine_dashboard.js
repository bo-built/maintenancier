document.addEventListener('alpine:init', () => {
    Alpine.data('machineApp', () => ({
        log_loading: true,
        log_entries: [],
        machine: {},
        selectedTask: null,
        createTaskModal: null,
        editingTask: null,
        draft: {},
        archiveTargetTask: null,
        archiveMachineModal: null,

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

        setEditingTask(task) {
            this.editingTask = task;
            this.draft = { ...task };
        },

        unSetEditingTask(task) {
            this.editingTask = null;
            this.draft = null;
        },

        async editTask(formEl, task) {

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
                const response = await fetch(task.api_url, {
                    method: 'PATCH',
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

                Object.assign(task, data.task);
                this.editingTask = null;

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

        confirmArchiveTask(target) {
            this.archiveTargetTask = target;
            this.archiveTaskModal.show();
        },

        closeArchiveTaskModal() {
            this.archiveTargetTask = null;
            this.archiveTaskModal.hide();
        },

        async archiveTask() {
            try {
                payload = {
                    pk: this.archiveTargetTask.pk,
                    status: 'archived',
                }
                const response = await fetch(this.archiveTargetTask.api_url, {
                    method: 'PATCH',
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

                this.editingTask = null;
                Object.assign(this.archiveTargetTask, data.task);
                this.closeArchiveTaskModal();

            } catch (error) {
                console.error('Failed to archive maintenance item:', error);
            }
        },

        confirmArchiveMachine(target) {
            this.archiveMachineModal.show();
        },

        closeArchiveMachineModal() {
            this.archiveMachineModal.hide();
        },

        async archiveMachine() {
            try {
                payload = {
                    pk: this.machine.pk,
                    status: 'archived',
                }
                const response = await fetch(this.machine.api_url, {
                    method: 'PATCH',
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

                Object.assign(this.machine, data.machine);
            } catch (error) {
                console.error('Failed to archive maintenance item:', error);
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

        exportTableToPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            // Optional: Add a title above the table
            doc.text("Team Directory", 14, 15);

            // Convert the HTML table to a PDF table
            doc.autoTable({
                html: '#log_table',
                startY: 20, // Starts below the title
                theme: 'grid', // Options: 'striped', 'grid', 'plain'
                styles: { fontSize: 10 },
                headStyles: { fillColor: [41, 128, 185] } // Custom header color (RGB)
            });

            doc.save('maintenance-log-export.pdf');
        },

        async initDashoard(url) {

            this.createTaskModal = new bootstrap.Modal(this.$refs.createTaskModal);
            this.$refs.createTaskModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });

            this.archiveTaskModal = new bootstrap.Modal(this.$refs.archiveTaskModal);
            this.$refs.archiveTaskModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });

            this.archiveMachineModal = new bootstrap.Modal(this.$refs.archiveMachineModal);
            this.$refs.archiveMachineModal.addEventListener('hide.bs.modal', () => {
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