document.addEventListener('DOMContentLoaded', () => {

	// add event listeners to all delete buttons
	document.querySelectorAll('.delete').forEach(element => {
		element.addEventListener('click', (event) => {
			event.preventDefault();

			const confirmation = confirm('Are you sure you want to delete this item?');

			if (confirmation) {

				const sneakerId = element.getAttribute('data-sneakerId');

				fetch(`/delete_post/${sneakerId}`, {
					method: 'DELETE'
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
						const sneakerItem = document.querySelector(`div[data-sneakerId='${sneakerId}']`);
						sneakerItem.remove();
						alert(data.success);
					}
				})
				.catch(error => {
					console.error('Error: ', error.message)
				});
			}
		});
	});
});
				
