$(document).ready(() => {

	let user_authenticated = $("#auth").val();

	let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

	// get data from server upon page load
	let usernames, friendsList, pendingFriendRequests, friendRequestPKs;
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

});