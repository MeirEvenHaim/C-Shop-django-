from django.db import models
from django.contrib.auth.models import User

# Computer model
class Computer(models.Model):
    name = models.CharField(max_length=255)
    year_of_creation = models.IntegerField()
    parts = models.ManyToManyField('Part', related_name="computers")  # Many-to-many with Part
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_sell = models.DateField()
    supplier = models.CharField(max_length=255)
    firm = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='computers/', null=True, blank=True)

    def __str__(self):
        return self.name

# Part model
class Part(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='parts/', null=True, blank=True)
    description = models.TextField()
    firm = models.CharField(max_length=255)
    date_of_creation = models.DateField()
    date_of_sale = models.DateField(null=True, blank=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Game model
class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_of_publish = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    demands_standard_computer_software = models.TextField()
    image = models.ImageField(upload_to='games/', null=True, blank=True)
    firm = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Cart model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part, related_name="carts", blank=True)
    computers = models.ManyToManyField(Computer, related_name="carts", blank=True)
    games = models.ManyToManyField(Game, related_name="carts", blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_of_payment = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def calculate_total_price(self):
        total = sum(part.price for part in self.parts.all())
        total += sum(computer.price for computer in self.computers.all())
        total += sum(game.price for game in self.games.all())
        self.total_price = total
        self.save()

# Shop model
class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="shops")
    parts = models.ManyToManyField(Part, related_name="shops")
    computers = models.ManyToManyField(Computer, related_name="shops")
    games = models.ManyToManyField(Game, related_name="shops")
    carts = models.ManyToManyField(Cart, related_name="shops")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def total_sales(self):
        return sum(cart.total_price for cart in self.carts.all())

    def total_users(self):
        return self.users.count()

    def total_parts_in_stock(self):
        return sum(part.amount for part in self.parts.all())
