from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0013_chatpromptandresponse_add_history_and_more')];operations=[migrations.CreateModel(name='LogEntry',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('level',models.CharField(max_length=20)),('message',models.TextField()),('created_at',models.DateTimeField(auto_now_add=True))],options={'verbose_name':'Log Entry','verbose_name_plural':'Log Entries'})]