import datetime
import json

from django.db.models import Sum
from django.db.utils import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

from finances.models import Asset, MonthlyStatement


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/finances/login')
		else:
			pass
	else:
		form = UserCreationForm()
		context = {'form': form}
	return render(request, 'finances/signup.html', context)


def log_in(request):
	error_message = None

	if request.method == 'POST':
		username = request.POST.get('username')
		raw_password = request.POST.get('password')
		user = authenticate(username=username, password=raw_password)
		if user:
			login(request, user)
			return redirect('/finances/home')
		else:
			error_message = 'Incorrect username or password'
	form = AuthenticationForm()
	context = {'form': form, 'message': error_message}
	return render(request, 'finances/login.html', context)	

def log_out(request):
	logout(request)
	return redirect('/finances/login')


@require_GET
def index(request):
	if not request.user.is_authenticated:
		return redirect('/finances/login')

	username = request.user.username
	user_id = request.user.id
	statement_objects = MonthlyStatement.objects.filter(user=user_id)
	if statement_objects:
		total_salary = statement_objects.aggregate(Sum('salary')).get('salary__sum')
		total_expenditure = statement_objects.aggregate(Sum('expenses')).get('expenses__sum')
		total_savings = statement_objects.aggregate(Sum('savings')).get('savings__sum')
		latest_liquid = statement_objects.latest('id').liquid
	else:
		total_salary = 0
		total_expenditure = 0
		total_savings = 0
		latest_liquid = 0
	

	asset_objects = Asset.objects.filter(active=True, user=user_id)
	if asset_objects:
		total_assets = asset_objects.aggregate(Sum('value')).get('value__sum')
	else:
		total_assets = 0

	total_assets += latest_liquid
	interest_earned = total_assets - total_savings
	if total_savings:
		percentage_earned = (interest_earned/total_savings)*100
	else:
		percentage_earned = 0

	stats = {
		'total_salary': total_salary,
		'total_expenditure': total_expenditure,
		'total_savings': total_savings,
		'total_assets': total_assets,
		'interest_earned': interest_earned,
		'percentage_earned': percentage_earned 
	}
	context = {'username': username, 'stats': stats}
	return render(request, 'finances/home.html', context)


@require_GET
def assets_view(request):
	if not request.user.is_authenticated:
		return redirect('/finances/login')

	user_id = request.user.id
	active_objects = Asset.objects.filter(active=True, user=user_id)
	inactive_objects = Asset.objects.filter(active=False, user=user_id)
	context = {'active_asset_objects': active_objects, 'inactive_asset_objects': inactive_objects}
	return render(request, 'finances/assets.html', context)


@require_POST
def assets_add(request):
	if not request.user.is_authenticated:
		return redirect('/finances/login')

	error_message = None
	try:
		new_asset = Asset(asset_type=request.POST.get('asset_type'), description=request.POST.get('description'),
			value=request.POST.get('value'), user=request.user)
		new_asset.save()
	except IntegrityError as e:
		print(e)
		error_message = 'Invalid input.'
	except Exception as e:
		print(e)
		error_message = e
	finally:
		if error_message:
			context = {'message': error_message, 'redirect_url': '/finances/assets/view'}
			return render(request, 'finances/alert.html', context)
	return redirect('/finances/assets/view')


@require_POST
def assets_update(request):
	return HttpResponse("Not implemented yet.")


@require_GET
def statements_view(request):
	if not request.user.is_authenticated:
		return redirect('/finances/login')

	user_id = request.user.id
	objects = MonthlyStatement.objects.filter(user=user_id)
	context = {'statement_objects': objects}
	return render(request, 'finances/statements.html', context)


@require_POST
def statements_add(request):
	if not request.user.is_authenticated:
		return redirect('/finances/login')

	error_message = None
	try:
		date = datetime.date(int(request.POST.get('year')), int(request.POST.get('month')), 1)
		new_statement = MonthlyStatement(month_year=date, salary=request.POST.get('salary'), 
			expenses=request.POST.get('expenses'), savings=request.POST.get('savings'), 
			liquid=request.POST.get('liquid'), user=request.user)
		new_statement.save()
	except IntegrityError as e:
		print(e)
		error_message = 'Either a statement entry for this month and year already exists or you entered invalid data.'
	except Exception as e:
		print(e)
		error_message = e
	finally:
		if error_message:
			context = {'message': error_message, 'redirect_url': '/finances/statements/view'}
			return render(request, 'finances/alert.html', context)
	return redirect('/finances/statements/view')


@require_POST
def statements_update(request):
	return HttpResponse("Not implemented yet.")
