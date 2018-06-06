from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import PostForm, IngredientForm
from .models import UserModel, RecipeModel, IngredientModel
from django.utils import timezone
from django.shortcuts import redirect
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

#Adding by Yi
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

import uuid
from datetime import datetime
import json
# import thread
import requests
import os
from django.conf import settings
from django.http import HttpResponse


def write_file(pk):
    post = get_object_or_404(RecipeModel, id=uuid.UUID(pk))
    title = post.title.replace(" ","_")
    with open("{}.txt".format(title), 'w+') as f:
        f.write('Title: {}, Description: {}, Author: {}'.format(post.title, post.content, post.owner))
    # testfile = urllib.URLopener()
    # testfile.retrieve("{}.txt".format(title), "{}.txt".format(title))
    file_path = os.path.join(settings.MEDIA_ROOT, "{}.txt".format(title))
    print(file_path)
    if os.path.exists(file_path):
        print('hi')
        with open(file_path, 'rb') as fh:
            print('hi2')
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename("{}.txt".format(title)
)
            return response
    raise Http404

def download(request, pk):
    # thread.start_new_thread(write_file, (pk, ))
    # return redirect('post_detail_without_edit', pk=pk)
    return write_file(pk)


def get_user_profile(request, username):
    print(username)
    user = get_object_or_404(User, username=username)
    print(user.username)
    post_list = []
    if RecipeModel.objects.filter(owner=str(username)):
        posts = RecipeModel.objects.filter(owner=str(username))
        # print(posts)
        for model in posts:
            post_list.append(model)
            print(model)
    post_list.sort(key=lambda post: post.post_time, reverse=True)
    return render(request, 'user_profile.html', {'profile_user':  user, 'posts': post_list})

