from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def get_category_label(category_key):
    """
    Returns a display label for a Listing Category.
    """
    for key, value in Listing.CATEGORY_CHOICES:
        if key == category_key:
            return value

def get_city_label(city_key):
    for key, value in Listing.CITY_CHOICES:
        if key == city_key:
            return value


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "Listing",
        related_name="watchlist",
        blank=True
    )
  

class Listing(models.Model):
    ACTIVE = "A"
    CLOSED = "C"

    FEMALE = "F"
    MALE = "M"
    GENERAL = "G"
   
    DOGS = "D"
    CATS = "C"
    GENERAL = "G"
    
    GENERAL ="G"
    SHIVAJINAGAR = "S"
    KOTHRUD = "U"
    VIMANNAGAR = "V"
    AUNDH = "A"
    BANERBALEWADI = "B"
    PASHAN = "P"
    KONDHWA = "K"
    HADAPSAR = "H"
    KHARADI = "I"
    VISHRANTWADI = "R"
    BAVDHAN = "M"
    BIBVEWADI = "O"
    DHANORI = "D"
    KATRAJ = "T"
    WAGHOLI = "L"
    YERWADA = "Y"
    WANOWRIE = "W"
    NANDED = "N"
   

    
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (CLOSED, "Closed")
    )
    GENDER_CHOICES = (
        (GENERAL, "No Category"),
        (FEMALE, "Female"),
        (MALE, "Male")
    )
    
    
    CATEGORY_CHOICES = (
        (GENERAL, "No Category"),
        (DOGS, "Dogs"),
        (CATS, "Cats")
        
    )
    CITY_CHOICES = (
        (GENERAL , "No Category"),
        (SHIVAJINAGAR , "Shivajinagar"),
        (KOTHRUD , "Kothrud"),
        (VIMANNAGAR , "Viman nagar"),
        (AUNDH , "Aundh"),
        (BANERBALEWADI , "Baner"),
        (PASHAN , "Pashan"),
        (KONDHWA , "Kondhwa"),
        (HADAPSAR, "Hadapsar"),
        (KHARADI , "Kharadi"),
        (VISHRANTWADI , "Vishrantwadi"),
        (BAVDHAN , "Bavdhan"),
        (BIBVEWADI , "Bibvewadi"),
        (DHANORI, "Dhanori"),
        (KATRAJ , "Katraj"),
        (WAGHOLI , "Wagholi"),
        (YERWADA , "Yerwada"),
        (WANOWRIE , "Wanowrie"),
        (NANDED , "Nanded")

    )


    image_url = models.URLField(max_length=200, blank=True)
    headline = models.CharField(max_length=64)
    breed = models.CharField(max_length=64, default="")
    weight = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    age = models.IntegerField(null=True)
    contact = models.IntegerField(null=True)
    city = models.CharField(max_length=1, choices=CITY_CHOICES, default=GENERAL)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENERAL)
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listing_owner"
    )
    
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES,
                                default=GENERAL)
    min_bid = models.DecimalField(
        max_digits=6, decimal_places=0, default=0,
        validators=[MinValueValidator(0,
                                      message="Number of days must be greater than 0.")])
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default="A")
    listing_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.headline} ({self.owner.username})"

    def top_bid(self):
        """
        Returns the top bid for this listing
        or None if there are no bids.
        """
        try:
            amount = 0
            top_bid = None
            for bid in self.bid_listing.all():
                if int(bid.bid) >= int(amount):
                    amount = bid.bid
                    top_bid = bid
            return top_bid
        except ValueError:
            return None


class Bid(models.Model):
    bid = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bid_owner"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bid_listing",
        default=1
    )
    bid_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bid}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comment_listing"
    )
    headline = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_owner",
        default=1
    )
    comment_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['comment_date']

    def __str__(self):
        return f"{self.headline} ({self.owner.username})"

class Article_list(models.Model):
    #id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=500)
    headline=models.CharField(max_length=256)
    link = models.TextField(max_length=500)
    cos_sim=models.FloatField(null=True)


    def __str__(self):
        return self.headline
        
        

