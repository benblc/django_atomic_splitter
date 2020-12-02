from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    answer_composition = models.CharField(max_length=500)

    def __str__(self):
        return self.answer_text

class Atom(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    atom_text = models.CharField(max_length=200)
    atom_number = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text + str(self.atom_number)


