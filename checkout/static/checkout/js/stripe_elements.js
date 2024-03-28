var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripe_public_key); // Use the variable from your script tag
var elements = stripe.elements();
var style = {
	base: {
		color: "#32325d",
		fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
		fontSmoothing: "antialiased",
		fontSize: "16px",
		"::placeholder": {
			color: "#aab7c4",
		},
	},
	invalid: {
		color: "#fa755a",
		iconColor: "#fa755a",
	},
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.addEventListener("change", function (event) {
	var errorDiv = document.getElementById("card-errors");
	if (event.error) {
		// If there is an error, show it in the card error div
		var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
		$(errorDiv).html(html);
	} else {
		errorDiv.textContent = "";
	}
});

	// card.on("change", ({ error }) => {
	// 	var displayError = document.getElementById("card-error");
	// 	if (error) {
	// 		displayError.textContent = error.message;
	// 	} else {
	// 		displayError.textContent = "";
	// 	}
	// });

