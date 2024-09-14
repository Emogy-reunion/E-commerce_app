document.addEventListener('DOMContentLoaded', () => {

	// toggle passwords
	document.getElementById('show').addEventListener('click', () => {
		let show = document.querySelector('#show');
		let password = document.querySelector('#password');

		if (show.checked) {
			password.setAttribute('type', 'text');
		} else {
			password.setAttribute('type', 'password');
		}
	});

	// send data to the server
	document.getElementById('login').addEventListener('submit', (event) => {
		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		let headers = {
			'X-CSRFToken' : form.csrf_token.value
		}
		
		fetch('/login', {
			headers: headers,
			body: formData,
			method: 'POST'
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
				document.querySelectorAll('.error').forEach(error => {
					error.textContent = '';
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
				const errorContainer = document.querySelector('.alert');
				const errorElement = document.querySelector('.alert p');
				errorElement.textContent = '';

				errorElement.textContent = data.error;
				errorContainer.classList.add('alert-danger');

				setTimeout(() => {
					errorElement.textContent = '';
					errorContainer.classList.remove('alert-danger');
				}, 5000);
			} else if(data.verify) {
				const errorContainer = document.querySelector('.alert');
                                const errorElement = document.querySelector('.alert p');
                                errorElement.textContent = '';

				errorElement.textContent = data.unverified;
                                errorContainer.classList.add('alert-danger');

				setTimeout(() => {
					errorElement.textContent = '';
                                        errorContainer.classList.remove('alert-danger');
					window.location.href = '/resend_verification_email';
				}, 2500);
			} else {
				window.location.href = '/guest_dashboard';
			}
		})
		.catch(error => {
			console.error('Error:' + error.message);
		});
	});
});
