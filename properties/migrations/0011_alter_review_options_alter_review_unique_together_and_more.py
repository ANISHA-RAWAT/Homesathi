import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_inquiry_seeker_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name': 'Property Review'},
        ),
        # ── Add new fields FIRST ──────────────────────────────────────────
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, default='', help_text='Share your experience with this property and its owner'),
        ),
        migrations.AddField(
            model_name='review',
            name='owner_rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, help_text='1-5 stars for the owner'),
        ),
        migrations.AddField(
            model_name='review',
            name='property_rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, help_text='1-5 stars for the property'),
        ),
        migrations.AddField(
            model_name='review',
            name='related_property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='properties.property'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        # ── Remove old fields ─────────────────────────────────────────────
        migrations.RemoveField(
            model_name='review',
            name='email',
        ),
        migrations.RemoveField(
            model_name='review',
            name='message',
        ),
        migrations.RemoveField(
            model_name='review',
            name='name',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        # ── AlterUniqueTogether AFTER both fields exist ───────────────────
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('related_property', 'reviewer')},
        ),
        # ── Inquiry / InquiryReply / Property field updates ───────────────
        migrations.AlterField(
            model_name='inquiry',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='seeker_email',
            field=models.EmailField(blank=True, default='', help_text='Contact email of the seeker', max_length=254),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='seeker_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='seeker_phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='inquiryreply',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='inquiryreply',
            name='sender_role',
            field=models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], default='buyer', max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='property',
            name='bhk',
            field=models.CharField(blank=True, choices=[('1rk', '1 RK'), ('1bhk', '1 BHK'), ('2bhk', '2 BHK'), ('3bhk', '3 BHK'), ('4bhk', '4 BHK'), ('5bhk+', '5 BHK+')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='property',
            name='construction_status',
            field=models.CharField(blank=True, choices=[('new_launch', 'New Launch'), ('under_construction', 'Under Construction'), ('ready_to_move', 'Ready To Move')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='property',
            name='facing',
            field=models.CharField(blank=True, choices=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South'), ('north_east', 'North-East'), ('north_west', 'North-West'), ('south_east', 'South-East'), ('south_west', 'South-West')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='floor_number',
            field=models.CharField(blank=True, default='', help_text='e.g. 3, Ground, Basement', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='flooring',
            field=models.CharField(blank=True, choices=[('marble', 'Marble'), ('vitrified_tiles', 'Vitrified Tiles'), ('ceramic_tiles', 'Ceramic Tiles'), ('wooden', 'Wooden'), ('granite', 'Granite'), ('mosaic', 'Mosaic'), ('normal_tiles', 'Normal Tiles')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='furnishing',
            field=models.CharField(blank=True, choices=[('furnished', 'Furnished'), ('semi_furnished', 'Semi Furnished'), ('unfurnished', 'Unfurnished')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='key_facilities',
            field=models.TextField(blank=True, default='', help_text='Comma-separated facilities, e.g. 24hr Security, CCTV'),
        ),
        migrations.AlterField(
            model_name='property',
            name='key_highlights',
            field=models.TextField(blank=True, default='', help_text='Why should someone consider this property?'),
        ),
        migrations.AlterField(
            model_name='property',
            name='listing_type',
            field=models.CharField(choices=[('rent', 'For Rent'), ('sell', 'For Sale'), ('pg', 'PG / Co-living')], default='rent', max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='location',
            field=models.CharField(blank=True, default='', help_text='City, Area or Full Address', max_length=200),
        ),
        migrations.AlterField(
            model_name='property',
            name='pg_for',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('any', 'Any')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='pg_notice_period',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='posted_by',
            field=models.CharField(blank=True, choices=[('owner', 'Owner'), ('builder', 'Builder'), ('dealer', 'Dealer'), ('featured_dealer', 'Featured Dealer')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='preferred_tenants',
            field=models.CharField(blank=True, choices=[('family', 'Family'), ('single_man', 'Single Man'), ('single_woman', 'Single Woman'), ('company_lease', 'Company Lease'), ('any', 'Any')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='property',
            name='project_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_age',
            field=models.CharField(blank=True, choices=[('0-1', '0-1 Years'), ('1-5', '1-5 Years'), ('5-10', '5-10 Years'), ('10-20', '10-20 Years'), ('20+', '20+ Years')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_category',
            field=models.CharField(blank=True, choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('pg', 'PG / Co-living')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_ownership',
            field=models.CharField(blank=True, choices=[('freehold', 'Freehold'), ('leasehold', 'Leasehold'), ('cooperative', 'Co-operative Society'), ('power_of_attorney', 'Power of Attorney')], default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('flat_apartment', 'Flat / Apartment'), ('independent_house_villa', 'Independent House / Villa'), ('builder_floor', 'Independent / Builder Floor'), ('plot_land_res', 'Plot / Land'), ('studio_1rk', '1 RK / Studio Apartment'), ('farmhouse', 'Farmhouse'), ('office', 'Office Space'), ('retail', 'Retail / Shop'), ('plot_land_com', 'Commercial Plot / Land'), ('storage', 'Storage / Warehouse'), ('dance_studio', 'Dance / Fitness Studio'), ('coworking', 'Co-working Space'), ('showroom', 'Showroom'), ('restaurant_cafe', 'Restaurant / Café'), ('pg_hostel', 'PG / Hostel')], default='flat_apartment', max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='purchase_type',
            field=models.CharField(blank=True, choices=[('resale', 'Resale'), ('new_booking', 'New Booking')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='rera_id',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='RERA ID'),
        ),
        migrations.AlterField(
            model_name='property',
            name='seller_type',
            field=models.CharField(blank=True, choices=[('pg_owner', 'PG Owner'), ('owner', 'Owner'), ('builder', 'Builder'), ('dealer', 'Dealer')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='state',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='property',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('new_property', 'New Property'), ('resale', 'Resale')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='water_source',
            field=models.CharField(blank=True, choices=[('borewell', 'Borewell'), ('municipal', 'Municipal Corporation'), ('both', 'Both (Borewell + Municipal)')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='property',
            name='width_of_facing_road',
            field=models.CharField(blank=True, default='', help_text='e.g. 30 ft, 9 metres', max_length=30),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        # ── Create PropertyView model ─────────────────────────────────────
        migrations.CreateModel(
            name='PropertyView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_views', to='properties.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Property View',
                'unique_together': {('property', 'user')},
            },
        ),
    ]