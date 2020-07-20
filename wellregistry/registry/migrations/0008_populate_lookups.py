# The below suppresses pylint message: Module name "*" doesn't conform to snake_case naming style
# pylint: disable-msg=C0103
# pylint: disable-msg=W0613
# Enable check for the rest of the file
# pylint: enable-msg=C0103
"""
Load lookup tables using data migrations as
described at https://docs.djangoproject.com/en/3.0/topics/migrations/#data-migrations
"""
# Generated by Django 3.0.8 on 2020-07-15 21:12
import csv
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import migrations


def load_country_lookups(apps, schema_editor):
    """
    Load country lookup table from data in a CSV.

    """
    country_lookup = apps.get_model('registry', 'CountryLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/country.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header row
        for country_cd, country_nm in csvreader:
            country = country_lookup(
                country_cd=country_cd,
                country_nm=country_nm
            )
            country.save()


def load_state_lookups(apps, schema_editor):
    """
    Load state lookup table from data in a CSV.
    Foreign keys are set using records in the country lookup table.

    """
    country_lookup = apps.get_model('registry', 'CountryLookup')
    state_lookup = apps.get_model('registry', 'StateLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/state.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for country_cd, state_cd, state_nm in csvreader:
            country = country_lookup.objects.get(country_cd=country_cd)
            state = state_lookup(
                country_cd=country,
                state_cd=state_cd,
                state_nm=state_nm
            )
            state.save()


def load_county_lookups(apps, schema_editor):
    """
    Load county lookup table from data in a CSV.
    Foreign keys are set using records in the country and state lookup tables.

    """
    country_lookup = apps.get_model('registry', 'CountryLookup')
    state_lookup = apps.get_model('registry', 'StateLookup')
    county_lookup = apps.get_model('registry', 'CountyLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/county.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for country_cd, state_cd, county_cd, county_nm in csvreader:
            country = country_lookup.objects.get(country_cd=country_cd)
            state = state_lookup.objects.get(state_cd=state_cd, country_cd=country_cd)
            county = county_lookup(
                country_cd=country,
                state_id=state,
                county_cd=county_cd,
                county_nm=county_nm
            )
            county.save()


def load_national_aquifer_lookups(apps, schema_editor):
    """
    Load national aquifer lookup table from data in a CSV.

    """
    aquifer_lookup = apps.get_model('registry', 'NatAqfrLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/nat_aqfr.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for nat_aqfr_cd, nat_aqfr_desc in csvreader:
            aquifer = aquifer_lookup(
                nat_aqfr_cd=nat_aqfr_cd,
                nat_aqfr_desc=nat_aqfr_desc
            )
            aquifer.save()


def load_altitude_datum_lookups(apps, schema_editor):
    """
    Load altitude datum lookup table from data in a CSV.

    """
    altitude_datum_lookup = apps.get_model('registry', 'AltitudeDatumLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/altitude_datums.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for adatum_cd, adatum_desc, _ in csvreader:
            altitude_datum = altitude_datum_lookup(
                adatum_cd=adatum_cd,
                adatum_desc=adatum_desc
            )
            altitude_datum.save()


def load_horizontal_datum_lookups(apps, schema_editor):
    """
    Load horizontal datum lookup table from data in a CSV.

    """
    horizontal_datum_lookup = apps.get_model('registry', 'HorizontalDatumLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/horizontal_datums.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for hdatum_cd, hdatum_desc in csvreader:
            horizontal_datum = horizontal_datum_lookup(
                hdatum_cd=hdatum_cd,
                hdatum_desc=hdatum_desc
            )
            horizontal_datum.save()


def load_unit_lookups(apps, schema_editor):
    """
    Load unit lookup table from data in a CSV.

    """
    unit_lookup = apps.get_model('registry', 'UnitsLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/units.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for unit_id, _, unit_desc in csvreader:
            unit = unit_lookup(
                unit_id=unit_id,
                unit_desc=unit_desc
            )
            unit.save()


def load_agency_lookups(apps, schema_editor):
    """
    Load agency lookup table from data in a CSV.

    """
    agency_lookup = apps.get_model('registry', 'AgencyLookup')
    data_src = os.path.join(settings.BASE_DIR, 'registry/migrations/initial_data/agency.csv')
    with default_storage.open(data_src, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for agency_cd, agency_nm, agency_med in csvreader:
            agency = agency_lookup(
                agency_cd=agency_cd,
                agency_nm=agency_nm,
                agency_med=agency_med
            )
            agency.save()


class Migration(migrations.Migration):
    """
    Insert initial data into lookup tables.

    """

    dependencies = [
        ('registry', '0007_registry_flags_to_boolean'),
    ]

    operations = [
        migrations.RunPython(load_country_lookups),
        migrations.RunPython(load_state_lookups),
        migrations.RunPython(load_county_lookups),
        migrations.RunPython(load_national_aquifer_lookups),
        migrations.RunPython(load_altitude_datum_lookups),
        migrations.RunPython(load_horizontal_datum_lookups),
        migrations.RunPython(load_unit_lookups),
        migrations.RunPython(load_agency_lookups)
    ]
