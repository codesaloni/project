from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager, Group, Permission
from django.db import models
from django.conf import settings

class UserManager(DefaultUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('lister', 'Lister'),
        ('buyer', 'Buyer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')

    objects = UserManager()

    class Meta:
        permissions = [
            # Add custom permissions if needed
        ]

    def __str__(self):
        return self.username

  
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  
        blank=True
    )

class Product(models.Model):
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price