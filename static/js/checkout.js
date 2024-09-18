document.addEventListener('DOMContentLoaded', () => {

	document.querySelector('.submit').addEventListener('click', () => {

		const priceElement = document.querySelector('.pricing span');
		const amountText = priceElement.textContent;

		const amount = parseFloat(amountText.replace('ksh ', '').trim());
		
		const params = new URLSearchParams();
		params.append('total_amount', amount);

		fetch(`/place_order?${params.toString()}`, {
			method: 'GET'
		})
		.then(response => {
			if (!response.ok) {
				throw new Error(response.statusText);
			} else {
				return response.json();
			}
		})
		.catch(error => {
			console.error('Error: ', error.message);
		});

	});
});
