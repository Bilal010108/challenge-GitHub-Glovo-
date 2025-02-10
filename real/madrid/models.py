from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django .contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True, region='KG')
    ROLES_CHOICES =(
        ('клиент', 'клиент'),
        ('курьер', 'курьер'),
        ('владелец', 'владелец'),
        ('aдминистратор','администратор')
    )
    user_role = models.CharField(max_length=16,choices=ROLES_CHOICES, default='клиент')
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(16), MaxValueValidator(50)])


    def __str__(self):
       return f'{self.username}'




class Category(models.Model):
    category_name =models.CharField(max_length=20,unique=True)


    def __str__(self):
       return self.category_name


class Store(models.Model):
    store_name = models.CharField(max_length=20)
    store_description =models.TextField(null=True,blank=True)
    contact_info = PhoneNumberField(null=True,blank=True,region='KG')
    address = models.TextField(null=True,blank=True)
    owner = models.ForeignKey(UserProfile,related_name='store',on_delete=models.CASCADE)


    def __str__(self):
        return self.store_name


    def get_avg_rating(self):
        ratings = self.store_review.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return  0

    def get_total_people(self):
        people = self.store_review.all()
        if people.exists():
            if people.count() > 3:
                return '+3'
            return people.count()
        return 0

    def get_total_good(self):
        total = self.store_review.count()
        good = self.store_review.filter(rating__gt=3).count()
        return f'{round((good * 100) / total)}%' if total > 0 else '0%'




class StoreImage(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_image = models.ImageField(upload_to='store_image/', null=True, blank=True)


    def __str__(self):
       return f'{self.store_image}'



class Product(models.Model):
    product_name =models.CharField(max_length=16)
    description = models.TextField(null=True,blank=True)
    price = models.PositiveIntegerField(default=0)
    quantity =models.PositiveSmallIntegerField(default=1)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product')
    category =models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_product')
    def __str__(self):
        return f'{self.product_name}'


    def get_avg_rating(self):
        ratings = self.store_review.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return 0


    def get_total_people(self):
        people = self.store_review.all()
        if people.exists():
            if people.count() > 3:
                return '+3'
            return people.count()
        return 0

    def get_total_good(self):
        total = self.store_review.count()
        good = self.store_review.filter(rating__gt=3).count()
        return f'{round((good * 100) / total)}%' if total > 0 else '0%'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)


    def __str__(self):
        return f'{self.product},{self.product_image}'







class Order(models.Model):
    client =models.ForeignKey(UserProfile,related_name='product_owners',on_delete=models.CASCADE)
    products = models.ForeignKey(Product,related_name='products_orders',on_delete=models.CASCADE)
    STATUS_ORDER_CHOICES = [
        ('Ожидает обработки', 'Ожидает обработки'),
        ('В процессе доставки', 'В процессе доставки'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен')
    ]
    status_order = models.CharField(max_length=20,choices=STATUS_ORDER_CHOICES,default='Ожидает обработки')
    delivery_address =models.TextField(null=True,blank=True)
    courier = models.ForeignKey(UserProfile,related_name='order_courier',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)



    def __str__(self):
       return f'{self.client},{self.status_order}'




class Courier(models.Model):
    user = models.ForeignKey(UserProfile,related_name='user',on_delete=models.CASCADE)
    STATUS_COURIER_CHOICES = [

        ('доступен', 'доступен'),
        ('занят', 'занят')

    ]

    status_courier = models.CharField(max_length=20,choices=STATUS_COURIER_CHOICES,default='доступен')
    current_orders = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
       return f'{self.user},{self.status_courier}'





class Review(models.Model):
    client_review = models.ForeignKey(UserProfile, related_name='client_review',on_delete=models.CASCADE)
    store_review = models.ForeignKey(Store, related_name='store_reviews',on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for  i in  range(1, 6)])
    comment = models.TextField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self):
       return f'{self.client_review},{self.store_review}'



class ComboProduct(models.Model):
    combo_name =models.CharField(max_length=16)
    combo_description = models.TextField(null=True,blank=True)
    combo_price = models.PositiveSmallIntegerField(default=0)
    combo_quantity =models.PositiveSmallIntegerField(default=1)
    store = models.ForeignKey(Store, related_name='store_product_combo',on_delete=models.CASCADE)

    def __str__(self):
      return f'{self.combo_name},{self.combo_price}'

    def get_avg_rating(self):
        ratings = self.store_review.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return  0

    def get_total_people(self):
        people = self.store_review.all()
        if people.exists():
            if people.count() > 3:
                return '+3'
            return people.count()
        return 0

    def get_total_good(self):
        total = self.store_review.count()
        good = self.store_review.filter(rating__gt=3).count()
        return f'{round((good * 100) / total)}%' if total > 0 else '0%'


class ComboImage(models.Model):
    combo = models.ForeignKey(ComboProduct, on_delete=models.CASCADE)
    combo_image = models.ImageField(upload_to='combo_image/', null=True, blank=True)


    def __str__(self):
       return self.combo_image




class Cart(models.Model):
    client_cart = models.ForeignKey(UserProfile,related_name='client_cart',on_delete=models.CASCADE)


    def __str__(self):
       return str(self.client_cart)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE,)
    product_cart = models.ForeignKey(Product,related_name='product_cart',on_delete=models.CASCADE)
    quantity_cart =models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.product_cart)



class StoreReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_revieww')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.client} - {self.rating} - {self.store}'


class CourierReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='courier_revieww')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateTimeField(auto_now_add=True)
    comment_courier = models.TextField(null=True,blank=True)


    def __str__(self):
        return f'{self.courier},{self.rating}'