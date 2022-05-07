# Create your models here.
from django.db import models

class IMG(models.Model):
    img = models.ImageField(upload_to='custom/')
    def __str__(self):
        return self.img.name
    class Meta:
        db_table = 'img'
        ordering = ['id']
        verbose_name = 'IMGTable'
        verbose_name_plural = verbose_name

class REC(models.Model):
    referring_expression = models.CharField(max_length=255, verbose_name='referring_expression')
    # image = models.ImageField(verbose_name='image', upload_to='custom/')
    img = models.ForeignKey(IMG, on_delete=models.CASCADE)
    result = models.CharField(max_length=255, verbose_name='result', null=True, blank=True)
    result_image = models.ImageField(verbose_name='result_image', null=True, blank=True)

    def __str__(self):
        return self.referring_expression

    class Meta:
        db_table = 'rec'
        ordering = ['id']
        verbose_name = 'RECTable'
        verbose_name_plural = verbose_name

class VQA(models.Model):
    question = models.CharField(max_length=255, verbose_name='question')
    img = models.ForeignKey(IMG, on_delete=models.CASCADE)
    # image = models.ImageField(verbose_name='image', upload_to='custom/')
    answer = models.CharField(max_length=255, verbose_name='answer', null=True, blank=True)
    rec = models.ForeignKey(REC, related_name='vqas', on_delete=models.CASCADE)
    def __str__(self):
        return '%s: %s'.format(self.rec.referring_expression, self.question)
    class Meta:
        db_table = 'vqa'
        ordering = ['id']
        verbose_name = 'VQATable'
        verbose_name_plural = verbose_name
