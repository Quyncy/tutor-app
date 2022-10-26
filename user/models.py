from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# class UserManager(BaseUserManager):
#     def create_user(self, email, username, first_name, last_name, role, password, **other_fields):
#         user = self.model(
#             email=email,
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             role=role,
#             **other_fields,
#         )
#         user.set_password(password)
#         user.save(using= self._db)
#         return user

#     def create_superuser(self, email, username, first_name, last_name, role, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_admin', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must be assigned to is_staff = True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must be addigned to is_superuser = True.')

#         return self.create_user(email, username, first_name, last_name, password, role, **other_fields)


###############
# Beim hinzufügen der Daten wird die rolle als admin zugewiesen, wenn
# die Daten bearbeitet werden, dann wird es wieder korrigiert
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    base_user = Role.ADMIN

    # Welche Rolle hat der User
    role = models.CharField(("Role"), max_length=10, choices=Role.choices, default=base_user)

    def save(self, *args, **kwargs):
        if not self.id:
             self.role = self.base_user
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
        return self.studentmore

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
        ('WS', 'Wintersemester'),   # WS wird in die Datenbank gespeichert und Wintersemester wird User angezeigt
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

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)


# Weitere Informationen über Studenten zB. Arbeitsstunden
class StudentMore(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    kurs = models.OneToOneField(Module, on_delete=models.CASCADE, null=True)
    work_hours = models.FloatField()
    anzahl_korrekturen = models.IntegerField()

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)
