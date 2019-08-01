from django.http import JsonResponse
from django.shortcuts import render
import json
import re

from datetime import datetime
from time import sleep

from .languages import content
from .models import Email, PressRu, PressEn


def change_content(language):
	changed_content      = content[language]
	not_changing_content = [
							'sending',
							'sending_completed_error',
							'sending_completed_success'
						   ]

	for item in not_changing_content:
		if item in changed_content:
			del changed_content[item]

	return changed_content


def index(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	print('New user\'s ip ' + ip + '\nDate: ' + str(datetime.now()))
	return render(request, 'main/index.html', change_content('ru'))


def get_data_for_messages(request):
	# sleep(5)
	print(request.POST.get('language'))
	if not request.POST.get('sender') or not request.POST.get('email') or not request.POST.get('msg') or not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', request.POST.get('email')):
		if request.POST.get('language') == 'ru':
			response_data = {'flag': 0, 'reply': 'Сообщение не отправлено! Возможно, одно из полей не заполненно или заполненно некорректно'}
		else:
			response_data = {'flag': 0, 'reply': 'The message didn\'t send. Perhapse, one field didn\'t input or input is incorrect'}
	else:
		# print(content[request.POST.get('language')]['sending_completed_success'])
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		# email = Email.objects.create(sender_ip=ip, sender_name=request.POST.get('sender'), reply_email=request.POST.get('email'), message=request.POST.get('msg'), csrf_token=request.POST.get('csrfmiddlewaretoken'))
		email = Email.objects.create(sender_ip=ip, sender_name=request.POST.get('sender'), reply_email=request.POST.get('email'), message=request.POST.get('msg'))
		if request.POST.get('language') == 'ru':
			response_data = {'flag': 1, 'reply': 'Сообщение отправлено'}
		else:
			response_data = {'flag': 1, 'reply': 'The message is sent'}
		email.email_send(request.POST.get('language'))
		message_for_console = f"\n\nNew email:\nthere was sent new email from {request.POST.get('sender')}, \nfrom ip address: {ip}, \ncsrf-token: {request.POST.get('csrfmiddlewaretoken')}, \nreply email: {request.POST.get('email')}, \nthe content of email: {request.POST.get('msg')}\n" + ('-' * 25)
		print(message_for_console)
	return JsonResponse(response_data)


def get_press(request):
	new_press_list = []
	response_data  = {}
	language       = request.GET.get('language')

	if language == 'ru':
		press = PressRu
	else:
		press = PressEn

	if int(request.GET.get('flag')) == 0:
		# print('1')
		new_press_list               = press.objects.order_by('added_at').reverse()[:5]
		new_list_id                  = sorted(list(i for i in new_press_list.values_list('id', flat=True)))
		response_data['new_list_id'] = new_list_id	
		print('new_list_id:', new_list_id)
	else:
		# print('2')
		last_list_id   = json.loads(request.GET.get('list_id'))

		if int(request.GET.get('flag')) == 1:
			# print('3')
			try:
				new_list_id = list(i for i in press.objects.order_by('added_at').reverse()[:5].values_list('id', flat=True))
			except:
				new_list_id = []
		else:
			# print('4')
			new_list_id     = list(i for i in press.objects.new().values_list('id', flat=True))

		print('last_list_id: ', last_list_id)
		print('new_list_id:', new_list_id)

		print(list(set(new_list_id) - set(last_list_id)) == [])

		response_data['new_list_id'] = new_list_id
			
		if int(request.GET.get('flag')) == 1:
			# print('7')
			id_list = sorted(list(set(new_list_id) - set(last_list_id)))
		else:
			# print('8')
			id_list = list(set(new_list_id) - set(last_list_id))
			id_list.sort(reverse=True)

		for id in id_list:
			# print('9')
			new_press_list.append(press.objects.get(id=id))
			
		old_press_list = list(id for id in list(set(last_list_id) - set(new_list_id)))
		response_data['old_press_list'] = old_press_list

	# print('flag', request.GET.get('flag'))
	try:
		# print('10')
		arr_new = []
		for new in reversed(new_press_list):
			# print('11')
			dic             = {}
			dic['id']       = new.id
			dic['text']     = new.text
			dic['title']    = new.title
			dic['author']   = new.author
			dic['source']   = new.source
			dic['added_at'] = new.added_at.strftime('%b %d, %Y %H:%M:%S')
			arr_new.append(dic)
		response_data['new_press_list'] = arr_new

		if press.objects.count() > 5:
			response_data['show_modal'] = True
		else:
			response_data['show_modal'] = False		

	except:
		response_data = {'result': 'Error'}
	print(response_data)
	return JsonResponse(response_data)


def get_message_for_waiting(request):
	print('Get message for waiting')
	print(type(request.GET.get('language')), request.GET.get('language'))
	if request.GET.get('language') == 'ru':
		return JsonResponse({'message': 'Пожалуйста, подождите, идёт отправка...'})
	else:
		return JsonResponse({'message': 'Please wait, the message is sending...'})
	
	
def get_changed_language_content(request):
	print('Changing language')
	return JsonResponse({'content': change_content(request.GET.get('language'))})
