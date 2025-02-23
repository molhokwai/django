_A=True
import django.db.models.deletion
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('webscraping','0012_webscrape_parent')];operations=[migrations.CreateModel(name='WebscrapeTasksQueue',fields=[('id',models.BigAutoField(auto_created=_A,primary_key=_A,serialize=False,verbose_name='ID')),('title',models.CharField(blank=_A,default='Default task queue',max_length=200,null=_A)),('description',models.TextField(blank=_A,default='\n            To:\n            - Add tasks to queue\n            - Check and limit to the number or max concurrent tasks from settings\n            The next task in the line is picked up when the previous is completed.\n        ',null=_A)),('created_on',models.DateTimeField(auto_now_add=_A)),('last_modified',models.DateTimeField(auto_now=_A))]),migrations.AddField(model_name='webscrape',name='task_queue',field=models.ForeignKey(blank=_A,editable=False,null=_A,on_delete=django.db.models.deletion.DO_NOTHING,related_name='tasksqueue_webscrapes',to='webscraping.webscrapetasksqueue'))]