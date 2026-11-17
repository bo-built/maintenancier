document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardApp', () => ({
        machines: [],
        machines_loading: true,
        schedule: {},

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

        initDashoard(machine_api_url, schedule_api_url) {
            this.fetchMachines(machine_api_url);
            this.fetchToDoSchedule(schedule_api_url);
        },

    }));
});