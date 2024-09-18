document.addEventListener('DOMContentLoaded', () => {

	document.querySelector('.submit').addEventListener('click', () => {

		const priceElement = document.querySelector('.pricing span');
		const amountText = priceElement.textContent;

		const amount = parseFloat(amountText.replace('ksh ', '').trim());
		
		const params = new URLSearchParams();
		params.append('total_amount', amount);

		window.location.href = `/place_order?${params.toString()}`;

	});
});
