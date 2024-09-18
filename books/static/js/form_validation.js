document.addEventListener("DOMContentLoaded", function () {
	const forms = document.querySelectorAll(".needs-validation");

	forms.forEach(function (form) {
		form.addEventListener(
			"submit",
			function (event) {
				const priceField = document.getElementById("#id_price");
				const availabilityField = document.getElementById("#id_availability");
				let valid = true;

				if (priceField && priceField.value < 0) {
					priceField.setCustomValidity("Price must be greater than 0.");
					valid = false;
				} else if (priceField) {
					priceField.setCustomValidity("");
				}

				if (availabilityField && parseInt(availabilityField.value) < 0) {
					availabilityField.setCustomValidity("Availability must be greater than 0.");
					valid = false;
				} else if (availabilityField) {
					availabilityField.setCustomValidity("");
				}

				if (!form.checkValidity() || !valid) {
					event.preventDefault();
					event.stopPropagation();
				}
				form.classList.add("was-validated");
			},
			false
		);
	});
});
