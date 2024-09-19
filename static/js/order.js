document.addEventListener('DOMContentLoaded', () => {

	document.getElementById('address').addEventListener('submit', (event) => {

		event.preventDefault();

		const totalText = document.getElementById('total').textContent;
		const totalValue = totalText.replace('ksh', '').trim();
		console.log(totalValue);


		const form = event.target;
		const formData = new FormData(form);
		formData.append('total_value', totalValue);

		let headers = {
			'X-CSRFToken': form.csrf_token.value
		}

		fetch('/place_order', {
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
			}
		})
		.catch(error => {
			console.error('Error: ', error.message);
		});
	});
});

