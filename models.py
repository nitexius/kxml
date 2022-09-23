from django.db import models
from .alrm import alrm, stations


class klogic(models.Model):
    '''xml klogic ИС Диспетчеризация ХО'''
    gm = models.CharField(max_length=100, verbose_name='Код ГМ', unique=True)
    xml = models.FileField(upload_to='media/klogic')
    station_id = models.CharField(max_length=100, default='0', verbose_name='Индетификатор станции', choices=stations)

    class Meta:
        ordering = ['gm']
        verbose_name = 'Klogic XML'
        verbose_name_plural = 'Klogic XML'

    def __str__(self):
        return self.gm


class Shift(models.Model):
    '''Смещение адресов контроллеров в xml klogic'''
    gm = models.CharField(max_length=100, verbose_name='Код ГМ', unique=True)
    txt = models.FileField(upload_to='media/shift')

    class Meta:
        ordering = ['gm']

    def __str__(self):
        return self.gm


class alarms(models.Model):
    '''xml Аварии ИС Диспетчеризация ХО'''
    gm = models.CharField(max_length=100, verbose_name='Код ГМ', unique=True)
    xml = models.FileField(upload_to='media/alarms')

    class Meta:
        ordering = ['gm']
        verbose_name = 'Alarm'
        verbose_name_plural = 'Alarms'

    def __str__(self):
        return self.gm


class klogger(models.Model):
    '''xml klogger (BDTP) ИС Диспетчеризация ХО'''
    gm = models.CharField(max_length=100, verbose_name='Код ГМ', unique=True)
    xml = models.FileField(upload_to='media/klogger')

    class Meta:
        ordering = ['gm']
        verbose_name = 'Klogger XML'
        verbose_name_plural = 'Klogger XML'

    def __str__(self):
        return self.gm


class Cutout(models.Model):
    '''Уставки для продуктов (Контроль уставок)'''
    name = models.CharField(max_length=100, verbose_name='Наименование продукта', unique=True)
    cutout = models.IntegerField(default=-50, verbose_name='Уставка')

    class Meta:
        ordering = ['name']
        verbose_name = 'Контроль уставок'
        verbose_name_plural = 'Контроль уставок'

    @classmethod
    def get_products_name(cls):
        products = Cutout.objects.all()
        return products

    def __str__(self):
        return self.name


class history_attr(models.Model):
    '''Служебные символы в названии переменной'''
    h_attr = models.CharField(max_length=30)

    class Meta:
        ordering = ['h_attr']
        verbose_name = '[H_   ]'
        verbose_name_plural = '[H_   ]'

    @classmethod
    def get_h_attrs(cls):
        result = []
        for h in cls.objects.all():
            attr = h.h_attr
            attr = attr.replace('"', "")
            result.append(attr)
        return result

    def __str__(self):
        return self.h_attr


class GoodTags(models.Model):
    '''Используемые переменные'''

    Name = models.CharField(max_length=100, verbose_name='Название переменной', unique=True)
    alarm_id = models.CharField(max_length=100, default='None', verbose_name='Код аварии', choices=alrm)
    bdtp = models.BooleanField(default=False, verbose_name='Архивируемая переменная')
    noffl = models.BooleanField(default=False, verbose_name='ФБ noffl')

    class Meta:
        ordering = ['Name']
        verbose_name = 'Используемая переменная'
        verbose_name_plural = 'Используемые переменные'

    @classmethod
    def get_GoodTagsall(cls):
        GoodTag = GoodTags.objects.all()
        return GoodTag

    @classmethod
    def get_noffl_tags(cls):
        nofflTag = GoodTags.objects.filter(noffl='1')
        return nofflTag

    @classmethod
    def get_bdtp_tags(cls):
        bdtpTag = GoodTags.objects.filter(bdtp='1')
        return bdtpTag

    @classmethod
    def get_central_tag(cls):
        centralTag = GoodTags.objects.filter(alarm_id='central')
        return centralTag

    @classmethod
    def get_id(cls):
        id = GoodTags.objects.filter(alarm_id='central')
        return id

    def __str__(self):
        return self.Name


class BadTags(models.Model):
    '''Удаляемые переменные'''
    Name = models.CharField(max_length=100, verbose_name='Название переменной', unique=True)

    class Meta:
        ordering = ['Name']
        verbose_name = 'Удаляемая переменная'
        verbose_name_plural = 'Удаляемые переменные'

    @classmethod
    def get_BadTagsall(cls):
        BadTag = BadTags.objects.all()
        return BadTag

    def __str__(self):
        return self.Name


class NewTags(models.Model):
    '''Новые переменные, отсутсвующие в GoodTags, BadTags'''
    Name = models.CharField(max_length=100, verbose_name='Название переменной')
    Controller = models.CharField(max_length=100, default="", verbose_name='Название контроллера')
    alarm_id = models.CharField(max_length=100, default='None', verbose_name='Код аварии', choices=alrm)
    bdtp = models.BooleanField(default=False, verbose_name='Архивируемая переменная')
    noffl = models.BooleanField(default=False, verbose_name='ФБ noffl')

    class Meta:
        verbose_name = 'Новая переменная'
        verbose_name_plural = 'Новые переменные'

    @classmethod
    def delete_NewTagsall(cls):
        NewTag = NewTags.objects.all()
        NewTag.delete()

    def __str__(self):
        return self.Name
