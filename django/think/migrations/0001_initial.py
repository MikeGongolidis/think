# Generated by Django 4.0.3 on 2022-03-12 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('alien_form', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.CharField(max_length=300)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='think.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='think.user')),
            ],
        ),
    ]
