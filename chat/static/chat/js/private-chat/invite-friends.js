
function validateInviteFriends(inviteFriends) {

	if (inviteFriends.length == 0) {
		return 'You must select at least one friend to invite.';
	} else return true;
}


$("#invite-friends-submit").click(() => {

	let inviteFriends = $("#invite-friends").val();
	let validate = validateInviteFriends(inviteFriends);
	
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