document.addEventListener('alpine:init', () => {
    Alpine.data('userDashboardApp', () => ({
        shops_loading: true,
        shops: {},
        user: {},
        createShopModal: null,
        shop_api_url: null,

        openShopModal() {
            this.createShopModal.show();
        },

        closeShopModal() {
            this.createShopModal.hide();
        },

        async submitNewShop(formEl) {
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
                const response = await fetch(this.shop_api_url, {
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
                this.shops.push(data.shop);
                this.closeShopModal();

            } catch (error) {
                console.error('Failed to create maintenance item:', error);
            }
        },

        async fetchShops() {
            try {
                const response = await fetch(this.shop_api_url);
                this.shops = await response.json();
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                document.getElementById('shops_loading').classList.add('hidden');
                document.getElementById('shops_loaded').classList.remove('hidden');
            }
        },

        async initDashoard(url) {
            this.shop_api_url = url
            this.createShopModal = new bootstrap.Modal(this.$refs.createShopModal);
            this.$refs.createShopModal.addEventListener('hide.bs.modal', () => {
                if (document.activeElement instanceof HTMLElement) {
                    document.activeElement.blur();
                }
            });

            this.fetchShops();
        },

    }));
});