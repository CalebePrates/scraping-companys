from django.db import models
from localflavor.br.models import BRCNPJField, BRCPFField
from scraping_companys.core.models import Address, CustomModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from scraping_companys.core.utils.tools import replace_all
from scraping_companys.scraping.list_options import CnaeChoices, SocietyTypeChoices, SubscriptionChoices


class NaturalPerson(CustomModel):
    """
    Model de Pessoa Fisica
    """
    cpf = BRCPFField(db_index=True, unique=True)
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name or self.cpf}'

    def save(self, *args, **kwargs) -> None:
        if self.cpf:
            self.cpf = replace_all(self.cpf, ['.', ',', '-', '/'], replace_all_for='')
        return super().save(*args, **kwargs)


class LegalPerson(CustomModel):
    """
    Model de Pessoa Juridica
    """
    cnpj = BRCNPJField(db_index=True, unique=True)
    fantasy_name = models.TextField(null=True, blank=True)
    corporate_name = models.TextField(null=True, blank=True)  # Razao Social
    telephone = models.TextField(null=True, blank=True)
    cell_phone = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    state_registration = models.BooleanField(default=False)  # registro estadual
    state_registration_number = models.TextField(null=True, blank=True)
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='legal_person_address'
    )
    billing_address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.SET_NULL, related_name='legal_person_billing_address'
    )
    social_capital = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=2)
    foundation_date = models.DateField(auto_now=False, null=True, blank=True)
    society_type = models.PositiveIntegerField(choices=CnaeChoices.choices, null=True, blank=True, default=1)

    def __str__(self):
        return f'{self.corporate_name or self.cnpj}'

    def save(self, *args, **kwargs) -> None:
        if self.cnpj:
            self.cnpj = replace_all(self.cnpj, ['.', ',', '-', '/'], replace_all_for='')
        return super().save(*args, **kwargs)


class Participation(CustomModel):
    """
    Model de Participacao de uma pessoa fisica ou juridica em uma empresa
    """
    partner_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    partner_id = models.PositiveIntegerField(null=True, db_index=True)
    partner = GenericForeignKey('partner_content_type', 'partner_id')  # socio (pj ou pf)
    percentage = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(
        LegalPerson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='participation_company',
        db_index=True,
    )
    legal_representative = models.BooleanField(default=False)  # representante legal
    guarantor = models.BooleanField(default=False)  # fiador
    signature = models.PositiveIntegerField(
        choices=SubscriptionChoices.choices, null=True, blank=True, default=1
    )  # tipo de assinatura
    can_operate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.company.corporate_name if self.company else ""} - {self.partner.id if self.partner else ""}'

    def is_partner_legalperson(self) -> bool:
        """O [partner] é um PJ ?"""
        if self.partner and self.partner._meta.model == LegalPerson:
            return True

        return False

    def is_partner_naturalperson(self) -> bool:
        """O [partner] é um PF ?"""
        if self.partner and self.partner._meta.model == NaturalPerson:
            return True

        return False


class CNAE(CustomModel):
    """
    Model de CNAE de uma empresa
    """
    code = models.CharField(
        max_length=10, db_index=True, null=True, blank=True, default=''
    )  # codigo do CNAE (ex: 7020-4/00)
    description = models.CharField(max_length=250, db_index=True, null=True, blank=True, default='')
    type = models.PositiveIntegerField(choices=SocietyTypeChoices.choices, null=True, blank=True, default=1)
    company = models.ForeignKey(
        LegalPerson, null=True, blank=True, on_delete=models.SET_NULL, related_name='cnae_company', db_index=True
    )  # empresa
