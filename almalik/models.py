from django.db import models
from main.models import MainMixin,GroupMixin,UserMixin


from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRel,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
#from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
import os
from django.conf import settings
import tarfile
BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT
# Create your models here.


class NoticeSetMixin(models.Model):


    class Meta:
        abstract = True
    activity_name = None
    user = None
    content = None
    def save(self,*args, **kwargs):
        #self.user = self.project.user
        super().save(*args, **kwargs)
        if not self.activity_name:
            self.activity_name = "تم"
        if not self.content:
            self.content = f"{self.activity_name}"
        if not self.user:
            self.user = self.project.user
        

        NoticeUser.objects.create(
            notice= Notice.objects.create(
                content = self.content
            ),
            user = self.user,
        )

class Management(MainMixin):
    name = models.CharField(_("name"), max_length=50)
    

    class Meta:
        verbose_name = _("Management")
        verbose_name_plural = _("Managements")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Management_detail", kwargs={"pk": self.pk})

class Department(MainMixin):
    management = models.ForeignKey(Management, verbose_name=_("management"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    #users = models.ManyToManyField(User, verbose_name=_("users"))
    #jobs = models.ManyToManyField(Job, verbose_name=_("jobs"))

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})




class BlanceType(MainMixin):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("BlanceType")
        verbose_name_plural = _("BlanceTypes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("BlanceType_detail", kwargs={"pk": self.pk})



class Balance(MainMixin):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    balance_type = models.ForeignKey(BlanceType, verbose_name=_("balance_type"), on_delete=models.CASCADE)
    #statu = models.CharField(_("statu"), max_length=50,choices=[("1","مراجعة"),("0","ملغي")],default="1")

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return f"{self.user} | {self.balance_type}"

    def get_absolute_url(self):
        return reverse("Balance_detail", kwargs={"pk": self.pk})

class ReceiveType(MainMixin):
    name = models.CharField(_("name"), max_length=50)
    account = models.CharField(_("account"), max_length=50)
    

    class Meta:
        verbose_name = _("ReceiveType")
        verbose_name_plural = _("ReceiveTypes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ReceiveType_detail", kwargs={"pk": self.pk})


class BalanceReceive(MainMixin):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE,null=True,blank=True)
    balance = models.ForeignKey(Balance, verbose_name=_("balance"), on_delete=models.CASCADE,null=True,blank=True)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    receive_type = models.ForeignKey(ReceiveType, verbose_name=_("receive_type"), on_delete=models.CASCADE)
    number = models.BigIntegerField(_("number"))
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2)
    statu = models.CharField(_("statu"), max_length=50,choices=[("1","مراجعة"),("OK","تم"),("0","ملغي")],default="1")


    class Meta:
        verbose_name = _("BalanceReceive")
        verbose_name_plural = _("BalanceReceives")
    def save(self,*args, **kwargs):
        #self.user = self.project.user
        super().save(*args, **kwargs)
        
        

        
    

    def get_absolute_url(self):
        return reverse("BalanceReceive_detail", kwargs={"pk": self.pk})




class Project(MainMixin):
    to_project = models.ForeignKey("Project", verbose_name=_("project"), on_delete=models.CASCADE,null=True,blank=True,related_name="project_to_project")
    department = models.ForeignKey(Department, verbose_name=_("نوع المشروع"), on_delete=models.CASCADE)
    #service = models.ForeignKey(Service, verbose_name=_("service"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(_("اسم المشروع"), max_length=50)
    price_min = models.DecimalField(_("اقل سعر"), max_digits=7, decimal_places=2)
    price_max = models.DecimalField(_("أعلى سعر"), max_digits=7, decimal_places=2)
    days = models.SmallIntegerField(_("المدة"))
    #jobs = models.ManyToManyField(Job, verbose_name=_("jobs"))
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)


    statu = models.CharField(_("حالة المشروع"), max_length=50,choices=[("مراجعة","مراجعة"),("عرض","عرض"),("جاري","جاري"),("تم","تم"),("معلق","معلق"),("ملغي","ملغي"),("مرفوض","مرفوض")],default="مراجعة")
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    is_view = True
    
class Job(MainMixin):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    def __str__(self):
        return self.name

    

class Offer(MainMixin):
    PATH_DIR = os.path.join(MEDIA_ROOT,"offers")
    #department = models.ForeignKey(Department, verbose_name=_("department"), on_delete=models.CASCADE)
    #user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    name = models.CharField(_("اسم العرض"), max_length=50)
    #price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    #jobs = models.ManyToManyField(Job, verbose_name=_("jobs"))
    file = models.FileField(_("file"), upload_to="almalik/offers/", max_length=100,null=True,blank=True)
    path = models.FilePathField(_("path"), path=PATH_DIR, allow_folders=True, max_length=100,null=True,blank=True)

    

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")

    def __str__(self):
        return f"{self.name}"

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        path = os.path.join(self.PATH_DIR,f"{self.id}")
        os.makedirs(path,exist_ok=True)
        Offer.objects.filter(id=self.id).update(path=path)

