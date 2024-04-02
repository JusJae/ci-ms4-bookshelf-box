/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements({
	fonts: [
		{
			cssSrc: "https://fonts.googleapis.com/css?family=Roboto",
		},
	],
});
var style = {
	// Style the card Element with the default style from old stripe docs not available in new docs
	base: {
		color: "#05668d",
		fontFamily: '"Roboto", sans-serif',
		fontSize: "16px",
		"::placeholder": {
			color: "#000",
		},
	},
	invalid: {
		color: "#dc3545",
		iconColor: "#dc3545",
	},
};
var card = elements.create("card", { style: style });
card.mount("#card-element");

// Handle realtime validation errors on the card Element
card.addEventListener("change", function (event) {
	var errorDiv = document.getElementById("card-errors"); // Get the error div
	if (event.error) {
		// If there is an error, show it in the card error div
		var html = `
 			<span class="icon" role="alert">
 				<i class="fas fa-times"></i>
 			</span>
 			<span>${event.error.message}</span> 
 		`;
		$(errorDiv).html(html); // Add the error message to the error div
	} else {
		errorDiv.textContent = ""; // Clear the error div if there are no errors
	}
});

// Handle form submit
var form = document.getElementById("payment-form"); // Get the payment form

form.addEventListener("submit", function (ev) {
	ev.preventDefault(); // Prevent the form from submitting
	card.update({ disabled: true });
	$("#submit-button").attr("disabled", true); // Disable the card element and submit button to prevent multiple submissions
	stripe.confirmCardPayment(clientSecret, {
			payment_method: {
				card: card, // Pass the card Element to confirmCardPayment
			},
		}) // If the card is valid, confirm the payment
		.then(function (result) {
			if (result.error) {
				// Show error to your customer (e.g., insufficient funds)
				var errorDiv = document.getElementById("card-errors");
				var html = `
                 <span class="icon" role="alert">
                 <i class="fas fa-times"></i>
                 </span>
                 <span>${result.error.message}</span>`;
				$(errorDiv).html(html);
				// Re-enable the card Element and submit button if therr is an error to allow the user to fix it
				card.update({ disabled: false });
				$("#submit-button").attr("disabled", false);
			} else {
				// The payment has been processed and will submit the form
				if (result.paymentIntent.status === "succeeded") {
					form.submit();
				}
			}
		});
});
