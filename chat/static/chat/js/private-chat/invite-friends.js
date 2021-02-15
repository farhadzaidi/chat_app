let friendsSentTo;
$.ajax({
	type: "get",
	data: {
		getInfo: true,
	},
	success: (event) => {
		friendsSentTo = event.friends_sent_to;
	}
})


function validateInviteFriends(inviteFriends, friendsSentTo) {

	if (inviteFriends.length == 0) {
		return 'You must select at least one friend to invite.';
	} 

	else {

		for (let friend of inviteFriends) {

			if (friendsSentTo.includes(friend)) {
				return `You have already sent an invitation to ${friend}`
			}
		}

		return true;	
	}


}


$("#invite-friends-submit").click(() => {

	let inviteFriends = $("#invite-friends").val();
	let validate = validateInviteFriends(inviteFriends, friendsSentTo);
	
	if (validate == true) {
		$.ajax({
			type: "post",
			data: {
				inviteFriends: inviteFriends,
				csrfmiddlewaretoken: csrf_token,
			},
			success: () => {
				location.reload();
			}
		});
	} else console.log(validate);

});