jQuery ->
	error_func = (response, a, b) ->
		if response.status == 403
			if response.responsJSON.data.message == "User must be a volunteer"
				$('#content').prepend('<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button>User must be a volunteer.</div>')
			else
				window.location = "/login?next=" + window.location
		undefined

	$('.button-div').on('click', '.org-active', ->
		alert 'hai'
		button = $(this)
		if not button.hasClass('disabled')
			id = button.data('id')
			response = $.ajax(
				'/ajax/main/join_org.json'
				data:
					'id': id
				success: (data) ->
					button.removeClass('btn-primary org-active').addClass('btn-success org-disabled disabled').html('Member')
				error: error_func
				timeout: 3000
				type: "POST"
			)
		undefined
	)

	$('.button-div').on('mouseenter', '.org-disabled', ->
		$(this).removeClass('disabled btn-success').addClass('btn-danger').html('Remove')
		undefined
	)

	$('.button-div').on('mouseleave', '.org-disabled', ->
		$(this).removeClass('btn-danger').addClass('disabled btn-success').html('Member')
		undefined
	)

	$('.button-div').on('click', '.org-disabled', ->
		button = $(this)
		id = button.data 'id'
		response = $.ajax(
			'/ajax/main/unjoin_org.json'
			data:
				'id': id
			success: (data) ->
				button.removeClass('btn-danger btn-success disabled org-disabled').addClass('btn-primary org-active').html('Join organization')
			error: error_func
			timeout: 3000
			type: "POST"
		)	
		undefined
	)
	undefined