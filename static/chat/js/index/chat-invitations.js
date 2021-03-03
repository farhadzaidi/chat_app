
// accept or decline private chat invitations
function privateChatInvitations() {
	for (let pk of chatInvitationPKs) {

		$(`#accept-invitation-${pk}`).click(()=> {

			$.ajax({
				type: "post",
				data: {
					acceptInvitation: pk,
					csrfmiddlewaretoken: csrf_token,
				},
				success: () => {
					$(`#chat-invitation-${pk}`).remove();
					location.reload();
				},
			});

		});

		$(`#decline-invitation-${pk}`).click(()=> {

			$.ajax({
				type: "post",
				data: {
					declineInvitation: pk,
					csrfmiddlewaretoken: csrf_token,
				},
				success: () => {
					$(`#chat-invitation-${pk}`).remove();
				},
			});

		});

	}

}