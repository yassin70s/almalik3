# Generated by Django 4.2.6 on 2023-12-08 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoreBecauseInjury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الفئة')),
            ],
            options={
                'verbose_name': 'فئة أسباب الإصابات',
                'verbose_name_plural': 'فئات أسباب الإصابات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CategoreDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الفئة')),
            ],
            options={
                'verbose_name': 'فئة مرض',
                'verbose_name_plural': 'فئات الأمراض',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CategoreInjury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الفئة')),
            ],
            options={
                'verbose_name': 'فئة إصابة',
                'verbose_name_plural': 'فئات الإصابات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CategoreProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الفئة')),
            ],
            options={
                'verbose_name': 'فئة إجراء طبي',
                'verbose_name_plural': 'فئات الإجرات الطبية',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Directorate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم المديرية')),
            ],
            options={
                'verbose_name': 'مديرية',
                'verbose_name_plural': 'المديريات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم المرض')),
                ('categore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.categoredisease', verbose_name='فئة المرض')),
            ],
            options={
                'verbose_name': 'مرض',
                'verbose_name_plural': 'أمراض',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم المحافظة')),
            ],
            options={
                'verbose_name': 'محافظة',
                'verbose_name_plural': 'المحافظات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Axi',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.user')),
                ('name', models.CharField(max_length=150, verbose_name='اسم المحور')),
            ],
            options={
                'verbose_name': 'محور',
                'verbose_name_plural': 'المحاور',
                'db_table': '',
                'managed': True,
            },
            bases=('medical.user',),
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.user')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم المستشفى')),
            ],
            options={
                'verbose_name': 'مستشفى',
                'verbose_name_plural': 'المستشفيات',
                'db_table': '',
                'managed': True,
            },
            bases=('medical.user',),
        ),
        migrations.CreateModel(
            name='SupervisorDirect',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.user')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='اسم المشرف المباشر')),
            ],
            options={
                'verbose_name': 'مشرف مباشر',
                'verbose_name_plural': 'المشرفين المباشرين',
                'db_table': '',
                'managed': True,
            },
            bases=('medical.user',),
        ),
        migrations.CreateModel(
            name='SupervisorGeneral',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.user')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='اسم المشرف العام')),
            ],
            options={
                'verbose_name': 'مشرف عام',
                'verbose_name_plural': 'المشرفين العام',
                'db_table': '',
                'managed': True,
            },
            bases=('medical.user',),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medical.user')),
                ('name', models.CharField(max_length=50, verbose_name='اسم الوحدة')),
            ],
            options={
                'verbose_name': 'وحدة',
                'verbose_name_plural': 'الوحدات',
                'db_table': '',
                'managed': True,
            },
            bases=('medical.user',),
        ),
        migrations.CreateModel(
            name='ProfileMedical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='الاسم الرباعي مع اللقب')),
                ('name_2', models.CharField(max_length=150, verbose_name='الكنية')),
                ('date_birth', models.DateField(verbose_name='تاريخ الميلاد')),
                ('number_military', models.BigIntegerField(unique=True, verbose_name='الرقم العسكري')),
                ('phone', models.BigIntegerField(verbose_name='رقم الهااتف')),
                ('directorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.directorate', verbose_name='المديرية')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.province', verbose_name='المحافظة')),
                ('axi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.axi', verbose_name='المحور')),
                ('supervisor_direct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.supervisordirect', verbose_name='المشرف المباشر')),
                ('supervisor_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.supervisorgeneral', verbose_name='المشرف العام')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.unit', verbose_name='مكان المرابطة')),
            ],
            options={
                'verbose_name': 'ProfileMedical',
                'verbose_name_plural': 'ProfileMedicals',
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الإجراء')),
                ('categore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.categoreinjury', verbose_name='فئة الإجراء الطبي')),
            ],
            options={
                'verbose_name': 'إجراء طبي',
                'verbose_name_plural': 'إجراءات طبية',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم الإصابة')),
                ('categore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.categoreinjury', verbose_name='فئة الإصابة')),
            ],
            options={
                'verbose_name': 'إصابة',
                'verbose_name_plural': 'إصابات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='directorate',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.province', verbose_name='المحافظة'),
        ),
        migrations.CreateModel(
            name='BecauseInjury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم سبب الإصابة')),
                ('categore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.categorebecauseinjury', verbose_name='فئة السبب')),
            ],
            options={
                'verbose_name': 'سبب الإصابة',
                'verbose_name_plural': 'أسباب الإصابات',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='اسم المنطقة')),
                ('directorate', models.ForeignKey(help_text='yy', on_delete=django.db.models.deletion.CASCADE, to='medical.directorate', verbose_name='المديرية')),
            ],
            options={
                'verbose_name': 'منطقة',
                'verbose_name_plural': 'المناطق',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True, verbose_name='تاريخ ووقت الدخول')),
                ('entry_type', models.CharField(blank=True, choices=[('1', 'دخول جديد'), ('2', 'عودة')], max_length=50, null=True, verbose_name='نوع الدخول')),
                ('number_notification', models.BigIntegerField(blank=True, null=True, verbose_name='رقم البلاغ')),
                ('diagnosi_type', models.CharField(blank=True, choices=[('1', 'مريض'), ('2', 'جريح'), ('3', 'شهيد')], max_length=50, null=True, verbose_name='نوع التشخيص')),
                ('result', models.CharField(blank=True, choices=[('1', 'معالجة'), ('2', 'رقود'), ('3', 'عودة'), ('4', 'تحويل'), ('5', 'وفاة')], max_length=50, null=True, verbose_name='النتيجة')),
                ('recipe', models.ImageField(blank=True, null=True, upload_to='media/images/medical/entry/recipes', verbose_name='الوصفة الطبية')),
                ('period_digg', models.IntegerField(blank=True, null=True, verbose_name='مدة الرقود')),
                ('date_back', models.DateField(blank=True, null=True, verbose_name='تاريخ العودة')),
                ('report_death', models.ImageField(blank=True, null=True, upload_to='media/images/medical/entry/report_death', verbose_name='تقرير الوفاة')),
                ('back', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical.entry', verbose_name='العودة')),
                ('becauseinjury', models.ManyToManyField(blank=True, null=True, to='medical.becauseinjury', verbose_name='أسباب الإصابة')),
                ('disease', models.ManyToManyField(blank=True, null=True, to='medical.disease', verbose_name='الأمرض')),
                ('injury', models.ManyToManyField(blank=True, null=True, to='medical.injury', verbose_name='الإصابت')),
                ('procedure', models.ManyToManyField(blank=True, null=True, to='medical.procedure', verbose_name='الإجراءات الطبية')),
                ('profilemedical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical.profilemedical', verbose_name='الملف الطبي')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical.hospital', verbose_name='المستشفى')),
                ('hospital_turn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_turn', to='medical.hospital', verbose_name='المستشفى المحول إليه')),
            ],
            options={
                'verbose_name': 'حالة دخول',
                'verbose_name_plural': 'حالات دخول',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
