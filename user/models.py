from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password, **extrafields):
        if not email:
            raise ValueError("Benutzer benötigt eine Email")
        if not password:
            raise ValueError("Benutzer benötigt ein Password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extrafields,
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, first_name, last_name, password, **extrafields):
        if not email:
            raise ValueError("Benutzer benötigt eine Email")
        if not password:
            raise ValueError("Benutzer benötigt ein Password")

        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)
        extrafields.setdefault('is_staff', True)

        user = self.create_user(
            email,
            first_name,
            last_name,
            password,
            **extrafields,
        )
        user.save(using=self.db)

        return user


###############
# Beim hinzufügen der Daten wird die Rolle als admin zugewiesen
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        TUTOR = "TUTOR", 'Tutor'
        KURSLEITER = "KURSLEITER", 'Kursleiter'

    base_user = Role.ADMIN

    # Welche Rolle hat der User
    role = models.CharField(("Rolle"), max_length=10, choices=Role.choices, default=base_user)
    vorname = models.CharField(max_length=255, blank=True)
    nachname = models.CharField(max_length=255, blank=True)
    email_confirmed = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['vorname', 'nachname',]

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Benutzer"

    def save(self, *args, **kwargs):
        if self.id:
            self.role = self.base_user
            print(self.role)
        return super().save(*args, **kwargs)


class KursleiterManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.KURSLEITER)


class TutorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TUTOR)


class Tutor(User):
    """Tutoren im System"""
    base_user = User.Role.TUTOR

    tutor = TutorManager()

    @property
    def more(self):
        return self.tutorprofile

    class Meta:
        verbose_name_plural = "Tutoren"
        proxy = True

    def welcome(self):
        return "Nur für Tutoren"


class Kursleiter(User):
    """Kursleiter im System"""
    base_user = User.Role.KURSLEITER

    kursleiter = KursleiterManager()

    @property
    def more(self):
        return self.kursleiterprofile

    class Meta:
        verbose_name_plural = "Kursleiter"
        proxy = True

    def welcome(self):
        return "Nur für Kursleiter"


class Dozent(models.Model):
    """Dozenten im System"""
    TITEL_CHOICES = [
        ('Prof.','Prof.'),
        ('Dr.', 'Dr.'),
    ]

    title = models.CharField(max_length=5, choices = TITEL_CHOICES, default='Prof.')  # Auswahl Prof., Dr., Wiss. Mitarbeiter
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Dozenten"

    def __str__(self):
        return f"{self.title} {self.vorname} {self.nachname}"


class Kurs(models.Model):
    """Kurse im System"""
    # field_of_study = Naturwissenschaften, Rechtswissenschaft
    kurs_name = models.CharField(max_length=50)
    beschreibung = models.TextField(blank=True, null=True)
    dozent = models.ForeignKey(Dozent, on_delete=models.CASCADE)
    kursleiter = models.ForeignKey(Kursleiter, on_delete=models.CASCADE, blank=True, null=True)

    SEMESTER_CHOICES = [
        ('WS', 'Wintersemester'),   # 'WS'/'SS' wird in die Datenbank gespeichert und Wintersemester oder Sommersemester wird User angezeigt
        ('SS', 'Sommersemester'),
    ]

    semester = models.CharField(
        max_length=3,
        choices=SEMESTER_CHOICES,
        default='',
    )

    class Meta:
        verbose_name_plural = "Kurse"

    def __str__(self):
        return f"{self.kurs_name}"


class KursleiterProfile(models.Model):
    user = models.OneToOneField(Kursleiter, on_delete=models.CASCADE)
    kurs_name = models.OneToOneField(Kurs, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kursleiter Profile"

    def __str__(self):
        return f"{self.user.email}"


# Weitere Informationen über Studenten zB. Arbeitsstunden
class TutorProfile(models.Model):
    user = models.OneToOneField(Tutor, on_delete=models.CASCADE)
    kurs = models.OneToOneField(Kurs, on_delete=models.CASCADE, null=True)
    arbeitsstunden = models.FloatField(default=0)
    anzahl_korrekturen = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Tutoren Profile"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# wartet auf ein Signal, sobald ein User gespeichert wird ein StudentProfile oder TeacherProfile erstellt
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "KURSLEITER":
        KursleiterProfile.objects.create(user=instance)
    if created and instance.role == "TUTOR":
        TutorProfile.objects.create(user=instance)

# wartet auf ein Signal, sobald ein Student gespeichert wird ein StudentProfile oder TeacherProfile erstellt
@receiver(post_save, sender=Tutor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TUTOR":
        TutorProfile.objects.create(user=instance)

# wartet auf ein Signal, sobald ein Teacher gespeichert wird ein StudentProfile oder TeacherProfile erstellt
@receiver(post_save, sender=Kursleiter)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "KURSLEITER":
        # hier könnte Email versendet werden
        KursleiterProfile.objects.create(user=instance)

