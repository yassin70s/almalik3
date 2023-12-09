from django.db import models
from main.models import MainMixin,UserMixin
from django.urls import reverse
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType 
#from django.utils.translation import gettext_lazy as _


from django.utils.translation import gettext as _


class User(UserMixin):
    pass
    



class Hospital(User):
    name = models.CharField(("اسم المستشفى"), max_length=150,unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مستشفى'
        verbose_name_plural = 'المستشفيات'
    


class Axi(User):
    name = models.CharField(("اسم المحور"), max_length=150)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'محور'
        verbose_name_plural = 'المحاور'
class Unit(User):
    name = models.CharField(("اسم الوحدة"), max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'وحدة'
        verbose_name_plural = 'الوحدات'
class SupervisorGeneral(User):
    name = models.CharField(("اسم المشرف العام"), max_length=50,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مشرف عام'
        verbose_name_plural = 'المشرفين العام'
    
class SupervisorDirect(User):
    name = models.CharField(("اسم المشرف المباشر"), max_length=50,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مشرف مباشر'
        verbose_name_plural = 'المشرفين المباشرين'

class Province(MainMixin):
    name = models.CharField(("اسم المحافظة"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
class Directorate(MainMixin):
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المديرية"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مديرية'
        verbose_name_plural = 'المديريات'
class Area(MainMixin):
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE,help_text="yy")
    name = models.CharField(("اسم المنطقة"), max_length=150,)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'منطقة'
        verbose_name_plural = 'المناطق'

class ProfileMedical(MainMixin):
    name = models.CharField(("الاسم الرباعي مع اللقب"), max_length=150,unique=True)
    name_2 = models.CharField(("الكنية"), max_length=150)
    date_birth = models.DateField(("تاريخ الميلاد"), auto_now=False, auto_now_add=False)
    number_military = models.BigIntegerField(("الرقم العسكري"),unique=True)
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE)
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE)
    
    supervisor_general = models.ForeignKey(SupervisorGeneral, verbose_name=("المشرف العام"), on_delete=models.CASCADE)
    supervisor_direct = models.ForeignKey(SupervisorDirect, verbose_name=("المشرف المباشر"), on_delete=models.CASCADE)
    phone = models.BigIntegerField(("رقم الهااتف"))
    axi =  models.ForeignKey(Axi, verbose_name=("المحور"), on_delete=models.CASCADE)
    unit =  models.ForeignKey(Unit, verbose_name=("مكان المرابطة"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("ProfileMedical")
        verbose_name_plural = _("ProfileMedicals")

    def __str__(self):
        return self.name


class CategoreDisease(MainMixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'فئة مرض'
        verbose_name_plural = 'فئات الأمراض'
class Disease(MainMixin):
    categore = models.ForeignKey(CategoreDisease, verbose_name=("فئة المرض"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المرض"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مرض'
        verbose_name_plural = 'أمراض'
        
class CategoreInjury(MainMixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'فئة إصابة'
        verbose_name_plural = 'فئات الإصابات'
class Injury(MainMixin):
    categore = models.ForeignKey(CategoreInjury, verbose_name=("فئة الإصابة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم الإصابة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'إصابة'
        verbose_name_plural = 'إصابات'
        
class CategoreProcedure(MainMixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'فئة إجراء طبي'
        verbose_name_plural = 'فئات الإجرات الطبية'
class Procedure(MainMixin):
    categore = models.ForeignKey(CategoreInjury, verbose_name=("فئة الإجراء الطبي"), on_delete=models.CASCADE)
    name = models.CharField(("اسم الإجراء"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'إجراء طبي'
        verbose_name_plural = 'إجراءات طبية'
class CategoreBecauseInjury(MainMixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'فئة أسباب الإصابات'
        verbose_name_plural = 'فئات أسباب الإصابات'
class BecauseInjury(MainMixin):
    categore = models.ForeignKey(CategoreBecauseInjury, verbose_name=("فئة السبب"), on_delete=models.CASCADE)
    name = models.CharField(("اسم سبب الإصابة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'سبب الإصابة'
        verbose_name_plural = 'أسباب الإصابات'




class Entry(MainMixin):

    is_view = True
    is_report = True



    hospital = models.ForeignKey(Hospital, verbose_name=("المستشفى"), on_delete=models.CASCADE,null=True,blank=True)
    profilemedical = models.ForeignKey(ProfileMedical,  verbose_name=("الملف الطبي"), on_delete=models.CASCADE,null=True,blank=True)
    datetime = models.DateTimeField(("تاريخ ووقت الدخول"), auto_now=False, auto_now_add=False,null=True,blank=True)
    
    class EntryTypes:
        NEW = '1'
        BACK = "2"
        choices = [
            (NEW,'دخول جديد'),
            (BACK,'عودة'),
        ]
    entry_type = models.CharField(("نوع الدخول"), max_length=50,choices=EntryTypes.choices,null=True,blank=True)
    
    back = models.ForeignKey('Entry', verbose_name=("العودة"), on_delete=models.CASCADE,null=True,blank=True)
    number_notification = models.BigIntegerField(("رقم البلاغ"),null=True,blank=True)

    
    class DiagnosiTypes:
        DISEASE = '1'
        INJURY = '2'
        DEATH = '3'
        choices = [
            (DISEASE,'مريض'),
            (INJURY,'جريح'),
            (DEATH,'شهيد')
        ]
    diagnosi_type = models.CharField(("نوع التشخيص"), max_length=50,choices=DiagnosiTypes.choices,null=True,blank=True)
    injury = models.ManyToManyField(Injury, verbose_name=("الإصابت"),null=True,blank=True)
    disease = models.ManyToManyField(Disease, verbose_name=("الأمرض"),null=True,blank=True)
    
    becauseinjury = models.ManyToManyField(BecauseInjury, verbose_name=("أسباب الإصابة"),null=True,blank=True)
    
    procedure = models.ManyToManyField(Procedure, verbose_name=("الإجراءات الطبية"),null=True,blank=True)
    class Results:
        TREATMENT = "1"
        DIGG = "2"
        BACK = "3"
        TURN = "4"
        DEATH = "5"
        choices = [
            (TREATMENT,'معالجة'),
            (DIGG,'رقود'),
            (BACK,'عودة'),
            (TURN,'تحويل'),
            (DEATH,'وفاة')
        ]

    result = models.CharField(("النتيجة"), max_length=50,choices=Results.choices,null=True,blank=True)

    recipe = models.ImageField(("الوصفة الطبية"), upload_to='media/images/medical/entry/recipes', height_field=None, width_field=None, max_length=None,null=True,blank=True)

    period_digg = models.IntegerField(("مدة الرقود"),null=True,blank=True)
    
    hospital_turn = models.ForeignKey(Hospital, verbose_name=("المستشفى المحول إليه"), on_delete=models.CASCADE,related_name='hospital_turn',null=True,blank=True)
    
    date_back = models.DateField(("تاريخ العودة"), auto_now=False, auto_now_add=False,null=True,blank=True)
    
    report_death = models.ImageField(("تقرير الوفاة"), upload_to='media/images/medical/entry/report_death', height_field=None, width_field=None, max_length=None,null=True,blank=True)
    
    is_cleaned = False
    is_blank = True
    
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'حالة دخول'
        verbose_name_plural = 'حالات دخول'
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    
   

    
            
        

        