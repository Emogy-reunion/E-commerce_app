document.addEventListener('DOMContentLoaded', () => {

	document.getElementById('add').addEventListener('submit', (event) => {
		event.preventDefault();

		const sizeForm = document.getElementById('add');
		const sneakerId = sizeForm.getAttribute('data-sneakerID');

		const form = event.target;
		const formData = new FormData(form);

		let headers = {
			'X-CSRFToken': form.csrf_token.value // extract the token
		};

		fetch(`/add_to_cart/${sneakerId}`, {
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
			if (data.error) {
				alert(data.error);
			} else {
				alert(data.success);
				window.location.href ='/view_cart';
			}
		})
		.catch(error => {
			console.error('Error: ', error.message);
		});
	});
});
