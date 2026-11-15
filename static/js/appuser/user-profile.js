document.addEventListener('alpine:init', () => {
    Alpine.data('updateProfileApp', () => ({

        errors: [],
        success_message: false,
        state: 'view',
        endpoint: '/api/profile/',
        profile: [],
        display_profile: [],
        loading: true,

        async fetchProfile() {
            try {
                const response = await fetch(this.endpoint);
                this.profile = await response.json();
                this.display_profile = structuredClone(Alpine.raw(this.profile));
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                showLoadedData();
            }
        },

        async handleChangePassword() {
            const formData = new FormData(this.$el);
            const csrftoken = getCookie('csrftoken');
            this.errors = [];
            this.success_message = false;

            const password_endpoint = '/api/update-password/';

            try {
                const payload = Object.fromEntries(formData.entries());
                if (payload.new_password == payload.confirm_new_password) {

                    const response = await fetch(password_endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        console.error('Server error:', data.message);
                        this.errors.push(data.message);
                        if(data.errors){
                            this.errors = data.errors;
                        }
                        return;
                    } else {
                        this.success_message = 'Password updated! You might need to log in again to continue.';
                        this.state = 'view';
                    }
                } else {
                    this.errors.push('Password must match');
                    document.getElementById('id_new_password').classList.add('field-error');
                    document.getElementById('id_confirm_new_password').classList.add('field-error');
                }
            } catch (error) {
                this.errors.push('An unknown error happened');
            }
        },

        async handleUpdateProfile() {
            const formData = new FormData(this.$el);
            const csrftoken = getCookie('csrftoken');
            this.errors = [];
            this.success_message = false;

            try {
                const payload = Object.fromEntries(formData.entries());
                if (payload.confirm_password == payload.password) {

                    const response = await fetch(this.endpoint, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        console.error('Server error:', data.message);
                        this.errors.push(data.message);
                        return;
                    } else {
                        this.success_message = 'Profile data updated!';
                        this.profile = data.user;
                        this.display_profile = structuredClone(data.user);
                        this.state = 'view';
                    }
                } else {
                    this.errors.push('Password must match');
                    document.getElementById('id_password').classList.add('field-error');
                    document.getElementById('id_confirm_password').classList.add('field-error');
                }
            } catch (error) {
                this.errors.push('An unknown error happened');
            }
        },

    }));
});