document.addEventListener('DOMContentLoaded', function() {

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
			if (data.success) {
				// Update the subtotal for the item
				const subtotalElement = itemElement.querySelector('.price');
				subtotalElement.textContent = `ksh. ${data.new_subtotal}`;

				// Update the total price
				const totalPriceElement = document.querySelector('.total .pricing h3 span');
				totalPriceElement.textContent = `ksh. ${data.total_price}`;
			} else {
				alert('Error updating cart. Please try again.');
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});
        }
});