def get_user_account(request, username):
    print(username)
    user = get_object_or_404(User, username=username)
    print(user.username)
    return render(request, 'account.html', {'account':  user})

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request,'login_form.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        print("get post")
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_model = UserModel.objects.create(id = uuid.uuid1(), username=username, password=raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list_without_edit')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_form(request):
    logout(request)
    return redirect('post_list_without_edit')

def post_list_without_edit(request):
    posts = RecipeModel.objects.all()
    post_list = []
    for model in posts:
        post_list.append(model)
        print(model)
    post_list.sort(key=lambda post: post.post_time, reverse=True)
    data = {}
    count = 1
    for i in post_list:
        tmp = {}
        tmp['id'] = str(i.id)
        tmp['owner'] = str(i.owner)
        tmp['post_time'] = i.post_time.strftime('%Y-%m-%dT%H:%M:%S')
        tmp['title'] = i.title
        tmp['content'] = i.content
        data[str(count)] = tmp
        count+=1
    print(json)
    if request.is_ajax():
        return HttpResponse(json.dumps(data))
    else:
        return render(request, 'post_list_without_edit.html', {'posts': post_list})

def post_detail_without_edit(request, pk):
    post = get_object_or_404(RecipeModel, id=uuid.UUID(pk))
    if UserModel.objects.filter(username=str(request.user)):
        user = UserModel.objects.filter(username=str(request.user)).get()
        user_ingred = user.stock
        post_ingred = post.ingredients
        shop_ingred = []
        for i in post_ingred:
            if i not in user_ingred:
                shop_ingred.append(i)
        print(shop_ingred)
        post.shop_ingred = shop_ingred

    return render(request, 'post_detail_without_edit.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(RecipeModel, id=uuid.UUID(pk))
    user = UserModel.objects.filter(username=str(request.user)).get()

    user_ingred = user.stock
    post_ingred = post.ingredients
    shop_ingred = []
    for i in post_ingred:
        if i not in user_ingred:
            shop_ingred.append(i)
    print(shop_ingred)
    post.shop_ingred = shop_ingred
    return render(request, 'post_detail.html', {'post': post})

def post_list(request):
    print("Hey this is post list")
    post_list = []
    if RecipeModel.objects.filter(owner=str(request.user)):
        posts = RecipeModel.objects.filter(owner=str(request.user))
        # print(posts)
        for model in posts:
            post_list.append(model)
            print(model)
        post_list.sort(key=lambda post: post.post_time, reverse=True)
    return render(request, 'post_list.html', {'posts': post_list})

def favorite_list(request):
    post_list = []
    if UserModel.objects.filter(username=str(request.user)):
        user = UserModel.objects.filter(username=str(request.user)).get()
        favor = user.favorite
        # print(posts)
        for post_id in favor:
            model = RecipeModel.objects.filter(id=post_id).get()
            post_list.append(model)
            print(model)
        post_list.sort(key=lambda post: post.post_time, reverse=True)
    return render(request, 'post_list_without_edit.html', {'posts': post_list})

def post_new(request):
    if request.method == "POST":
        myDict = dict(request.POST.lists())
        title = myDict['title'][0]
        content = myDict['content'][0]
        ingred_list = myDict['ingred[]']
        amount_list = myDict['amount[]']
        ingredients = {}
        for i, a in zip(ingred_list, amount_list):
            if i != "":
                ingredients[i] = a
        Rid = uuid.uuid1()
        post_model = RecipeModel.objects.create(id = Rid, title=title, content=content, owner=str(request.user), post_time=datetime.now(), ingredients=ingredients)
        for item in ingred_list:
            if IngredientModel.objects.filter(name=str(item)):
                ingred = IngredientModel.objects.filter(name=str(item)).get()
                ingred_usedby = ingred.usedby
                ingred_usedby.append(Rid)
                IngredientModel.objects(id=ingred.id, name=item).update(usedby=ingred_usedby)
            else:
                ingred_usedby = []
                ingred_usedby.append(Rid)
                IngredientModel.objects.create(id = uuid.uuid1(), name=item, usedby=ingred_usedby)
        return redirect('post_detail', pk=str(post_model.pk))
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(RecipeModel, id=pk)
    if request.method == "POST":
        myDict = dict(request.POST.iterlists())
        title = myDict['title'][0]
        content = myDict['content'][0]
        ingred_list = myDict['ingred[]']
        amount_list = myDict['amount[]']
        ingredients = {}
        for i, a in zip(ingred_list, amount_list):
            if i != "":
                ingredients[i] = a
        print(ingredients)
        post.title = title
        post.content = content
        post.ingredients = ingredients
        post.post_time = datetime.now()
        post.save()
        Rid = post.id
        for item in post.ingredients:
            if IngredientModel.objects.filter(name=str(item)):
                ingred = IngredientModel.objects.filter(name=str(item)).get()
                ingred_usedby = ingred.usedby
                ingred_usedby.append(Rid)
                IngredientModel.objects(id=ingred.id, name=item).update(usedby=ingred_usedby)
            else:
                ingred_usedby = []
                ingred_usedby.append(Rid)
                IngredientModel.objects.create(id = uuid.uuid1(), name=item, usedby=ingred_usedby)

            return redirect('post_detail', pk=str(post.pk))
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def my_stock(request):
    user = UserModel.objects.filter(username=str(request.user)).get()
    ingredients = user.stock
    # print(type(ingredients))

    Recipe = {}
    # print(ingredients)
    for i in ingredients:
        if IngredientModel.objects.filter(name=str(i)):
            ingred = IngredientModel.objects.filter(name=str(i)).get()
            for r in ingred.usedby:
                if r not in Recipe:
                    Recipe[r] = 1
                else:
                    Recipe[r] += 1
    s = [(r, Recipe[r]) for r in sorted(Recipe, key=Recipe.get, reverse=True)]
    print(s)
    i = 1
    Recommendation = {}
    for recpie, count in s:
        if i > 5:
            break
        rec = RecipeModel.objects.filter(id=recpie).get()
        need = 0
        for ingred in rec.ingredients:
            if ingred not in ingredients:
                need += 1
        i += 1
        Recommendation[recpie] = need
    r = [(f, Recommendation[f]) for f in sorted(Recommendation, key=Recommendation.get, reverse=False)]
    print(r)
    i = 1
    Final = []
    for recpie, count in r:
        if i > 3:
            break
        rec = RecipeModel.objects.filter(id=recpie).get()
        Final.append(rec)
        i += 1

    # print("my ingredients: {}".format(ingredients))
    # print("Recommendation: {}".format(ingredients))
    print(Final)
    return render(request, 'my_stock.html', {'ingredients': ingredients, 'recommendation': Final})

def add_ingredient(request):
    user = UserModel.objects.filter(username=str(request.user)).get()
    ingredients = user.stock
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            ingredient_name = form.cleaned_data['name']
            ingredient_amount = form.cleaned_data['amount']
            ingredients[ingredient_name] = ingredient_amount
            user.save()
            if IngredientModel.objects.filter(name=str(ingredient_name)):
                ingred = IngredientModel.objects.filter(name=str(ingredient_name)).get()
                ingred_usedby = ingred.usedby
                IngredientModel.objects(id=ingred.id, name=ingredient_name).update(usedby=ingred_usedby)
            else:
                IngredientModel.objects.create(id=uuid.uuid1(), name=ingredient_name, usedby=[])
            return redirect('my_stock')
    else:
        form = IngredientForm()
    return render(request, 'add_ingredient.html', {'form': form, 'ingredients': ingredients})

# def edit_ingredient(request, name):
#     user = UserModel.objects.filter(username=str(request.user)).get()
#     ingredients = user.ingredients
#     ingred
#     # print(ingred.name)
#     if request.method == "POST":
#         # form = PostForm(request.POST, instance=post)
#         form = IngredientForm(request.POST, instance=ingred)
#         print(form)
#         form.name = name
#         if form.is_valid():
#             ingredient = form.save(commit=False)
#             ingredient.save()
#             print(type("{now():{}}"))
#             # cluster = Cluster(['18.219.216.0'])
#             # session = cluster.connect()
#             # ingred_map = "{'"+str(ingredient.name)+"':"+str(ingredient.amount)+"}"
#             # sql = "update ezcook17.user set ingredients = ingredients + {} where id = 1 and username = '{}'".format(ingred_map, str(request.user))
#             # print(sql)
#             # session.execute(sql)
#             return redirect('my_stock')
#     else:
#         form = IngredientForm()
#     return render(request, 'edit_ingredient.html', {'form': form})
