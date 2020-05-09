// A reference to Stripe.js initialized with a fake API key.
//Sign in to see examples pre-filled with your key.
var stripe = Stripe("pk_test_oB6wyC75CL7Ebw5ohzYPzY1h0028iIzITV");
var elements = stripe.elements();

// Set up Stripe.js and Elements to use in checkout form
var style = {
    base: {
      color: "#32325d",
    }
  };
  
  var card = elements.create("card", { style: style });
  card.mount("#card-element");


  card.addEventListener('change', ({error}) => {
    const displayError = document.getElementById('card-errors');
    if (error) {
      displayError.textContent = error.message;
    } else {
      displayError.textContent = '';
    }
  });


  var form = document.getElementById('payment-form');
  let btn = document.getElementById('submit');
  let clientSecret = btn.dataset.secret;
  let clientName = btn.dataset.user;

  form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
      // Stripe will send an email receipt when the payment succeeds in live mode (but will not send one in test mode).
      receipt_email: document.getElementById('email').value,
      payment_method: {
        card: card,
        billing_details: {
          name: clientName
        }
      }
    }).then(function(result) {
      if (result.error) {
        // Show error to your customer (e.g., insufficient funds)
        console.log(result.error.message);
        var errorMsg = document.querySelector("#card-errors");
        errorMsg.textContent = result.error.message;
      } else {
        // The payment has been processed!
        if (result.paymentIntent.status === 'succeeded') {
          // Show a success message to your customer
          // There's a risk of the customer closing the window before callback
          // execution. Set up a webhook or plugin to listen for the
          // payment_intent.succeeded event that handles any business critical
          // post-payment actions.
          document.querySelector(".result-message").classList.remove("hidden");
          document.querySelector("button").disabled = true;
        }
      }
    });
  });

// Shows a success message when the payment is complete
// var orderComplete = function(paymentIntentId) {
//     loading(false);
//     document
//       .querySelector(".result-message a")
//       .setAttribute(
//         "href",
//         "https://dashboard.stripe.com/test/payments/" + paymentIntentId
//       );
//     document.querySelector(".result-message").classList.remove("hidden");
//     document.querySelector("button").disabled = true;
//   };
//   // Show the customer the error from Stripe if their card fails to charge
//   var showError = function(errorMsgText) {
//     loading(false);
//     var errorMsg = document.querySelector("#card-errors");
//     errorMsg.textContent = errorMsgText;
//     setTimeout(function() {
//       errorMsg.textContent = "";
//     }, 4000);
//   };
//   // Show a spinner on payment submission
//   var loading = function(isLoading) {
//     if (isLoading) {
//       // Disable the button and show a spinner
//       document.querySelector("button").disabled = true;
//       document.querySelector("#spinner").classList.remove("hidden");
//       document.querySelector("#button-text").classList.add("hidden");
//     } else {
//       document.querySelector("button").disabled = false;
//       document.querySelector("#spinner").classList.add("hidden");
//       document.querySelector("#button-text").classList.remove("hidden");
//     }
//   };