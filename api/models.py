from django.db import models


class Photo(models.Model):

    PERSON = 'PS'
    CAT = 'CA'
    PHOTO = [
        (PERSON, 'Person'),
        (CAT, 'Cat'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=2, choices=PHOTO, default=PERSON)
    is_real = models.BooleanField()
    photo_url = models.ImageField(upload_to="img", unique=True)

    def __str__(self):
        return str(self.id)

