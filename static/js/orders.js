document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('.toggle-table').forEach(button => {

		// Add the event listener for toggling
		button.addEventListener('click', () => {
            		const itemsRow = button.closest('tr').nextElementSibling;
            	
			// Toggle the display of the itemsRow
            		if (itemsRow.style.display === '' || itemsRow.style.display === 'none') {
                		itemsRow.style.display = 'table-row'; // Show items
                		button.textContent = 'Hide Items'; // Change button text
            		} else {
                		itemsRow.style.display = 'none'; // Hide items
                		button.textContent = 'Show Items'; // Change button text
            		}
        	});
    	});
});
