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

// Respond with 'Hello World' when a GET request is made to the homepage
app.get('/', function (_req, res) {
    res.send('<h1>Running MelisaBot for Facebook</h1>');
});

// Adds support for GET requests to our webhook
app.get('/webhook', (req, res) => {

    // Parse the query params
    let mode = req.query['hub.mode'];
    let token = req.query['hub.verify_token'];
    let challenge = req.query['hub.challenge'];

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
    let body = req.body;

    // Checks if this is an event from a page subscription
    if (body.object === 'page') {

        // Iterates over each entry - there may be multiple if batched
        body.entry.forEach(function (entry) {

            // Gets the body of the webhook event
            let webhookEvent = entry.messaging[0];            

            // Get the sender PSID
            let senderPsid = webhookEvent.sender.id;            

            // Check if the event is a message or postback and
            // pass the event to the appropriate handler function
            if (webhookEvent.message) {
                handleMessage(senderPsid, webhookEvent.message);
            } else if (webhookEvent.postback) {
                handlePostback(senderPsid, webhookEvent.postback);
            }
        });

        // Returns a '200 OK' response to all requests
        res.status(200).send('EVENT_RECEIVED');
    } else {

        // Returns a '404 Not Found' if event is not from a page subscription
        res.sendStatus(404);
    }
});

// Creates the endpoint for receptor
app.post('/receptor', (req, res) => {
    let body = req.body;    
    let token = body.token,
        messages = body.text,
        senderPsid = body.user_id;

    // Checks if this is an event from a page subscription
    if (token === conf.TOKEN_DEMETER) {

        // Iterates over each entry - there may be multiple if batched
        messages.forEach(function (entry) {                        
            let response = { 'text': entry };
            callSendAPI(senderPsid, response);
            console.log('[RECEPTOR]|OK|' + senderPsid + "|" + entry);
        });

        // Returns a '200 OK' response to all requests
        res.status(200).send('EVENT_RECEIVED');
    } else {

        // Returns a '404 Not Found' if event is not from a page subscription
        res.sendStatus(404);
    }
});


// Handles messages events
function handleMessage(senderPsid, receivedMessage) {
    let response;

    // Checks if the message contains text
    if (receivedMessage.text) {
        console.log('[WEBHOOK]|OK|' + senderPsid + '|' + receivedMessage.text);
        // Create the payload for a basic text message, which
        // will be added to the body of your request to the Send API
        response = {
            //'text': `You sent the message: '${receivedMessage.text}'. Now send me an attachment!`
            'text':"Hemos recibido tu mensaje, en poco te enviaremos la información"
        };

        let url = conf.DEMETER_URL + "?melisa=" + conf.MELISA_NAME + "&token=" + conf.TOKEN_DEMETER + "&user=" + senderPsid + "&message=" + receivedMessage.text;
        axios.get(url)
            .then(response => {
                console.log('[WEBHOOK]|DEMETER|' + response.data);
            })
            .catch(error => {
                console.log('[WEBHOOK]|ERROR|' + error);
            });
    } else if (receivedMessage.attachments) {

        // Get the URL of the message attachment
        let attachmentUrl = receivedMessage.attachments[0].payload.url;
        response = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': 'Is this the right picture?',
                        'subtitle': 'Tap a button to answer.',
                        'image_url': attachmentUrl,
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Yes!',
                                'payload': 'yes',
                            },
                            {
                                'type': 'postback',
                                'title': 'No!',
                                'payload': 'no',
                            }
                        ],
                    }]
                }
            }
        };
    }

    // Send the response message
    //callSendAPI(senderPsid, response);
}

// Handles messaging_postbacks events
function handlePostback(senderPsid, receivedPostback) {
    let response;

    // Get the payload for the postback
    let payload = receivedPostback.payload;

    // Set the response based on the postback payload
    if (payload === 'yes') {
        response = { 'text': 'Thanks!' };
    } else if (payload === 'no') {
        response = { 'text': 'Oops, try sending another image.' };
    }
    // Send the message to acknowledge the postback
    callSendAPI(senderPsid, response);
}

// Sends response messages via the Send API
function callSendAPI(senderPsid, response) {

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
            console.log('Message sent!');
        } else {
            console.error('Unable to send message:' + err);
        }
    });
}

// listen for requests :)
var listener = app.listen(conf.PORT, conf.HOSTNAME, function () {
    console.log('Your app is listening on port ' + listener.address().port);
});

// nohup npm start > melisa.log 2>&1 &