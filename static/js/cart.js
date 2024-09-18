document.addEventListener('DOMContentLoaded', () => {

	const quantityFields = document.querySelectorAll('.quantity-input');

	quantityFields.forEach(field => {
		field.addEventListener('change', function(event) {
			const itemElement = event.target.closest('.item');
			const sneakerId = itemElement.getAttribute('data-sneakerId');

			const newQuantity = parseInt(event.target.value);

			if (newQuantity > 0) {
				updateCartQuantity(sneakerId, newQuantity, itemElement);
			}
		});
	});

	function updateCartQuantity(sneakerId, quantity, itemElement) {

		const csrfToken = document.querySelector('input[name="csrf_token"]').value;

		// Create a FormData object to send the data
		let formData = new FormData();
		formData.append('quantity', quantity);

		fetch(`/update_cart/${sneakerId}`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrfToken
			},
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
				// Update the subtotal for the item
				const subtotalElement = itemElement.querySelector('.price');
				subtotalElement.textContent = `ksh. ${data.subtotal}`;

				// Update the total price
				const formattedPrice = data.total_price.toFixed(2);
				const totalPriceElement = document.querySelector('.total .pricing h3 span');
				totalPriceElement.textContent = `ksh ${formattedPrice}`;
			} 
		})
		.catch(error => {
			console.error('Error:', error);
			alert('An error occurred while updating the cart');
		});
        }

});


document.addEventListener('DOMContentLoaded', () => {
	// attach event listeners to all delete buttons
	document.querySelectorAll('.remove').forEach(element => {
		element.addEventListener('click', (event) => {

			event.preventDefault();

			const confirmation = confirm('Are you sure you want to remove this item from cart?');

			if (confirmation) {
				const sneakerId = element.getAttribute('data-sneakerId');

				fetch(`/remove_from_cart/${sneakerId}`, {
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

						const item = event.target.closest('.item');
						item.remove();

						const formattedPrice = data.total_price.toFixed(2);
						const totalPriceElement = document.querySelector('.total .pricing h3 span');
						totalPriceElement.textContent = `ksh ${formattedPrice}`;
					}
				})
				.catch(error => {
					console.error('Error: ', error.message);
				});
			}
		});
	});
});
