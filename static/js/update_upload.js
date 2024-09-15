document.addEventListener('DOMContentLoaded', () => {

	// handle form submission
	document.getElementById('upload').addEventListener('submit', (event) => {
		
		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		let headers = {
			'X-CSRFToken': form.csrf_token.value
		};

		fetch('/update_upload', {
			headers: headers,
			method: 'PATCH',
			body: formData
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Error: ' + response.statusText);
			} else {
				return response.json();
			}
		})
		.then(data => {
			if (data.errors) {

				// retrieve and display form errors
				document.querySelectorAll('.error').forEach(element => {
					element.textContent = '';
				});

				for (let field in data.errors) {
					let errorMessage = data.errors[field].join(', ');
					let errorElement = document.querySelector(`#${field}-error`);

					errorElement.textContent = errorMessage;

					setTimeout(() => {
						errorElement.textContent = '';
					}, 3000);
				}

			} else if (data.error) {

				// retrieve any other errors that might occur
				const errorContainer = document.querySelector('.alert');
				const errorElement = document.querySelector('.alert p');

				errorElement.textContent = data.error;
				errorContainer.classList.add('alert-danger');

				setTimeout(() => {
					errorElement.textContent = '';
					errorContainer.classList.remove('alert-danger');
				}, 3000);
			} else {

				// handles successful uploads
				const messageContainer = document.querySelector('.alert')
				const messageElement = document.querySelector('.alert p');

				messageElement.textContent = data.success;
				messageContainer.classList.add('alert-success');


				setTimeout(() => {
					messageContainer.classList.remove('alert-success');
					window.location.href = '/uploads';
				}, 2000);
			}
		})
		.catch(error => {
			console.error('Error: ' + error.message);
			alert('An unexpected error occured. Please try again!');
		});
	});
});
