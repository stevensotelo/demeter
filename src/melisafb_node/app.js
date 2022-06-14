/**
 * Copyright 2021-present, Facebook, Inc. All rights reserved.
 *
 * This source code is licensed under the license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * Messenger Platform Quick Start Tutorial
 *
 * This is the completed code for the Messenger Platform quick start tutorial
 *
 * https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start/
 *
 * To run this code, you must do the following:
 *
 * 1. Deploy this code to a server running Node.js
 * 2. Run `yarn install`
 * 3. Add your conf.VERIFY_TOKEN and conf.PAGE_ACCESS_TOKEN to your environment vars
 */

'use strict';

// Use dotenv to read .env vars into Node
require('dotenv').config();

// Imports dependencies and set up http server
const
    request = require('request'),
    express = require('express'),
    axios = require('axios'),
    { urlencoded, json } = require('body-parser'),
    fs = require('fs');

const app = express(),
    conf = JSON.parse(fs.readFileSync('conf.json'));


// Parse application/x-www-form-urlencoded
app.use(urlencoded({ extended: true }));

// Parse application/json
app.use(json());

function log_request(req) {
    let ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    let datetime = new Date();
    let requestMethod = req.method;
    var fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
    console.log(ip + " | " + datetime.toISOString() + " | " + requestMethod + " | " + fullUrl);
}

// Respond with 'Hello World' when a GET request is made to the homepage
app.get('/', function (_req, res) {
    res.send('<h1>Running MelisaBot for Meta</h1>');
});

// Adds support for GET requests to our webhook
app.get('/webhook', (req, res) => {
    log_request(req);

    // Parse the query params
    let mode = req.query['hub.mode'];
    let token = req.query['hub.verify_token'];
    let challenge = req.query['hub.challenge'];

    console.log('WEBHOOK | CHECK |' + mode + " | " + token + " | " + challenge);

    // Checks if a token and mode is in the query string of the request
    if (mode && token) {

        // Checks the mode and token sent is correct
        if (mode === 'subscribe' && token === conf.VERIFY_TOKEN) {

            // Responds with the challenge token from the request
            console.log('WEBHOOK_VERIFIED');
            res.status(200).send(challenge);

        } else {
            // Responds with '403 Forbidden' if verify tokens do not match
            res.sendStatus(403);
        }
    }
});

// Creates the endpoint for your webhook
app.post('/webhook', (req, res) => {
    log_request(req);
    let body = req.body;
    console.log('WEBHOOK | MESSAGE | ' + JSON.stringify(body));
    // Iterates over each entry - there may be multiple if batched

    body.entry.forEach(function (entry) {
        var senderPsid = "",
            message = "",
            user_tags = {},
            message_tags = {};
        // Checks if this is an event from a page subscription
        if (body.object === 'page') {
            user_tags = { service: "facebook" };
            // Gets the body of the webhook event
            let webhookEvent = entry.messaging[0];
            // Get the id sender
            senderPsid = webhookEvent.sender.id;
            // Check if the event is a message or postback and
            // pass the event to the appropriate handler function
            if (webhookEvent.message && webhookEvent.message.text) {
                message = webhookEvent.message.text;
            }
        }
        else if (body.object === 'whatsapp_business_account') {
            let webhookEvent = entry.changes[0].value;

            user_tags = {
                service: "whatsapp",
                wp_id: entry.id,
                phone: webhookEvent.metadata.display_phone_number,
                phone_id: webhookEvent.metadata.phone_number_id
            };

            // Check if contact exists
            if (webhookEvent.contacts && webhookEvent.contacts[0].profile) {
                user_tags.name = webhookEvent.contacts[0].profile.name;
            }
            // Check if message comes in the request
            if (webhookEvent.messages && webhookEvent.messages[0].text) {
                // Get the id sender
                senderPsid = webhookEvent.messages[0].from;
                message = webhookEvent.messages[0].text.body;
                message_tags = {
                    wp_id: webhookEvent.metadata.phone_number_id
                }
            }
        }
        // Send
        SendRequestDemeter(senderPsid, message, user_tags, message_tags);
    });
    // Returns a '200 OK' response to all requests
    res.status(200).send('EVENT_RECEIVED');
});


// Handles messages events
function SendRequestDemeter(senderPsid, message, user_tags, message_tags) {

    console.log('WEBHOOK | REQUEST | ' + senderPsid + ' | ' + message + " | " + user_tags + " | " + message_tags);
    // Create the payload for a basic text message, which
    let json = {
        melisa: conf.MELISA_NAME,
        token: conf.TOKEN_DEMETER,
        user: senderPsid,
        message: message,
        user_tags: user_tags,
        message_tags: message_tags
    }
    request({
        'uri': conf.DEMETER_URL,
        'method': 'POST',
        'json': json
    }, (err, _res, _body) => {
        if (!err) {
            console.log('WEBHOOK | RESPONSE |' + _res);
        } else {
            console.log('WEBHOOK | ERROR |' + err);
        }
    });
}

// Creates the endpoint for receptor
app.post('/receptor', (req, res) => {
    log_request(req);
    let body = req.body;
    let token = body.token,
        messages = body.text,
        senderPsid = body.user_id;
    // Checks if this is an event from a page subscription
    if (token === conf.TOKEN_DEMETER) {

        // Iterates over each entry - there may be multiple if batched
        messages.forEach(function (message) {
            if (message != "") {
                let response = { 'text': message };
                if (body.message_tags && body.message_tags.wp_id) {
                    callSendAPIWhatsapp(senderPsid, response, body.message_tags.wp_id)
                }
                else {
                    callSendAPIFacebook(senderPsid, response);
                }
            }
        });

        // Returns a '200 OK' response to all requests
        res.status(200).send('EVENT_RECEIVED');
    } else {

        // Returns a '404 Not Found' if event is not from a page subscription
        res.sendStatus(404);
    }
});


// Sends response messages via the Send API
function callSendAPIFacebook(senderPsid, response) {

    // Construct the message body
    let requestBody = {
        'recipient': {
            'id': senderPsid
        },
        'message': response
    };

    // Send the HTTP request to the Messenger Platform
    request({
        'uri': 'https://graph.facebook.com/v2.6/me/messages',
        'qs': { 'access_token': conf.PAGE_ACCESS_TOKEN },
        'method': 'POST',
        'json': requestBody
    }, (err, _res, _body) => {
        if (!err) {
            console.log('Message sent to FACEBOOK!');
        } else {
            console.error('Unable to send message FACEBOOK:' + err);
        }
    });
}

function callSendAPIWhatsapp(senderPsid, response, from) {
    const json = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": senderPsid,
        "type": "text",
        "text": { "preview_url": false, "body": response.text }
    };

    request({
        'uri': 'https://graph.facebook.com/v13.0/' + from + '/messages',
        'qs': { 'access_token': conf.PAGE_ACCESS_TOKEN },
        'method': 'POST',
        'json': json
    }, (err, _res, _body) => {
        if (!err) {
            console.log('Message sent WHATSAPP!');
        } else {
            console.error('Unable to send message WHATSAPP:' + err);
        }
    });
}

// listen for requests :)
var listener = app.listen(conf.PORT, conf.HOSTNAME, function () {
    console.log('Melisa is listening on port ' + listener.address().port);
});

// nohup npm start > melisa.log 2>&1 &