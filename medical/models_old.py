from typing import Any, Coroutine, Iterable, List, Optional
from django.db import models

# Create your models here.
class Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('posts')

class Mixin(models.Model):
    objects = Manager()
    class Meta:
        abstract = True
        managed = False
        app_label = 'posts'


class Unit(Mixin):
    name = models.CharField(("اسم الوحدة"), max_length=50)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        
        verbose_name = 'وحدة'
        verbose_name_plural = 'الوحدات'
class SupervisorGeneral(Mixin):
    name = models.CharField(("اسم المشرف العام"), max_length=50,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مشرف عام'
        verbose_name_plural = 'المشرفين العام'
    
class SupervisorDirect(Mixin):
    supervisor_general = models.ForeignKey(SupervisorGeneral, verbose_name=("المشرف العام"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المشرف المباشر"), max_length=50,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مشرف مباشر'
        verbose_name_plural = 'المشرفين المباشرين'

class Province(Mixin):
    name = models.CharField(("اسم المحافظة"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
class Directorate(Mixin):
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المديرية"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مديرية'
        verbose_name_plural = 'المديريات'
class Area(Mixin):
    """ffffff"""
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE,help_text="yy")
    name = models.CharField(("اسم المنطقة"), max_length=150,)
    def __str__(self):
        return self.name

    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'منطقة'
        verbose_name_plural = 'المناطق'
class WorkPast(Mixin):
    name = models.CharField(("اسم العمل"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'عمل سابق'
        verbose_name_plural = 'الأعمال السابقة'

class ExperienceMedical(Mixin):
    name = models.CharField(("اسم الهارة الطبية"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مهارة طبية'
        verbose_name_plural = 'المهارت الطبية'        

class Axi(Mixin):
    name = models.CharField(("اسم المحور"), max_length=150)
    supervisor_medical = models.CharField(("المشرف الصحي للمحور"), max_length=150)
    supervisor_general = models.CharField(("المشرف العسكري للمحور"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'محور'
        verbose_name_plural = 'المحاور'
class Work(Mixin):
    name = models.CharField(("اسم العمل"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'عمل'
        verbose_name_plural = 'الأعمال'


class File(Mixin):
    name = models.CharField(("الاسم الرباعي مع اللقب"), max_length=150,unique=True)
    name_2 = models.CharField(("الكنية"), max_length=150)
    date_birth = models.DateField(("تاريخ الميلاد"), auto_now=False, auto_now_add=False)
    number_military = models.BigIntegerField(("الرقم العسكري"),unique=True)
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE)
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE)
    
    supervisor_general = models.ForeignKey(SupervisorGeneral, verbose_name=("المشرف العام"), on_delete=models.CASCADE)
    supervisor_direct = models.ForeignKey(SupervisorDirect, verbose_name=("المشرف المباشر"), on_delete=models.CASCADE)
    phone = models.BigIntegerField(("رقم الهااتف"))
    unit =  models.ForeignKey(Unit, verbose_name=("مكان المرابطة"), on_delete=models.CASCADE)
    
    def __str__(self):
        return f'ملف رقم: ( {self.id} )  --  {self.name}' 
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'ملف'
        verbose_name_plural = 'الملفات'

class CategoreDisease(Mixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'فئة مرض'
        verbose_name_plural = 'فئات الأمراض'
class Disease(Mixin):
    categore = models.ForeignKey(CategoreDisease, verbose_name=("فئة المرض"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المرض"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مرض'
        verbose_name_plural = 'أمراض'
        
class CategoreInjury(Mixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'فئة إصابة'
        verbose_name_plural = 'فئات الإصابات'
class Injury(Mixin):
    categore = models.ForeignKey(CategoreInjury, verbose_name=("فئة الإصابة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم الإصابة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'إصابة'
        verbose_name_plural = 'إصابات'
        
class CategoreProcedure(Mixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'فئة إجراء طبي'
        verbose_name_plural = 'فئات الإجرات الطبية'
class Procedure(Mixin):
    categore = models.ForeignKey(CategoreInjury, verbose_name=("فئة الإجراء الطبي"), on_delete=models.CASCADE)
    name = models.CharField(("اسم الإجراء"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'إجراء طبي'
        verbose_name_plural = 'إجراءات طبية'
class CategoreBecauseInjury(Mixin):
    name = models.CharField(("اسم الفئة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'فئة أسباب الإصابات'
        verbose_name_plural = 'فئات أسباب الإصابات'
class BecauseInjury(Mixin):
    categore = models.ForeignKey(CategoreBecauseInjury, verbose_name=("فئة السبب"), on_delete=models.CASCADE)
    name = models.CharField(("اسم سبب الإصابة"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'سبب الإصابة'
        verbose_name_plural = 'أسباب الإصابات'
class Hospital(Mixin):
    name = models.CharField(("اسم المستشفى"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مستشفى'
        verbose_name_plural = 'المستشفيات'
    
class Entry(Mixin):
    hospital = models.ForeignKey(Hospital, verbose_name=("المستشفى"), on_delete=models.CASCADE,null=True,blank=True)
    fiel = models.ForeignKey(File, verbose_name=("الملف الطبي"), on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(("تاريخ ووقت الدخول"), auto_now=False, auto_now_add=False,null=True,blank=True)
    type_entry = models.CharField(("نوع الدخول"), max_length=50,choices=[('دخول جديد','دخول جديد'),('عودة','عودة')],null=True,blank=True)
    back = models.ForeignKey('posts.Entry', verbose_name=("العودة"), on_delete=models.CASCADE,null=True,blank=True)
    number_notification = models.BigIntegerField(("رقم البلاغ"),null=True,blank=True)
    type_diagnosi = models.CharField(("نوع التشخيص"), max_length=50,choices=[('مريض','مريض'),('جريح','جريح'),('شهيد','شهيد')],null=True,blank=True)
    injury = models.ManyToManyField(Injury, verbose_name=("الإصابت"),null=True,blank=True)
    disease = models.ManyToManyField(Disease, verbose_name=("الأمرض"),null=True,blank=True)
    
    because_injury = models.ManyToManyField(BecauseInjury, verbose_name=("أسباب الإصابة"),null=True,blank=True)
    
    procedure = models.ManyToManyField(Procedure, verbose_name=("الإجراءات الطبية"),null=True,blank=True)
    RESULT_CHOICES = [('معالجة','معالجة'),('رقود','رقود'),('تحويل','تحويل'),('عودة','عودة'),('وفاة','وفاة')]
    result = models.CharField(("النتيجة"), max_length=50,choices=RESULT_CHOICES,null=True,blank=True)

    recipe = models.ImageField(("الوصفة الطبية"), upload_to='images/recipes', height_field=None, width_field=None, max_length=None,null=True,blank=True)

    period_digg = models.IntegerField(("مدة الرقود"),null=True,blank=True)
    
    hospital_turn = models.ForeignKey(Hospital, verbose_name=("المستشفى المحول إليه"), on_delete=models.CASCADE,related_name='hospital_turn',null=True,blank=True)
    
    date_back = models.DateField(("تاريخ العودة"), auto_now=False, auto_now_add=False,null=True,blank=True)
    
    report_death = models.ImageField(("تقرير الوفاة"), upload_to='images/reports_death', height_field=None, width_field=None, max_length=None,null=True,blank=True)
    
    
    
    def __str__(self):
        if self.date_back:
            date = 'بتاريخ: ' + str(self.date_back)
        else:
            date = ''
        return f'{self.fiel.name} {self.result} {date}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'حالة دخول'
        verbose_name_plural = 'حالات دخول'
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.type_entry == 'دخول جديد':
            self.back = None
        elif self.type_entry == 'عودة':
            self.number_notification = None
            self.type_diagnosi = None
            
            
            #self.because_injury = None
        if self.result == 'رقود':
            self.hospital_turn = None
            self.date_back = None
            self.report_death = None
        if self.result == 'تحويل':
            self.period_digg = None
            self.date_back = None
            self.report_death = None
        if self.result == 'عودة':
            self.period_digg = None
            self.hospital_turn = None
            self.report_death = None
        if self.result == 'وفاة':
            self.period_digg = None
            self.hospital_turn = None
            self.date_back = None   
             
        
    

class People(Mixin):
    name = models.CharField(("الاسم الرباعي مع اللقب"), max_length=150)
    name_2 = models.CharField(("الكنية"), max_length=150)
    date_birth = models.DateField(("تاريخ الميلاد"), auto_now=False, auto_now_add=False)
    type_blood = models.CharField(
        ("فصيلة الدم"), 
        max_length=50,
        choices=[
            ('A+','A+'),
            ('A-','A-'),
            ('O+','O+'),
            ('O-','O-'),
            ('B+','B+'),
            ('B-','B-'),
            ('AB+','AB+'),
            ('AB-','AB-'),
        ],
        null=True,blank=True
    )
    number_national = models.BigIntegerField(("الرقم الوطني"),null=True,blank=True)
    number_military = models.BigIntegerField(("الرقم العسكري"),null=True,blank=True)
    number_necklaces = models.BigIntegerField(("رقم القلادة"),null=True,blank=True)
    number_phone = models.BigIntegerField(("رقم الهااتف"),null=True,blank=True)
    number_phone_2 = models.BigIntegerField(("رقم هاتف آخر"),null=True,blank=True)
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE,null=True,blank=True)
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE,null=True,blank=True)
    area = models.ForeignKey(Area, verbose_name=("المنطقة"), on_delete=models.CASCADE,null=True,blank=True)
    statu_marital = models.CharField(("الحالة الإجتماعية"), max_length=50,choices=[('عازب','عازب'),('متزوج','متزوج')],null=True,blank=True)
    
    date_start = models.DateField(("تاريخ الإنطلاقة"), auto_now=False, auto_now_add=False,null=True,blank=True)
    work_past = models.ManyToManyField(WorkPast, verbose_name=("الأعمال قبل الإنطلاقة"))
    work_after = models.ManyToManyField(Work, verbose_name=("الأعمال بعد الإنطلاقة"),related_name='work_after',null=True,blank=True)
    axi = models.ForeignKey(Axi, verbose_name=("مكان العمل"), on_delete=models.CASCADE,null=True,blank=True)
    work = models.ForeignKey(Work, verbose_name=("نوع العمل"), on_delete=models.CASCADE,null=True,blank=True)
    period_work = models.IntegerField(("مدة العمل"),null=True,blank=True)
    experience_medical = models.ManyToManyField(ExperienceMedical, verbose_name=("المهارات الطبية التي يتقنها"),null=True,blank=True)
    
    
    
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'فرد'
        verbose_name_plural = 'الأفراد'

class Qualification(Mixin):
    name = models.CharField(("اسم المؤهل"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مؤهل'
        verbose_name_plural = 'المؤهلات'    
class Specialty(Mixin):
    name = models.CharField(("اسم التخصص"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'تخصص'
        verbose_name_plural = 'التخصصات'    
  
class QualificationPeople(Mixin):
    people = models.ForeignKey(People, verbose_name=("الفرد"), on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, verbose_name=("المؤهل"), on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, verbose_name=("التخصص"), on_delete=models.CASCADE)
    revisionist = models.IntegerField(("المعدل"))
    def __str__(self):
        return f'{self.people.name} - {self.qualification.name}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مؤهل'
        verbose_name_plural = 'مؤهلات'

     
class Experience(Mixin):
    name = models.CharField(("اسم الخبرة أو الموهبة"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'خبرة أو موهبة'
        verbose_name_plural = 'الخبرات والمواهب'        
class ExperiencePeople(Mixin):
    people = models.ForeignKey(People, verbose_name=("الفرد"), on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, verbose_name=("الخبرة أو الموهبة"), on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.people.name} - {self.experience.name}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'خبرة أو موهبة'
        verbose_name_plural = 'الخبرات والمواهب'
        
        
class CourseType(Mixin):
    name = models.CharField(("نوع الدورة"), max_length=150)
    period = models.IntegerField(("مدة الدورة"),help_text='يرجى تحديد عدد أيام الدورة')
    total_people = models.IntegerField(("عدد الافراد"))
    
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'نوع دورة'
        verbose_name_plural = 'أنواع الدورات'    

class EvaluationType(Mixin):
    name = models.CharField(("نوع التقييم"), max_length=50)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'نوع تقييم'
        verbose_name_plural = 'أنواع التقاييم'


     
class EvaluationTypeCourse(Mixin):
    course_type = models.ForeignKey(CourseType, verbose_name=("الدورة"), on_delete=models.CASCADE)
    evaluation_type = models.ForeignKey(EvaluationType, verbose_name=("نوع التقييم"), on_delete=models.CASCADE)
    period = models.IntegerField(("فترة التقييم"),choices=[
        (1,'يومي'),
        (7,'كل اسبوع'),
        (2,'نصفي'),
        (4,'ربعي'),
        (0,'مرة واحدة'),  
    ])
    rate = models.IntegerField(("النسبة من المجموع الكلي"),max_length=100,null=True,blank=True)
    def __str__(self):
        return f'{self.course_type}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'تقييم دورة'
        verbose_name_plural = 'تقاييم الدورات'
   
class Place(Mixin):
    name = models.CharField(("اسم المكان"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'مكان'
        verbose_name_plural = 'أماكن'        



        
class Relative(Mixin):
    name = models.CharField(("اسم صلة القرابة"), max_length=150)
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'صلة قرابة'
        verbose_name_plural = 'صلات القرابة'        
class RelativePeople(Mixin):
    people = models.ForeignKey(People, verbose_name=("الفرد"), on_delete=models.CASCADE)
    relative = models.ForeignKey(Relative, verbose_name=("صلة القرابة"), on_delete=models.CASCADE)
    number_phone = models.BigIntegerField(("رقم الهاتف"))
    def __str__(self):
        return f'{self.people.name} - {self.relative.name} - {self.number_phone}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'رقم هاتف أحد الأقرباء'
        verbose_name_plural = 'أرقام هواتف الأقرباء'
 



class Course(Mixin):
    course_type = models.ForeignKey(CourseType, verbose_name=("نوع الدورة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم الدورة"), max_length=150)
    place = models.ForeignKey(Place, verbose_name=("مكانها"), on_delete=models.CASCADE)
    date_start = models.DateField(("تاريخ البدء"), auto_now=False, auto_now_add=False)
    people = models.ManyToManyField(People, verbose_name=("أفراد الدورة"),db_table="posts_coursepeople")
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        db_table = ''
        managed = False
        verbose_name = 'دورة'
        verbose_name_plural = 'دورات'

class CourseOther(Course):
    def __str__(self):
        return self.name
    class Meta(Mixin.Meta):
        
        verbose_name = 'دورة'
        verbose_name_plural = 'الدورات' 
        

    
 
class CoursePeople(Mixin):
    course = models.ForeignKey(Course, verbose_name=("الدورة"), on_delete=models.CASCADE)
    people = models.ForeignKey(People, verbose_name=("اسم الفرد"), on_delete=models.CASCADE)
    course_type = models.ForeignKey(CourseType, verbose_name=("نوع الدورة"), on_delete=models.CASCADE,null=True)
    name = models.CharField(("اسم الدورة"), max_length=150,null=True)
    place = models.ForeignKey(Place, verbose_name=("مكانها"), on_delete=models.CASCADE,null=True)
    date_start = models.DateField(("تاريخ البدء"), auto_now=False, auto_now_add=False,null=True)
    
    def __str__(self):
        return f'{self.course}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'متدرب'
        verbose_name_plural = 'المتدربين'
    
    def save(self,*args, **kwargs ):
        self.course_type = self.course.course_type
        self.name = 'yyyy'
        self.place = self.course.place
        self.date_start = self.course.date_start
        super().save(*args, **kwargs)
   
        
       
 
 
                   
class Evaluation(Mixin):
    course_people = models.ForeignKey(CoursePeople, verbose_name=("فرد الدورة"), on_delete=models.CASCADE)
    evaluation_type = models.ForeignKey(EvaluationType, verbose_name=("نوع التقييم"), on_delete=models.CASCADE)
    date = models.DateField(("تاريخ التقييم"), auto_now=False, auto_now_add=False)
    value = models.IntegerField(("النتيجة"),max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f'{self.course_people}'
    class Meta(Mixin.Meta):
        db_table = ''
        
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقاييم'
 
 