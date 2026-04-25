from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_property_facing_property_floor_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bathrooms',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedrooms',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]