// get chat name from html input to start websocket
let chatName = $("#chat-name").val();

// create websocket using chat name
let publicChatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatName}/`);

// get current user from html input
let currentUser = $("#current-user").val();

// function to send message to the server
function sendMessageToServer() {
    // get message info and put it in an object
    let messageText = $("#message-input").val();
    let messageInfo = {
        text: messageText,
        author: currentUser
    }
    
    // send object to server as a string
    publicChatSocket.send(JSON.stringify(messageInfo));

    // reset input value
    $("#message-input").val("");
}

// send message when send button is clicked
$("#message-send").click(() => {
    sendMessageToServer();
});

// send message when enter key is pressed
$("#message-input").keydown((e) => {
    if (e.keyCode === 13) {
        sendMessageToServer();
    }
}); 


// recieve message from server
publicChatSocket.onmessage = (e) => {

    let messageInfo = JSON.parse(e.data)

    // appends message to chat log with sent or recieved class depending on if the current user sent the message or not
    if (currentUser == messageInfo.author) {
        $("#chat-log").append(`
            <h5 class="sent text-right mr-3 mt-3">${messageInfo.text}</h5>
            <h6 class="sent text-right mr-3 mb-3">${messageInfo.author}</h6>
            `)
    } else {
        $("#chat-log").append(`
            <h5 class="recieved text-left ml-3 mt-3">${messageInfo.text}</h5>
            <h6 class="sent text-left ml-3 mb-3">${messageInfo.author}</h6>
            `)
    }
};
