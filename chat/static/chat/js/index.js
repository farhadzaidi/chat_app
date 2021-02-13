$(document).ready(() => {

	let user_authenticated = $("#auth").val();

	let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

	// get data from server upon page load
	let usernames, friendsList, pendingFriendRequests, friendRequestPKs, privateChatNames;
	if (user_authenticated == "yes") {
		$.ajax({
			type: "get",
			async: false, 
			data: {
				getData: true,
			},
			success: (event) => {
				usernames = event.usernames;
				friendsList = event.friends_list;
				pendingFriendRequests = event.pending_friend_requests;
				friendRequestPKs = event.friend_request_pks;
				privateChatNames = event.private_chat_names;
			}
		});
	}

	function validateFriendRequest(friendName) {

		if (!(usernames.includes(friendName))) {
			return `${friendName} is not a valid user.`;
		}

		else if (friendsList.includes(friendName)) {
			return `You are already friends with ${friendName}`;
		}

		else if (pendingFriendRequests.includes(friendName)) {
			return `You have already sent a friend request to ${friendName}`
		}

		else return true;


	}

	function sendFriendRequest() {
		let friendName = $("input[name=friend-name]").val();
		let validate = validateFriendRequest(friendName);

		if (validate == true) {

			$.ajax({
				type: "post",
				data: {
					friendName: friendName,
					csrfmiddlewaretoken: csrf_token,
				},
				success: () => {
					location.reload();	
				}
			});

		} else {
			console.log(validate)
			$("#add-friend-errors").append(`<p class="bg-danger text-dark">${validate}</p>`)
		}
	}

	// add friend on click
	$("#send-friend-request").click(() => {
		sendFriendRequest();

	});

	// add friend when enter is pressed
	$("input[name=friend-name]").keydown((e) => {
        if (e.keyCode === 13) {
            sendFriendRequest();
        }
    }); 


	// accept or decline friend requests
	if (user_authenticated == "yes") {
		for (let pk of friendRequestPKs) {

			$(`#accept-friend-${pk}`).click(()=> {

				$.ajax({
					type: "post",
					data: {
						acceptFriendPK: pk,
						csrfmiddlewaretoken: csrf_token,
					},
					success: () => {
						$(`#friend-request-${pk}`).remove();
						location.reload();
					},
				});

			});

			$(`#decline-friend-${pk}`).click(()=> {

				$.ajax({
					type: "post",
					data: {
						declineFriendPK: pk,
						csrfmiddlewaretoken: csrf_token,
					},
					success: () => {
						$(`#friend-request-${pk}`).remove();
					},
				});

			});

		}
	}

	function validatePrivateChat(chatName, inviteFriends) {

		if (inviteFriends.length == 0) {
			return 'You must at least invite one friend to create a new private chat'
		}

		else if (chatName == "") {
			return 'Please enter a chat name.';
		}

		else if (privateChatNames.includes(chatName)) {
			return `You are already in a chat named ${chatName}.`
		} 

		else {
			// regex to test for alphanumeric characters
			let re = /^[a-z0-9]+$/i

			if (re.test(chatName)) {
				return true;
			} else {
				return 'The chat name can contain only alphanumeric characters.'
			}
		}

	}

	function createPrivateChat(chatName, inviteFriends) {

		let validate = validatePrivateChat(chatName, inviteFriends);

		if (validate == true) {

			$.ajax({
				type: "post",
				data: {
					chatName: chatName,
					inviteFriends: inviteFriends,
					csrfmiddlewaretoken: csrf_token,
				},
				success: () => {
					location.reload();
				}
			});

		} else console.log(validate);


	}

	$("#create-private-chat").click(() => {

		let chatName = $("input[name=private-room-name]").val();
		let inviteFriends = $("#invite-friends").val();

		createPrivateChat(chatName, inviteFriends);

	});

});