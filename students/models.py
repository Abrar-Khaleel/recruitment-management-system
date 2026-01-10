from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)      # e.g., Data Structures
    code = models.CharField(max_length=20)       # e.g., CS-101
    credits = models.DecimalField(max_digits=3, decimal_places=1) # e.g., 4.0
    department = models.CharField(max_length=100) # e.g., Computer Science

    def __str__(self):
        return f"{self.name} ({self.code})"

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    # This links the Student to a Course. If the Course is deleted, the Student is also deleted (CASCADE).
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True) # Automatically set when created
    status = models.CharField(max_length=20, default='Admitted')

    def __str__(self):
        return self.full_name