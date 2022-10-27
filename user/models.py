from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


# class UserManager(BaseUserManager):
#     def create_user(self, email,password, **extrafields):
#         user = self.model(
#             email=self.normalize_email(email),
#             **extrafields,
#         )
#         user.set_password(password)
#         user.save(using=self.db)
#         return user

#     def create_superuser(self, username, email, first_name, last_name, password, **extrafields):
#         self.create_user(
#             email,
#             password,
#         )
#         self.is_admin=True
#         self.is_staff=True
#         self.is_active=True
#         user.save(using=self.db)
#         return user


###############
# Beim hinzufügen der Daten wird die rolle als admin zugewiesen, wenn
# die Daten bearbeitet werden, dann wird es wieder korrigiert
class User(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    base_user = Role.ADMIN

    # Welche Rolle hat der User
    role = models.CharField(("Role"), max_length=10, choices=Role.choices)
    name = models.CharField(blank=True, max_length=255)



    def save(self, *args, **kwargs):
        if self.pk:
            self.role = self.base_user
            print("Im pk")
        return super().save(*args, **kwargs)


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)

class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT

    student = StudentManager()

    @property
    def more(self):
        return self.studentprofile

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


class Teacher(User):
    base_role = User.Role.TEACHER
    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for teachers"


class Dozent(models.Model):
    """Dozenten im System"""
    TITEL_CHOICES = [
        ('Prof','Prof.'),
        ('Dr', 'Dr.'),
        ('WM', 'Wissenschaftliche/r Mitarbeiter/in')
    ]

    titel = models.CharField(max_length=5, choices = TITEL_CHOICES, default='Dr')  # Auswahl Prof., Dr., Wiss. Mitarbeiter
    name = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.nachname}"


class Module(models.Model):
    module_name = models.CharField(max_length=50)
    description = models.TextField(default='')
    dozent = models.ForeignKey(Dozent, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    SEMESTER_CHOICES = [
        ('WS', 'Wintersemester'),   # 'WS'/'SS' wird in die Datenbank gespeichert und Wintersemester oder Sommersemester wird User angezeigt
        ('SS', 'Sommersemester'),
    ]

    semester = models.CharField(
        max_length=3,
        choices=SEMESTER_CHOICES,
        default='',
    )
    def __str__(self):
        return f"{self.module_name}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.user.email}"

# wartet auf ein Signal, sobald ein User gespeichert wird ein StudentProfile oder TeacherProfile erstellt
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.create(user=instance)
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)

# Weitere Informationen über Studenten zB. Arbeitsstunden
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)
    kurs = models.OneToOneField(Module, on_delete=models.CASCADE, null=True)
    work_hours = models.FloatField()
    anzahl_korrekturen = models.IntegerField()

    def __str__(self):
        return self.user.first_name

