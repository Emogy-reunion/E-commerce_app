document.addEventListener('DOMContentLoaded', () => {

	document.getElementById('filter').addEventListener('submit', (event) => {

		event.preventDefault();

		const form = event.target;
		const formData = new FormData(form);

		// convert it to query parameters
		let queryParams = new URLSearchParams(formData).toString();

		const url = `/guest_search?${queryParams}`;

		const headers = {
			'X-CSRFToken': form.csrf_token.value
		};

		const container = document.getElementById('display');
		container.innerHTML = ''; // clear any existing items

		
		// send a get request to retrieve data
		fetch(url, {
			headers,
			method: 'GET'
		})
		.then(response => {
			if (!response.ok) {
				throw new Error(response.statusText);
			} else {
				return response.json();
			}
		})
		.then(data => {
			if (data.message) {
				alert(data.message);
			} else {
				data.forEach(sneaker => {
					const item = document.createElement('div'); // element div
					item.setAttribute('data-sneakerId', sneaker.id);

					const link = document.createElement('a'); // link to property details
					link.href = `/guest_product_details/${sneaker.id}`;

					const imageDiv = document.createElement('div'); // contains sneaker image
					const image = document.createElement('img');
					image.src = `/send_image/${sneaker.filename}`;
					image.alt = sneaker.filename;
					imageDiv.appendChild(image);
					imageDiv.classList.add('image');

					link.appendChild(imageDiv);

					const details = document.createElement('div'); // holds the sneaker price and name
					details.classList.add('details')

					const name = document.createElement('h3');
					name.textContent = sneaker.name;

					const price = document.createElement('h5');
					price.textContent = sneaker.price;

					details.appendChild(name);
					details.appendChild(price);

					item.appendChild(link);
					item.appendChild(details);
					item.classList.add('item');
					
					container.appendChild(item);
				});
			}
		})
		.catch(error => {
			console.error('Error: ', error.message);
		});
	});
});
