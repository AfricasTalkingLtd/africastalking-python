function log(message) {
        $("#response").text(message);
        $('pre span').each(function(i, block) {
            hljs.highlightBlock(block);
        });
    }

$( "#sms" ).click(function() {
    let phone = $("#phone").val();
    if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
    }

    log("Sending SMS...");

    $.ajax({
        method: "POST",
        url: "/sms",
        data: { number: phone }
    })
        .done(function( msg ) {
            log(JSON.stringify(msg));
        })
        .fail(function( jqXHR, textStatus ) {
            log(textStatus);
        });
    
});
$( "#airtime" ).click(function() {
    const phone = $("#phone").val();
    const amount = $("#amount").val();
    if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
    }

    if (!amount) {
        log(JSON.stringify({ error: "Enter an amount (with currency) e,g, KES 334"}, null, 2));
        return;
    }

    log("Sending airtime.....");


    $.ajax({
        method: "POST",
        url: "/airtime",
        data: { 
            number: phone, 
            amount: amount
        }
    })
        .done(function( msg ) {
            log(JSON.stringify(msg));
        })
        .fail(function( jqXHR, textStatus ) {
            log(textStatus);
        });
    
});

$( "#mobileCheckout" ).click(function() {
    const phone = $("#phone").val();
    const amount = $("#amount").val();
    const productName = $("#product_name").val();

    if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
    }

    if (!amount) {
        log(JSON.stringify({ error: "Enter an amount (with currency) e,g, KES 334"}, null, 2));
        return;
    }
    if (!productName) {
        log(JSON.stringify({ error: "Enter the name of the product registered with AT, eg. Braids"}, null, 2));
        return;
    }

    log("Sending...");
    
    $.ajax({
        method: "POST",
        url: "/mobile_checkout",
        data: { 
            number: phone, 
            amount: amount, 
            product_name: productName
        }
    })
        .done(function( msg ) {
            log(JSON.stringify(msg));
        })
        .fail(function( jqXHR, textStatus ) {
            log(textStatus);
        });
    
});

$( "#mobileB2C" ).click(function() {
    const phone = $("#phone").val();
    const amount = $("#amount").val();
    const productName = $("#product_name").val();
    const name = $("#name").val();
    if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
    }

    if (!amount) {
        log(JSON.stringify({ error: "Enter an amount (with currency) e,g, KES 334"}, null, 2));
        return;
    }
    if (!productName) {
        log(JSON.stringify({ error: "Enter the name of the product registered with AT, eg. Braids"}, null, 2));
        return;
    }
    if (!name) {
        log(JSON.stringify({ error: "Enter the name of the recipient"}, null, 2));
        return;
    }

    log("Sending money...");

    $.ajax({
        method: "POST",
        url: "/mobile_b2c",
        data: { 
            number: phone, 
            amount: amount, 
            product_name: productName, 
            name: name
        }
    })
        .done(function( msg ) {
            log(JSON.stringify(msg));
        })
        .fail(function( jqXHR, textStatus ) {
            log(textStatus);
        });
    
});


