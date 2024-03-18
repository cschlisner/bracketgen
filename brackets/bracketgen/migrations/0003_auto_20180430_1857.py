# Generated by Django 2.0.4 on 2018-05-01 00:57

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('bracketgen', '0002_tournament_user_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('index', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('winner'), nulls_last=False)],
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=80)),
                ('index', models.SmallIntegerField()),
                ('matches', models.ManyToManyField(related_name='round', to='bracketgen.Match')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='rank',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='losses',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='match',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='wins',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='password',
            field=models.CharField(blank=True, help_text='Enter a tournament password', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='winners',
            field=models.ManyToManyField(to='bracketgen.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(related_name='matches', to='bracketgen.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_won', to='bracketgen.Player'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='rounds',
            field=models.ManyToManyField(blank=True, related_name='tournament', to='bracketgen.Round'),
        ),
    ]