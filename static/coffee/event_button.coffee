jQuery ->
	error_func = (response, a, b) ->
		if response.status == 403
			if response.responseJSON.data.message == "User must be a volunteer"
				$('#content').prepend('<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button>User must be a volunteer.</div>')
			else
				window.location = "/login?next=" + window.location
		undefined

	update_status = (status) ->
		field = $('#user-status')
		if field
			field.html(status).removeClass()
			if status == "User-created event" or status == "Confirmed"
				field.addClass('text-success')
			else if status == "Unconfirmed"
				field.addClass('text-warning')
		undefined

	$('.button-div').on('click', '.commit-active', ->
		button = $(this)
		if not button.hasClass('disabled')
			id = button.data('id')
			response = $.ajax(
				'/ajax/main/do_event.json'
				data:
					'id': id
				success: (data) ->
					button.removeClass('btn-primary').addClass('btn-success commit-disabled disabled').html('Participating')
					update_status data.data.user_status
				error: error_func
				timeout: 3000
				type: "POST"
			)
		undefined
	)

	$('.button-div').on('mouseenter', '.commit-disabled', ->
		$(this).removeClass('disabled btn-success').addClass('btn-danger').html('Remove')
		undefined
	)

	$('.button-div').on('mouseleave', '.commit-disabled', ->
		$(this).removeClass('btn-danger').addClass('disabled btn-success').html('Participating')
		undefined
	)

	$('.button-div').on('click', '.commit-disabled', ->
		button = $(this)
		id = button.data 'id'
		response = $.ajax(
			'/ajax/main/dont_do_event.json'
			data:
				'id': id
			success: (data) ->
				button.removeClass('btn-danger btn-success disabled commit-disabled').addClass('btn-primary commit-active').html('Do this event!')
				update_status data.data.user_status
			error: error_func
			timeout: 3000
			type: "POST"
		)	
		undefined
	)
	undefined