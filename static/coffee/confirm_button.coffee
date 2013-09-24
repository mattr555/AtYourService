jQuery ->
	$('.button-div').on('click', '.confirm-button.btn-success', ->
		console.log "clicked!"
		button = $(this)
		user_id = button.data 'user-id'
		event_id = button.data 'event-id'
		response = $.ajax(
			'/ajax/main/confirm_participant.json'
			data:
				'user_id': user_id
				'event_id': event_id
			success: (data) ->
				button.removeClass('btn-success').addClass(data.data.button_class).html(data.data.button_text)
				button.parents('tr').removeClass().addClass(data.data.row_class)
				button.parents('tr').children('.status-field').html(data.data.status)
			timeout: 3000
			type: "POST"
			)
		undefined)
	undefined
