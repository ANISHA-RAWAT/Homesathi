from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_alter_property_bathrooms_alter_property_bedrooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='seeker_email',
            field=models.EmailField(blank=True, help_text='Contact email of the seeker'),
        ),
    ]