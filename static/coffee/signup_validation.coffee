jQuery ->
	$('input[name="username"]').on('keyup', ->
		t = this
		if this.value != this.lastValue
			if this.timer 
				clearTimeout(this.timer)
			$('#username-help').html('...')
			this.timer = setTimeout(->
				$.ajax(
					url: '/ajax/main/username_valid.json'
					type: 'POST'
					data: 
						username: t.value
					success: (j) ->
						$('#username-help').html(j.data.message)
						if j.data.valid == true
							$('#username-help').parent().addClass('has-success').removeClass('has-error')
						else
							$('#username-help').parent().addClass('has-error').removeClass('has-success')
						undefined
					)
				undefined
			)
			this.lastValue = this.value
		undefined
	)

	$('input[name="password2"]').on('keyup', ->
		if this.value != $('input[name="password1"]')[0].value
			$('#password-help').html('Passwords do not match')
			$('#password-help').parent().addClass('has-error').removeClass('has-success')
		else
			$('#password-help').html('')
			$('#password-help').parent().addClass('has-success').removeClass('has-error')
	)

	$('button[type="submit"]').on('click', ->
		#TODO: check required stuff?
		undefined
	)

	undefined