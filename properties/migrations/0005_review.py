from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_inquiryreply_is_rented'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])),
                ('message', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]