let user_authenticated = $("#auth").val();

let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

// get data from server upon page load
let usernames, friendsList, pendingFriendRequests, friendRequestPKs, privateChatNames;

let getInfo = () => {
    $.ajax({
        type: "get",
        data: {
            getInfo: true,
        },
        success: (event) => {
            usernames = event.usernames;
            friendsList = event.friends_list;
            pendingFriendRequests = event.pending_friend_requests;
            friendRequestPKs = event.friend_request_pks;
            chatInvitationPKs = event.chat_invitation_pks;
            privateChatNames = event.private_chat_names;
            friendRequests();
            privateChatInvitations();
        }
    });
}

if (user_authenticated == "yes") {
    getInfo();
}