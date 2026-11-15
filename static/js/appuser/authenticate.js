document.addEventListener('alpine:init', () => {
    Alpine.data('authenticationApp', () => ({

        state: 'login',
        errors: [],
        successMessage: null,

        async handleRegistration() {
            const formData = new FormData(this.$el);
            const csrftoken = getCookie('csrftoken');
            this.errors = [];
            this.successMessage = null;

            try {
                const payload = Object.fromEntries(formData.entries());
                const nextUrl = getNextParam();
                if (payload.confirm_password == payload.password) {

                    const response = await fetch('/api/profile/', {
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
                        if(data.errors) {
                            this.errors = data.errors;
                        }
                        return;
                    } else {
                        this.successMessage = "Registration successful! You can log in now";
                        this.state = 'login';
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

        async handleLogin() {
            const formData = new FormData(this.$el);
            const csrftoken = getCookie('csrftoken');
            this.errors = [];
            this.successMessage = null;

            try {
                const payload = Object.fromEntries(formData.entries());
                const nextUrl = getNextParam();

                const response = await fetch('/api/authenticate-login/', {
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
                    return;
                } else {
                    if (nextUrl) {
                        window.location.href = nextUrl;
                    } else {
                        window.location.href = data.redirect_url;
                    }
                }
            } catch (error) {
                this.errors.push('An unknown error happened');
            }
        }
    }));
});