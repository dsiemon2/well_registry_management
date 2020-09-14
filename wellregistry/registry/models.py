"""
Well Registry ORM object.
"""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from smart_selects.db_fields import ChainedForeignKey



class AgencyLookup(models.Model):
    """Model definition for the agency table, lookup only"""
    agency_cd = models.CharField(max_length=50, unique=True)
    agency_nm = models.CharField(max_length=150, blank=True, null=True)
    agency_med = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'agency'
        ordering = ['agency_nm']

    def __str__(self):
        return self.agency_nm


class AltitudeDatumLookup(models.Model):
    """Model definition for the altitude_datum table, lookup only"""
    adatum_cd = models.CharField(max_length=10, unique=True)
    adatum_desc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'altitude_datum'
        ordering = ['adatum_cd']

    def __str__(self):
        return self.adatum_cd


class CountryLookup(models.Model):
    """Model definition for the country table, lookup only"""
    country_cd = models.CharField(unique=True, max_length=2)
    country_nm = models.CharField(max_length=48)

    class Meta:
        db_table = 'country'
        ordering = ['country_nm']

    def __str__(self):
        return self.country_nm


class CountyLookup(models.Model):
    """Model definition for the county table, lookup only"""
    country_cd = models.ForeignKey('CountryLookup', on_delete=models.PROTECT, db_column='country_cd',
                                   to_field='country_cd')
    state_id = models.ForeignKey('StateLookup', on_delete=models.PROTECT, db_column='state_id')
    county_cd = models.CharField(max_length=3)
    county_nm = models.CharField(max_length=48)

    class Meta:
        db_table = 'county'
        ordering = ['county_nm']
        unique_together = (('country_cd', 'state_id', 'county_cd'),)

    def __str__(self):
        return self.county_nm


class HorizontalDatumLookup(models.Model):
    """Model definition for the horizontal_datum table, lookup only"""
    hdatum_cd = models.CharField(max_length=10, unique=True)
    hdatum_desc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'horizontal_datum'
        ordering = ['hdatum_cd']

    def __str__(self):
        return self.hdatum_cd


class NatAqfrLookup(models.Model):
    """Model definition for the nat_aqfr table, lookup only"""
    nat_aqfr_cd = models.CharField(unique=True, max_length=10)
    nat_aqfr_desc = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        db_table = 'nat_aqfr'
        ordering = ['nat_aqfr_desc']

    def __str__(self):
        return self.nat_aqfr_desc


class StateLookup(models.Model):
    """Model definition for the state table, lookup only"""
    country_cd = models.ForeignKey('CountryLookup', on_delete=models.PROTECT, db_column='country_cd',
                                   to_field='country_cd')
    state_cd = models.CharField(max_length=2)
    state_nm = models.CharField(max_length=53)

    class Meta:
        db_table = 'state'
        ordering = ['state_nm']
        unique_together = (('country_cd', 'state_cd'),)

    def __str__(self):
        return self.state_nm


class UnitsLookup(models.Model):
    """Model definition for the units_dim table, lookup only"""
    unit_id = models.IntegerField(unique=True)
    unit_desc = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'units'
        ordering = ['unit_desc']

    def __str__(self):
        return self.unit_desc


WELL_TYPES = [('Surveillance', 'Surveillance'), ('Trend', 'Trend'), ('Special', 'Special')]
WELL_CHARACTERISTICS = [('Background', 'Background'),
                        ('Suspected/Anticipated Changes', 'Suspected/Anticipated Changes'),
                        ('Known Changes', 'Known Changes')]
WELL_PURPOSES = [('Dedicated Monitoring/Observation', 'Dedicated Monitoring/Observation'), ('Other', 'Other')]

non_blank_validator = RegexValidator(
    r'\S[\s\S]*',
    message='Field must not be blank')

