import unidecode
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class CustomModelManager(models.Manager):
	"""Manager custom para os models"""
	def get_or_none(self, **obj_data):
		"""Get object or return None"""
		try:
			obj = self.get(**obj_data)
		except ObjectDoesNotExist:
			obj = None

		return obj


class CustomModel(models.Model):
	modified = models.DateTimeField(blank=True)
	created = models.DateTimeField(default=timezone.now, editable=False)

	objects = CustomModelManager()

	class Meta:
		abstract = True

	def save(self, *args, **kwargs) -> None:
		self.modified = timezone.now()
		return super().save(*args, **kwargs)


class State(CustomModel):
    name = models.CharField(max_length=30, db_index=True)
    initials = models.CharField(max_length=5, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = unidecode.unidecode(self.name).upper().strip()
        self.initials = unidecode.unidecode(self.initials).upper().strip()
        return super().save(*args, **kwargs)


class City(CustomModel):
    name = models.CharField(max_length=100, db_index=True)
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, db_index=True, null=True, blank=True, related_name='City_State'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = unidecode.unidecode(self.name).upper().strip()
        return super().save(*args, **kwargs)


class Neighborhood(CustomModel):
    name = models.CharField(max_length=100, db_index=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, db_index=True, null=True, blank=True, related_name='Neighborhood_City'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = unidecode.unidecode(self.name).upper().strip()
        return super().save(*args, **kwargs)


class Address(CustomModel):
    postal_code = models.CharField(max_length=8, null=True, blank=True)
    neighborhood = models.ForeignKey(
        Neighborhood,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
        related_name='Address_Neighborhood',
    )
    street = models.CharField(max_length=250, db_index=True, null=True, blank=True, default='Sem nome')
    number = models.CharField(max_length=50, null=True, blank=True)
    complement = models.CharField(max_length=150, null=True, blank=True, default='')

    def get_address(self):
        return f'{self.street}, {self.neighborhood}, {self.neighborhood.city} - {self.neighborhood.city.state}'

    def __str__(self):
        return self.postal_code

    def save(self, *args, **kwargs) -> None:
        self.street = unidecode.unidecode(self.street).upper().strip() if self.street else ''
        self.complement = unidecode.unidecode(self.complement).upper().strip() if self.complement else ''
        return super().save(*args, **kwargs)