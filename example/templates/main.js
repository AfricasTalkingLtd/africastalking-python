"use strict";

$(function () {


    function log(message) {
        $("#response").text(message);
        $('pre span').each(function(i, block) {
            hljs.highlightBlock(block);
        });
    }

    $("#signUp").click(() => {
        let phone = $("#phone").val();
        if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
        }

        log("Sending SMS...");

        $.ajax({
            type: "POST",
            url: `/auth/register/${encodeURIComponent(phone)}`,
            success: (resp) => {
                try {
                    log(JSON.stringify(JSON.parse(resp), null, 2));
                } catch (ex) {
                    log(resp);
                }
            },
            error: (xhr, textStatus, errorThrown) => {
                log(errorThrown);
            }
        });

    });

    $("#airtime").click(() => {
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

        log("Sending Airtime...");

        $.ajax({
            type: "POST",
            url: `/airtime/${encodeURIComponent(phone)}?amount=${amount}`,
            success: (resp) => {
                try {
                    log(JSON.stringify(JSON.parse(resp), null, 2));
                } catch (ex) {
                    log(resp);
                }
            },
            error: (xhr, textStatus, errorThrown) => {
                log(errorThrown);
            }
        });

    });

    $("#mobileCheckout").click(() => {
        const phone = $("#phone").val();
        const amount = $("#mobileCheckoutAmount").val();
        if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
        }

        if (!amount) {
            log(JSON.stringify({ error: "Enter an amount (with currency) e,g, KES 334"}, null, 2));
            return;
        }

        log("Initiating Mobile Checkout...");

        $.ajax({
            type: "POST",
            url: `/mobile/checkout/${encodeURIComponent(phone)}?amount=${amount}`,
            success: (resp) => {
                try {
                    log(JSON.stringify(JSON.parse(resp), null, 2));
                } catch (ex) {
                    log(resp);
                }
            },
            error: (xhr, textStatus, errorThrown) => {
                log(errorThrown);
            }
        });

    });

    $("#mobileB2C").click(() => {
        const phone = $("#phone").val();
        const amount = $("#mobileB2CAmount").val();
        if (!phone) {
            log(JSON.stringify({ error: "Enter a phone number"}, null, 2));
            return;
        }

        if (!amount) {
            log(JSON.stringify({ error: "Enter an amount (with currency) e,g, KES 334"}, null, 2));
            return;
        }

        log("Initiating Mobile B2C...");

        $.ajax({
            type: "POST",
            url: `/mobile/b2c/${encodeURIComponent(phone)}?amount=${amount}`,
            success: (resp) => {
                try {
                    log(JSON.stringify(JSON.parse(resp), null, 2));
                } catch (ex) {
                    log(resp);
                }
            },
            error: (xhr, textStatus, errorThrown) => {
                log(errorThrown);
            }
        });

    });

});
