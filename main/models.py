from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.http import Http404

from time import strftime

from .languages import content


class Email(models.Model):
	sender_ip     = models.GenericIPAddressField()
	sender_name   = models.CharField("Sender's name:", max_length=100, help_text='Please, enter your name')
	reply_email   = models.EmailField("Feedback's email:", help_text='Please, enter your email for feedback')
	message       = models.TextField(help_text='Please, enter your answer')
	creation_date = models.DateTimeField(auto_now_add=True)
	# csrf_token    = models.CharField(max_length=100)

	def email_send(self, language):
		title         = f'ACL-LAW.COM message from: {self.sender_name}'
		creation_date = self.creation_date.strftime('%b %d, %Y %H:%M:%S')
		message       = f'{self.message} \
						\n\nEmail for reply: {self.reply_email} \
						\n\nCreation date of message: {creation_date}'
		print(('-' * 25) + '\n' + 'There is a new email...\n' + title + '\n' + message + '\n')
		send_mail(
			title,  
			message, 
			settings.EMAIL_HOST_USER,
			# [settings.EMAIL_HOST_USER, 'acl4client@gmail.com'],
			[settings.EMAIL_HOST_USER],
			fail_silently=False
		)
		print('EMAIL SENT TO ', [settings.EMAIL_HOST_USER, 'acl4client@gmail.com'])

		reply_title   = content[language]['content_for_reply_title'] 
		reply_message = f"{content[language]['content_for_reply_hello']}{self.sender_name}!{content[language]['content_for_reply_message']}"
		send_mail(
			reply_title,  
			reply_message, 
			settings.EMAIL_HOST_USER,
			[self.reply_email],
			fail_silently=False
		)
		print('EMAIL SENT TO ', self.reply_email)
    

class PressManager(models.Manager):
	def new(self):
		return super(PressManager, self).get_queryset().order_by('-id')


class PressRu(models.Model):
	title    = models.CharField(max_length=100)
	text     = models.TextField()
	added_at = models.DateTimeField("Date:")
	author   = models.CharField("Author:", max_length=100)
	source	 = models.URLField('Source:')
	objects  = PressManager()

	def __str__(self):
		return self.title
    

class PressEn(models.Model):
	title    = models.CharField(max_length=100)
	text     = models.TextField()
	added_at = models.DateTimeField("Date:")
	author   = models.CharField("Author:", max_length=100)
	source	 = models.URLField('Source:')
	objects  = PressManager()
    
	def __str__(self):
		return self.title