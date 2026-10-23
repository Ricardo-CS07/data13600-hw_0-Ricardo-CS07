# LLM: ChatGPT
# Prompt:
# Write a Django models.py for an app called AttendanceChimp, which tracks class attendance via QR codes.
#
# Steps/Things needed for the table:
# Users are students and instructors (two roles), using separate profile tables linked to Django's User: InstructorProfile and StudentProfile.
# Each course has one instructor. Students can enroll in multiple courses, so use an Enrollment table.
# Lectures are individual class meetings, each connceted with a course, with a date and a QR identifier.
# QRCodeUpload: photos uploaded by students, each associated with a student and (optionally) a lecture.

from django.db import models
from django.contrib.auth.models import User


class InstructorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    students = models.ManyToManyField(
        StudentProfile,
        through="Enrollment",
        related_name="courses"
    )

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} - {self.course}"


class Lecture(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lectures"
    )
    date = models.DateField()
    qr_identifier = models.UUIDField(
        unique=True,
        editable=False
    )

    def __str__(self):
        return f"{self.course} - {self.date}"


class QRCodeUpload(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="qr_uploads"
    )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="qr_uploads"
    )
    photo = models.ImageField(upload_to="qr_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.uploaded_at}"
