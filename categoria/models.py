from django.db import models


class Categoria(models.Model):
    nome_cat = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.nome_cat
