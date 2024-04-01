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
