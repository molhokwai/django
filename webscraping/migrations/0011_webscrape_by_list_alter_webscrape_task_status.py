_B='webscrape'
_A=True
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('webscraping','0010_rename_task_outputs_webscrape_task_output')];operations=[migrations.AddField(model_name=_B,name='by_list',field=models.TextField(blank=_A,null=_A)),migrations.AlterField(model_name=_B,name='task_status',field=models.CharField(blank=_A,choices=[('STARTED','Started'),('RUNNING','Running'),('SUCCESS','Success'),('FAILED','Failed')],max_length=20,null=_A))]