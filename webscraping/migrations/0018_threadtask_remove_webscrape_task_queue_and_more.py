_I='last_modified'
_H='created_on'
_G='task_attempts'
_F='task_output'
_E='task_status'
_D='task_progress'
_C=False
_B='webscrape'
_A=True
import django.db.models.deletion
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('webscraping','0017_alter_webscrape_task_status')];operations=[migrations.CreateModel(name='ThreadTask',fields=[('id',models.BigAutoField(auto_created=_A,primary_key=_A,serialize=_C,verbose_name='ID')),('task_title',models.CharField(blank=_A,max_length=200,null=_A)),('task_run_id',models.CharField(blank=_A,max_length=50,null=_A)),(_D,models.IntegerField(default=0)),(_E,models.CharField(blank=_A,choices=[('RUNNING','Running'),('SUCCESS','Success'),('FAILED','Failed'),('QUEUED','Queued'),('STARTED','Started')],max_length=20,null=_A)),(_F,models.TextField(blank=_A,null=_A)),('task_thread_started_at',models.DateTimeField(blank=_A,null=_A)),('task_thread_stopped_at',models.DateTimeField(blank=_A,null=_A)),(_G,models.IntegerField(default=0)),(_H,models.DateTimeField(auto_now_add=_A)),(_I,models.DateTimeField(auto_now=_A))]),migrations.RemoveField(model_name=_B,name='task_queue'),migrations.RemoveField(model_name=_B,name=_H),migrations.RemoveField(model_name=_B,name='id'),migrations.RemoveField(model_name=_B,name=_I),migrations.RemoveField(model_name=_B,name=_G),migrations.RemoveField(model_name=_B,name='task_id'),migrations.RemoveField(model_name=_B,name=_F),migrations.RemoveField(model_name=_B,name=_D),migrations.RemoveField(model_name=_B,name=_E),migrations.RemoveField(model_name=_B,name='title'),migrations.AddField(model_name=_B,name='threadtask_ptr',field=models.OneToOneField(auto_created=_A,default=0,on_delete=django.db.models.deletion.CASCADE,parent_link=_A,primary_key=_A,serialize=_C,to='webscraping.threadtask'),preserve_default=_C),migrations.DeleteModel(name='WebscrapeTasksQueue')]