from django.db import models
from django.contrib.auth.models import User


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    avatar = models.ImageField(upload_to="profiles/avatars/", blank=True, null=True)
    social_media = models.JSONField(blank=True, null=True)  # Store social media links as JSON
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_profiles_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "01 | Member"
        verbose_name_plural = "01 | Members"


class MemberBodyProfile(models.Model):
    member = models.OneToOneField('MemberProfile', on_delete=models.CASCADE, related_name="body_profile")
    # Basic info
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Common Upper Body
    neck = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bicep = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    arm_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Armpit to wrist
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Shoulder to wrist
    wrist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    back_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    torso_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Chest/Bust depending on gender
    chest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bust = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Midsection
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    front_rise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    crotch_depth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Lower Body
    hips = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    knee = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    calf = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ankle = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    inseam = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Women-only (optional fields)
    skirt_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dress_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.user.username}'s Body Profile"
    
    class Meta:
        verbose_name = "01 | Member measurement"
        verbose_name_plural = "01 | Members measurements"

