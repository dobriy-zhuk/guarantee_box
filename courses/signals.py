"""Define signals."""
from django.dispatch import Signal

lesson_done_signal = Signal(providing_args=[
    'duration', 'present_students_id',
    'coefficient', 'teacher', 'lesson_id',
])
