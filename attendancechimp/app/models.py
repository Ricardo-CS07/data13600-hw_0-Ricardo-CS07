"""
models.py — Data model for AttendanceChimp.

AttendanceChimp is an electronic class attendance tool.  Instructors create
courses and lectures; each lecture is assigned a random QR code.  Students
photograph the QR code and upload the image.  The system decodes the QR code,
matches it to a lecture, and records the attendance.

Entities
--------
- InstructorProfile : extends Django User → instructor-specific data
- StudentProfile    : extends Django User → student-specific data
- Course            : a course taught by one instructor
- Enrollment        : junction table linking students to courses
- Lecture           : a single class meeting (has a QR-code identifier)
- QRCodeUpload      : a student's uploaded QR-code photograph
"""

from django.db import models
from django.contrib.auth.models import User

import logging
import string
import random

logger = logging.getLogger(__name__)  # set up tracking, auditing, and debugging


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

class InstructorProfile(models.Model):
    """
    Extra information for a user who teaches courses.

    Linked one-to-one to a Django User (the login account). Separate profile
    tables for instructors and students keep the two roles distinct, so each
    can get its own fields without cluttering the User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    """
    Extra information for a user who takes courses.

    Linked one-to-one to a Django User. student_id is the school's ID number
    and is unique so no two students can share one.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class Course(models.Model):
    """
    A course taught by exactly one instructor.

    meeting_schedule is free text such as "Mon/Wed 10:30-11:50".
    """
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    meeting_schedule = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class Enrollment(models.Model):
    """
    Links a student to a course (many-to-many through this table).

    One row per (student, course) pair. unique_together prevents a student
    from being enrolled in the same course twice.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} in {self.course}"


# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------

class Lecture(models.Model):
    """
    One class meeting of a course.

    qr_identifier is a unique code for this lecture. Comparing it with the
    code in an uploaded photo helps detect cheating, for example a QR code
    from a different lecture.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField()
    qr_identifier = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.course} on {self.date:%Y-%m-%d}"


# ---------------------------------------------------------------------------
# QR Code Upload
# ---------------------------------------------------------------------------

class QRCodeUpload(models.Model):
    """
    A photo of the QR code uploaded by a student as proof of attendance.

    uploaded_at is set automatically by the server so a student cannot fake
    the time. lecture is optional because it may only be matched after the
    photo is decoded. unique_together stops a student from uploading twice
    for the same lecture.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="qr_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "lecture")

    def __str__(self):
        return f"{self.student} upload at {self.uploaded_at}"


# ---------------------------------------------------------------------------
# Helper / API functions
# ---------------------------------------------------------------------------

def generate_qr_identifier(length=12):
    """Return a random string of letters and digits to use as a lecture's QR code."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
