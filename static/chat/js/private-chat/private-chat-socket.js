
let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

// get chat name from html input to start websocket
let chatName = $("#chat-name").val();

// create websocket using chat name
let privateChatSocket = new WebSocket(`ws://${window.location.host}/ws/private-chat/${chatName}/`);


// get current user from html input
let currentUser = $("#current-user").val();

function saveMessage(messageText, currentUser) {

    $.ajax({
        type: "post",
        data: {
            messageText: messageText,
            messageAuthor: currentUser,
            csrfmiddlewaretoken: csrf_token,
        },
        success: (event) => {
            sendMessageToServer(messageText, currentUser, event.message_timestamp);
        }
    });

}

// function to send message to the server
function sendMessageToServer(messageText, currentUser, messageTimestamp) {

    // get message info and put it in an object
    let messageInfo = {
        text: messageText,
        author: currentUser,
        timestamp: messageTimestamp
    }
    
    // send object to server as a string
    privateChatSocket.send(JSON.stringify(messageInfo));

    // reset input value
    $("#message-input").val("");
}

// send message when send button is clicked
$("#message-send").click(() => {
    let messageText = $("#message-input").val();
    saveMessage(messageText, currentUser);
});

// send message when enter key is pressed
$("#message-input").keydown((e) => {
    if (e.keyCode === 13) {
        let messageText = $("#message-input").val();
        saveMessage(messageText, currentUser);
    }
}); 


// recieve message from server
privateChatSocket.onmessage = (e) => {

    let messageInfo = JSON.parse(e.data)

    // appends message to chat log with sent or recieved class depending on if the current user sent the message or not
    if (currentUser == messageInfo.author) {
        $("#chat-log").append(`
            <h5 class="sent text-right mr-3 mt-3">${messageInfo.text}</h5>
            <h6 class="sent text-right mr-3">${messageInfo.author}</h6>
            <h6 class="sent text-right mr-3 mb-3">${messageInfo.timestamp}</h6>
            `)
    } else {
        $("#chat-log").append(`
            <h5 class="recieved text-left ml-3 mt-3">${messageInfo.text}</h5>
            <h6 class="recieved text-left ml-3">${messageInfo.author}</h6>
            <h6 class="recived text-left ml-3 mb-3">${messageInfo.timestamp}</h6>
            `)
    }
};