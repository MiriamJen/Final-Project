from django.db import models
import re
import bcrypt 
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address"
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if form['password'] != form['confirm']:
            errors['password'] = "Passwords do not match"
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def register (self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            username = form['username'],
            password = pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    username = models.CharField(max_length=55, unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #user_reviews
    #liked_reviews
    #user_comments

    objects = UserManager()

    def __repr__(self):
        return f"<User.object:{self.first_name} {self.last_name} {self.username}>"
        
class Review(models.Model):
    title = models.CharField(max_length=255, null=True)
    rose = models.CharField(max_length=255)
    bud = models.CharField(max_length=255)
    thorn = models.CharField(max_length=255)
    review_type = models.CharField(max_length=255)
    reviewer = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #review_comments

    def __repr__(self):
        return f"<Review.objects: {self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    review_comment = models.ForeignKey(Review, related_name='review_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Comment.objects{self.comment}>"
# Create your models here.
