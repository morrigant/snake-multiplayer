from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
import json
from .scheme import *
from .forms import *



class MainView(View):

	def get(self, request):
		return render(request, 'welcome.html', {'form' : NameForm()})

	def post(self, request):

		form = NameForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			room = get_room()
			key = room.init_snake(name, 25, 18, direction=2)

			args = {'room_id': room.id, 'key' : key, 'action' : 0}
			return render(request, 'field.html', args)

		return redirect('/')


class ChannelView(View):

	def render_ok_response(self, room):
		snakes_cells = []
		for snake in room.snakes:
			snakes_cells.append([ snake.name, [transform_coordinates(cell.x, cell.y) for cell in snake.cells] ])

		return json.dumps({'status' : 'OK', 'info' : {
			'appleCell' : transform_coordinates(room.apple.x, room.apple.y),
			'snakesCells': snakes_cells
            }
		})


	error_response = json.dumps({'status' : 'error'})

	def post(self, request):
		channel_form = ChannelForm(request.POST)

		if channel_form.is_valid():
			room_id = channel_form.cleaned_data['room_id']
			key = channel_form.cleaned_data['key']
			action = channel_form.cleaned_data['action']

			if action == 0:

				room = get_room(id=room_id)
				if room.is_auth(key):
					return HttpResponse(self.render_ok_response(room))

			if action == 1 or action == 2 or action == 3 or action == 4:

				room = get_room(room_id)

				if room.is_auth(key):
					snake = room.get_snake(key)
					snake.move(action)


		return HttpResponse(self.__class__.error_response)


class LoseView(View):
	
	def get(self, request):
		return render(request, 'lose.html')