class MonitoringLocation(models.Model):
    """
    Django Registry Model.

    # python manage.py makemigrations and migrate
    """
    display_flag = models.BooleanField(default=False, verbose_name='Display Site?')

    agency = models.ForeignKey(AgencyLookup, on_delete=models.PROTECT, db_column='agency_cd', null=True,
                               to_field='agency_cd')
    site_no = models.CharField(max_length=16)
    site_name = models.CharField(max_length=300)

    country = models.ForeignKey(CountryLookup, on_delete=models.PROTECT, db_column='country_cd',
                                null=True, blank=True, to_field='country_cd')
    state = ChainedForeignKey(StateLookup,
                              chained_field="country",
                              chained_model_field="country_cd",
                              show_all=False,
                              auto_choose=True,
                              sort=True,
                              on_delete=models.PROTECT, db_column='state_id', null=True)
    county = ChainedForeignKey(CountyLookup,
                               chained_field="state",
                               chained_model_field="state_id",
                               show_all=False,
                               auto_choose=True,
                               sort=True,
                               on_delete=models.PROTECT,
                               db_column='county_id', null=True)

    dec_lat_va = models.DecimalField(max_digits=11, decimal_places=8, null=True,
                                     verbose_name='Latitude(decimal degrees)')
    dec_long_va = models.DecimalField(max_digits=11, decimal_places=8, null=True,
                                      verbose_name='Longitude(decimal degrees)')
    horizontal_datum = models.ForeignKey(HorizontalDatumLookup, on_delete=models.PROTECT,
                                         db_column='horizontal_datum_cd', null=True,
                                         to_field='hdatum_cd')
    horz_method = models.CharField(max_length=300, blank=True, verbose_name='Lat/Long method')
    horz_acy = models.CharField(max_length=300, blank=True, verbose_name='Lat/Long accuracy')

    alt_va = models.DecimalField(max_digits=10, decimal_places=6, null=True,
                                 verbose_name='Altitude')
    altitude_units = models.ForeignKey(UnitsLookup, on_delete=models.PROTECT, db_column='altitude_units',
                                       to_field='unit_id', null=True)
    altitude_datum = models.ForeignKey(AltitudeDatumLookup, on_delete=models.PROTECT,
                                       db_column='altitude_datum_cd', null=True,
                                       to_field='adatum_cd')
    alt_method = models.CharField(max_length=300, blank=True, verbose_name='Altitude method')
    alt_acy = models.CharField(max_length=300, blank=True, verbose_name='Altitude accuracy')

    well_depth = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    well_depth_units = models.ForeignKey(UnitsLookup, related_name='+', db_column='well_depth_units',
                                         on_delete=models.PROTECT, to_field='unit_id', null=True, blank=True)

    nat_aqfr = models.ForeignKey(NatAqfrLookup, on_delete=models.PROTECT, db_column='nat_aqfr_cd',
                                 to_field='nat_aqfr_cd', null=True, verbose_name='National aquifer')
    local_aquifer_name = models.CharField(max_length=100, blank=True)

    site_type = models.CharField(max_length=10, choices=[('WELL', 'Well'), ('SPRING', 'Spring')])
    aqfr_type = models.CharField(max_length=10, blank=True, db_column='aqfr_char',
                                 choices=[('CONFINED', 'Confined'), ('UNCONFINED', 'Unconfined')],
                                 verbose_name='Aquifer type')

    wl_sn_flag = models.BooleanField(default=False, verbose_name='In WL sub-network?')
    wl_network_name = models.CharField(max_length=50, blank=True, db_column='wl_sys_name',
                                       verbose_name='WL network name')
    wl_baseline_flag = models.BooleanField(default=False, verbose_name='WL baseline?')
    wl_well_type = models.CharField(max_length=32, blank=True, choices=WELL_TYPES,
                                    verbose_name='WL well type')
    wl_well_chars = models.CharField(max_length=32, blank=True, choices=WELL_CHARACTERISTICS,
                                     verbose_name='WL well characteristics')
    wl_well_purpose = models.CharField(max_length=32, blank=True, choices=WELL_PURPOSES,
                                       verbose_name='WL well purpose')
    wl_well_purpose_notes = models.CharField(max_length=4000, blank=True, verbose_name='WL well purpose notes')

    qw_sn_flag = models.BooleanField(default=False, verbose_name='In QW sub-network?')
    qw_network_name = models.CharField(max_length=50, blank=True, db_column='qw_sys_name',
                                       verbose_name='QW network name')
    qw_baseline_flag = models.BooleanField(default=False, verbose_name='QW baseline?')
    qw_well_type = models.CharField(max_length=32, blank=True, choices=WELL_TYPES,
                                    verbose_name='QW well type')
    qw_well_chars = models.CharField(max_length=32, blank=True, choices=WELL_CHARACTERISTICS,
                                     verbose_name='QW well characteristics')
    qw_well_purpose = models.CharField(max_length=32, blank=True, choices=WELL_PURPOSES,
                                       verbose_name='QW well purpose')
    qw_well_purpose_notes = models.CharField(max_length=4000, blank=True,
                                             verbose_name='QW well purpose notes')

    link = models.CharField(max_length=500, blank=True)

    insert_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, editable=False,
                                    related_name='+')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, editable=False,
                                    related_name='+')

    insert_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (('site_no', 'agency'),)

    def __str__(self):
        """Default string."""
        str_rep = f'{self.agency}:{self.site_no}'
        return str_rep
