document.addEventListener('DOMContentLoaded', () => {
	
	// handle image previews
	document.addEventListener('change', (event) => {
		
		files = event.target.files;

		const preview = document.getElementById('image-preview');
		preview.innerHTML = '';

		Array.from(files).forEach((file) => {

			// check the type of file, makes sure it's an image
			if (file.type.startsWith('image/')) {

				const reader = new FileReader();

				reader.onload = event => {
					const img = document.createElement('img');
					img.src = event.target.result;

					const deleteButton = document.createElement('button');
					deleteButton.textContent = 'X';
					deleteButton.classList.add('remove-button');

					const item = document.createElement('div');
					item.classList.add('item');
					item.appendChild(img);
					item.appendChild(deleteButton);
					preview.appendChild(item);

					deleteButton.addEventListener('click', () => {
						preview.removeChild(item);
					});
				};

				reader.onerror = event => {
					console.error("Error: ", event.target.error);
				};

				reader.readAsDataURL(file);
			}
		});
	});

	// handle form submission
	document.getElementById('upload').addEventListener('submit', (event) => {
		
		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		let headers = {
			'X-CSRFToken': form.csrf_token.value
		};

		fetch('/upload', {
			headers: headers,
			method: 'POST',
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
				const errorElement = document.querySelector('.alert p');

				errorElement.textContent = data.error;
				errorElement.classList.add('alert-danger');

				setTimeout(() => {
					errorElement.textContent = '';
					errorElement.classList.remove('alert-danger');
				}, 3000);
			} else {

				const messageElement = document.querySelector('.alert p');

				messageElement.textContent = data.success;
				messageElement.classList.add('alert-success');


				setTimeout(() => {
					messageElement.classList.remove('alert-success');
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
