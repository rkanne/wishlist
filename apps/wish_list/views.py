from django.shortcuts import render, redirect , HttpResponse
from .models import Users, Wishlist, Join
from django.contrib import messages

def index(request):
	# request.session.clear()
	return render(request, 'wish_list/index.html')

def insert(request):
	if request.method == "POST":
		result = Users.registerMgr.register(request.POST['name'],request.POST['username'],request.POST['password'],request.POST['confirm_password'], request.POST['date_hired'])
		# print "result===",result
	 	if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/dashboard')
	 	else:
	 		# print result[0], "="*20
	 		for x in xrange(len(result[1])):
	 			print x
	 			messages.error(request, result[1][x])

	 		return redirect('/')

def login(request):
	# print "---Session----",request.session.get('user_id')
	
	if request.method == "POST":
		result = Users.loginMgr.login(request.POST['username_login'],request.POST['password_login'])
		login = Users.loginMgr.filter(username=request.POST['username_login'])
		wishlist = Wishlist.wishlistMgr.all()

		users = Users.registerMgr.all()
		if len(login)> 0:
			login = login[0].id, login[0].name
			request.session['user_id'] = login
		if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/dashboard')
	 	else:
	 		# print result[0], "="*20
	 		# request.session['message'] =result[1]
	 		if request.POST['password_login'] == "":
	 			messages.error(request, "Password is required!!")
	 		for x in xrange(len(result[1])):
	 			print x
	 			messages.error(request, result[1][x])
	 		return redirect('/')

def dashboard(request):
	if request.session.get('user_id') == None:
		return redirect('/')

	currentuser = request.session.get('user_id')
	wishes = Wishlist.wishlistMgr.filter(user_id=currentuser)
	joins = Join.joinsMgr.filter(user_id=currentuser)
	wishes_other = Wishlist.wishlistMgr.exclude(user_id=currentuser)
	for x in joins:
		wishes_other = wishes_other.exclude(id = x.wishlist.id)

	# print '='*50, request.session.get('user_id')
	context = {
	'joins': joins,
	'wishes' : wishes,
	'wishes_other': wishes_other
	}
	return render(request, 'wish_list/dashboard.html',context)	

def delete(request, id):
	Join.joinsMgr.filter(wishlist_id=id).delete()
	Wishlist.wishlistMgr.filter(id=id).delete()

	return redirect('/dashboard')

def remove(request, id):
	currentuser = request.session['user_id']
	print currentuser
	Join.joinsMgr.filter(user_id=currentuser).filter(wishlist_id=id).delete()
	return redirect('/dashboard')

def create_item(request):
	if request.session.get('user_id') == None:
		return redirect('/')
		
	currentuser = request.session.get('user_id')
	return render(request, 'wish_list/create_item.html')

def add_item(request):
	if request.method == "GET": 
		# print "Session === user_id====",type(request.session.get('user_id')[0])
		return render(request, 'wish_item/create_item.html')
	elif request.method == "POST":
			print "USER_ID++++++++++",request.session.get('user_id')
			print "item_name------", request.POST['item_name']
			wish = Wishlist.wishlistMgr.add(item_name=request.POST['item_name'])

			if wish[0]:
				wish = Wishlist.wishlistMgr.create(item_name=request.POST['item_name'],user_id =request.session.get('user_id'))
				wish.save()
				print wish.id, "="*100
				join = Join.joinsMgr.create(wishlist_id=wish.id, user_id=request.session.get('user_id'))
				return redirect('/dashboard')
			else:
				for x in xrange(len(wish[1])):
					print x
					messages.error(request, wish[1][x])
				return redirect('/wish_item/create')


def addwish(request, id):
	currentuser = request.session['user_id']

	Wish_id = Wishlist.wishlistMgr.filter(id=id)[0].id
	print "=====Wish_id===", Wish_id
	join = Join.joinsMgr.create(user_id=request.session.get('user_id'),wishlist_id=Wish_id)
	join.save()
	messages.error(request, 'Congratulation!! You have added')
	return redirect('/dashboard')

def wishitems(request, id):
	wishlist = Wishlist.wishlistMgr.filter(id=id)
	joins = Join.joinsMgr.filter(wishlist=id)
	user= Users.registerMgr.all()
	context = {
	'wishlist': wishlist,
	'joins': joins,
	'user':user
	}
	return render(request, 'wish_list/wish_items.html', context)

def logout(request):
	request.session.pop('user_id')
	request.session.pop('name')
	# Join.joinsMgr.all().delete()
	# Wishlist.wishlistMgr.all().delete()

	return redirect('/')





			

		