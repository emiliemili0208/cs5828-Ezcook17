# from django.db import models
# from django.utils import timezone
#
# class PostNew(models.Model):
#     #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     def __str__(self):
#         return self.title
#
# class Ingredient(models.Model):
#     name = models.CharField(max_length=200)
#     amount = models.CharField(max_length=200)


import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class UserModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True, default=uuid.uuid1())
    lastname = columns.Text(required=False)
    firstname = columns.Text(required=False)
    username = columns.Text()
    password = columns.Text()
    admin = columns.Boolean(required=False)
    favorite = columns.Set(columns.UUID(), required=False)
    stock = columns.Map(columns.Text(), columns.Float(), required=False)


class RecipeModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True, default=uuid.uuid1())
    owner = columns.Text(primary_key=True)
    title = columns.Text(required=True)
    content = columns.Text(max_length=100)
    ingredients = columns.Map(columns.Text(), columns.Float(), required=False)
    post_time = columns.DateTime()

class IngredientModel(DjangoCassandraModel):
    class Meta:
        get_pk_field='id'
    id = columns.UUID(primary_key=True, default=uuid.uuid1())
    name = columns.Text(primary_key=True)
    category  = columns.Text()
    usedby = columns.List(columns.UUID)