class OfferJob(MainMixin):
    offer = models.ForeignKey(Offer, verbose_name=_("offer"), on_delete=models.CASCADE)
    job = models.ForeignKey(Job, verbose_name=_("job"), on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    period = models.SmallIntegerField(_("period"))

    class Meta:
        verbose_name = _("OfferJob")
        verbose_name_plural = _("OfferJobs")

    def __str__(self):
        return f"{self.offer} | {self.job} | {self.price} | {self.period}"

    def get_absolute_url(self):
        return reverse("OfferJob_detail", kwargs={"pk": self.pk})



class ProjectUnAccepted(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    detail = models.TextField(_("detail"))

    class Meta:
        verbose_name = _("ProjectUnAccepted")
        verbose_name_plural = _("ProjectUnAccepteds")

    activity_name = "تم رفض"

    def __str__(self):
        return self.detail

    def get_absolute_url(self):
        return reverse("ProjectUnAccepted_detail", kwargs={"pk": self.pk})

class ProjectStop(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    detail = models.TextField(_("detail"))
    

    class Meta:
        verbose_name = _("ProjectStop")
        verbose_name_plural = _("ProjectStops")

    activity_name = "تم إيقاف"

    def __str__(self):
        return self.detail

    def get_absolute_url(self):
        return reverse("ProjectStop_detail", kwargs={"pk": self.pk})



class ProjectOffer(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, verbose_name=_("offer"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    
    

    class Meta:
        verbose_name = _("ProjectOffer")
        verbose_name_plural = _("ProjectOffers")


    activity_name = "تم عرض"
    

    def get_absolute_url(self):
        return reverse("ProjectOffer_detail", kwargs={"pk": self.pk})




class ProjectStart(NoticeSetMixin,MainMixin):
    PROJECTS_DIR = os.path.join(MEDIA_ROOT,"projects")

    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    projectoffer = models.ForeignKey(ProjectOffer, verbose_name=_("projectoffer"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    period = models.SmallIntegerField(_("period"))
    #offer = models.ForeignKey(Offer, verbose_name=_("offer"), on_delete=models.CASCADE)
    path = models.FilePathField(_("path"), path=PROJECTS_DIR, max_length=100,allow_folders=True,null=True,blank=True)
   
    class Meta:
        verbose_name = _("ProjectStart")
        verbose_name_plural = _("ProjectStarts")
    activity_name = "تم البدء"
    user = ""
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        path = os.path.join(self.PROJECTS_DIR,f"{self.project.id}")
        
        
        BalanceSpend.objects.update_or_create(
            content_type = ContentType.objects.get_for_model(self),
            object_id = self.id,
            user = self.project.user,
            balance = Balance.objects.get(user=self.project.user),
            amount = self.price, 
        )
        if not self.path:
            os.makedirs(path,exist_ok=True)
            import shutil
            shutil.copytree(self.projectoffer.offer.path,path,dirs_exist_ok=True)
            for file,text in [("ID.py",f"id={self.project.id}")]:
                file_path = os.path.join(path,f"{file}")
                with open(file_path,"w") as fi:
                    fi.write(text)
            
            ProjectStart.objects.filter(id=self.id).update(path=path)
        
        
import tarfile



class ProjectJob(MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    projectstart = models.ForeignKey(ProjectStart, verbose_name=_("projectstart"), on_delete=models.CASCADE)
    #project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    job = models.ForeignKey(Job, verbose_name=_("job"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ProjectJob")
        verbose_name_plural = _("ProjectJobs")

    def __str__(self):
        return self.job

    def get_absolute_url(self):
        return reverse("ProjectJob_detail", kwargs={"pk": self.pk})

class ProjectEnd(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    projectstart = models.ForeignKey(ProjectStart, verbose_name=_("projectstart"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    file = models.FileField(_("file"), upload_to="media/projects", max_length=100)
    class Meta:
        verbose_name = _("ProjectEnd")
        verbose_name_plural = _("ProjectEnds")

    activity_name = "تم إنجاز"

class ProjectApp(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("ProjectApp")
        verbose_name_plural = _("ProjectApps")

    def __str__(self):
        return self.name

    activity_name = "تم انشاء"


class ProjectDdownload(MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    projectend = models.ForeignKey(ProjectEnd, verbose_name=_("projectend"), on_delete=models.CASCADE)
    datetime = models.DateTimeField(_("datetime"), auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE,null=True,blank=True)

    

    class Meta:
        verbose_name = _("ProjectDdownload")
        verbose_name_plural = _("ProjectDdownloads")

    
class ProjectCode(NoticeSetMixin,MainMixin):
    project = models.ForeignKey(Project, verbose_name=_("project"), on_delete=models.CASCADE)
    projectend = models.ForeignKey(ProjectEnd, verbose_name=_("projectend"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    code = models.CharField(_("code"), max_length=50)
    period_days = models.IntegerField(_("period_days"))
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2)
    name = models.CharField(_("name"), max_length=50)
    detail = models.TextField(_("detail"))


    

    class Meta:
        verbose_name = _("ProjectCode")
        verbose_name_plural = _("ProjectCodes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProjectCode_detail", kwargs={"pk": self.pk})



class BalanceSpend(NoticeSetMixin,MainMixin):
    content_type = models.ForeignKey(ContentType, verbose_name=_("content_type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("object_id"))
    content_object = GenericForeignKey()
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, verbose_name=_("balance"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2)
    statu = models.CharField(_("statu"), max_length=50,choices=[("1","مراجعة"),("0","ملغي")],default="1")


    

    class Meta:
        verbose_name = _("BalanceSpend")
        verbose_name_plural = _("BalanceSpends")

    activity_name = "تم الدفع"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

   



class Image(MainMixin):
    image = models.ImageField(_("image"), upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    content_type = models.ForeignKey(ContentType, verbose_name=_("content_type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("object_id"))
    content_object = GenericForeignKey()
    
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")



class File(MainMixin):
    file = models.FileField(_("file"), upload_to="media/file/", max_length=100)
    content_type = models.ForeignKey(ContentType, verbose_name=_("content_type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("object_id"))
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")



class UserContact(MainMixin):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE,related_name="related_usercontact_user")
    contact = models.ForeignKey(User, verbose_name=_("contact"), on_delete=models.CASCADE,related_name="related_usercontact_contact")
    
    admin = True

    class Meta:
        verbose_name = _("UserContact")
        verbose_name_plural = _("UserContacts")

    def __str__(self):
        return f"{self.user} | {self.contact}"

    def get_absolute_url(self):
        return reverse("UserContact_detail", kwargs={"pk": self.pk})


class Chat(MainMixin):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    datetime_change = models.DateTimeField(_("datetime_change"), auto_now=True, auto_now_add=False)
    content_type = models.ForeignKey(ContentType, verbose_name=_("content_type"), on_delete=models.CASCADE,null=True,blank=True)
    object_id = models.PositiveIntegerField(_("object_id"),null=True,blank=True)
    content_object = GenericForeignKey()
    to_user = models.ForeignKey(User, verbose_name=_("to_user"), on_delete=models.CASCADE,related_name="related_chat_to_user")
    link_chat = models.ForeignKey("Chat", verbose_name=_("link_chat"), on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(_("text"),null=True,blank=True)
    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return f"{self.user} | {self.to_user} | {self.text}"

    is_view = True
    

class ChatImage(MainMixin):
    chat = models.ForeignKey(Chat, verbose_name=_("chat"), on_delete=models.CASCADE)
    image = models.ImageField(_("image"), upload_to="account/chat/images", height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = _("ChatImage")
        verbose_name_plural = _("ChatImages")

    

    def get_absolute_url(self):
        return reverse("ChatImage_detail", kwargs={"pk": self.pk})

class ChatVideo(MainMixin):
    chat = models.ForeignKey(Chat, verbose_name=_("chat"), on_delete=models.CASCADE)
    video = models.FileField(_("video"), upload_to="account/chat/videos", max_length=100)

    class Meta:
        verbose_name = _("ChatVideo")
        verbose_name_plural = _("ChatVideos")

    

    def get_absolute_url(self):
        return reverse("ChatVideo_detail", kwargs={"pk": self.pk})


class ChatFile(MainMixin):
    chat = models.ForeignKey(Chat, verbose_name=_("chat"), on_delete=models.CASCADE)
    file = models.FileField(_("file"), upload_to="account/chat/file", max_length=100)
    

    class Meta:
        verbose_name = _("ChatFile")
        verbose_name_plural = _("ChatFiles")

    

    def get_absolute_url(self):
        return reverse("ChatFile_detail", kwargs={"pk": self.pk})

class Comment(MainMixin):
    text = models.CharField(_("text"), max_length=50)
    
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text




class Notice(MainMixin):
    datetime = models.DateTimeField(_("datetime_add"), auto_now=False, auto_now_add=True)
    content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")

    def __str__(self):
        return f"{self.content}"

    def get_absolute_url(self):
        return reverse("Notice_detail", kwargs={"pk": self.pk})

class NoticeUser(MainMixin):
    notice = models.ForeignKey(Notice, verbose_name=_("notice"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    is_view = models.BooleanField(_("is_view"),default=False)
    is_notice = models.BooleanField(_("is_notice"),default=False)
    class Meta:
        verbose_name = _("NoticeUser")
        verbose_name_plural = _("NoticeUsers")

    def __str__(self):
        return f"{self.notice} | {self.user} | {self.is_view}"

    def get_absolute_url(self):
        return reverse("NoticeUser_detail", kwargs={"pk": self.pk})

class Profile(MainMixin):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    datebirth = models.DateField(_("datebirth"), auto_now=False, auto_now_add=False,null=True,blank=True)
    profession = models.CharField(_("profession"), max_length=50,null=True,blank=True)
    country = models.CharField(_("country"), max_length=50,null=True,blank=True)
    address = models.CharField(_("address"), max_length=50,null=True,blank=True)
    location = models.CharField(_("location"), max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})

class Setting(MainMixin):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    choose_theme = models.CharField(_("choose_theme"), max_length=50,choices=[("dark","dark"),("ligth","ligth")],default="dark")


    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("Setting_detail", kwargs={"pk": self.pk})

