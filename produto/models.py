from django.db import models
from django.utils.text import slugify
from categoria.models import Categoria
from django.conf import settings
import os
from PIL import Image


class Produto(models.Model):
    nome_generico = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    marca = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_generico
        

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    descricao_var = models.TextField(max_length=255)
    preco = models.FloatField()
    desconto_var = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    imagem = models.ImageField(upload_to='produto_img/%Y/%m/0')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            tema = str(self.produto.nome_generico) + str(self.nome)
            slug = f'{slugify(tema)}'
            self.slug = slug
        
        super().save(*args, **kwargs)
        
        self.resize_img(self.imagem.name)

    @staticmethod
    def resize_img(img_name):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size

        if width <= 800:
            img.close()
            return
        
        max_height = round((800 * height) / width)

        new_img = img.resize((800, max_height), Image.LANCZOS)
        new_img.save(
            img_path,
            optimize=True,
            quality=70
        )
        new_img.close()

    def __str__(self):
        return self.nome or self.produto.nome_generico
    
    @property
    def imagemURL(self):
        try:
            url = self.imagem.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


class Banner(models.Model):
    diferencial = models.CharField(max_length=255)
    img_banner = models.ImageField(upload_to='banner_img/%Y/%m/0')
    tipo_link = models.CharField(
        default='',
        max_length=1,
        choices=(
            ('P', 'Por produto'),
            ('M', 'Por marca'),
            ('C', 'Por categoria'),
            ('H', 'Por campanha')
        )
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_img_banner(self.img_banner.name)

    @staticmethod
    def resize_img_banner(img_banner_name):
        img_path_b = os.path.join(settings.MEDIA_ROOT, img_banner_name)
        img_banner = Image.open(img_path_b)
        new_img_b = img_banner.resize((900, 350), Image.LANCZOS)
        new_img_b.save(
            img_path_b,
            optimize=True,
            quality=70
        )
        new_img_b.close()


