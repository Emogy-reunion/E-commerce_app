document.addEventListener('DOMContentLoaded', () => {

	document.getElementById('update').addEventListener('submit', (event) => {

		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		element = document.getElementById('update');
		orderId = element.getAttribute('data-orderId');

		headers = {
			'X-CSRFToken': form.csrf_token.value
		}

		fetch(`/update_order_status/${orderId}`, {
			headers,
			method: 'POST',
			body: formData
		})
		.then(response => {
			if (!response.ok) {
				throw new Error(response.statusText);
			} else {
				return response.json();
			}
		})
		.then(data => {
			if (data.errors) {
				document.querySelectorAll('.error').forEach(element => {
					element.textContent = '';
				});

				for (let field in data.errors) {
					let errorMessage = data.errors[field].join(', ');
					let errorElement = document.querySelector(`#${field}-error`);

					errorElement.textContent = errorMessage;

					setTimeout(() => {
						errorElement.textContent = '';
					}, 5000);
				}
			} else if (data.error) {
				alert(data.error);
			} else {
				alert(data.success);
				window.location.href = '/admin_orders_view';
			}
		})
		.catch(error => {
			console.error('Error: ', error.message);
		});
	});
});
