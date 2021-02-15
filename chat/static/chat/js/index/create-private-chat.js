
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
			return 'The chat name can contain only alphanumeric characters and it must not contain any spaces.'
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

	let chatName = $("input[name=private-chat-name]").val();
	let inviteFriends = $("#invite-friends").val();

	createPrivateChat(chatName, inviteFriends);

});