_A='trainingcoursesession'
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0004_alter_trainingcoursesession_course_media_final_and_more')];operations=[migrations.AlterField(model_name=_A,name='title',field=models.CharField(max_length=255)),migrations.AlterUniqueTogether(name=_A,unique_together={('title','course')})]