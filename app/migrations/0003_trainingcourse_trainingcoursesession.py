_S='last_modified'
_R='created_on'
_Q='date_published'
_P='status_text'
_O='☴'
_N='WHEN_FREE'
_M='✗'
_L='STOPPED'
_K='✓'
_J='COMPLETED'
_I='|'
_H='ON_HOLD'
_G='⌛'
_F='IN_VALIDATION'
_E='~'
_D='IN_PROGRESS'
_C='↗'
_B='TODO'
_A=True
import django.db.models.deletion
from django.db import migrations,models
class Migration(migrations.Migration):dependencies=[('app','0002_alter_book_country')];operations=[migrations.CreateModel(name='TrainingCourse',fields=[('id',models.BigAutoField(auto_created=_A,primary_key=_A,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=255,unique=_A)),('slug',models.SlugField(max_length=200,unique=_A)),(_P,models.TextField()),(_Q,models.DateTimeField(null=_A)),(_R,models.DateTimeField(auto_now_add=_A)),(_S,models.DateTimeField(auto_now=_A))]),migrations.CreateModel(name='TrainingCourseSession',fields=[('id',models.BigAutoField(auto_created=_A,primary_key=_A,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=255,unique=_A)),('slug',models.SlugField(max_length=200,unique=_A)),(_P,models.TextField()),('preparation',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('course_media_raw',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('course_media_final',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('course_media_validated',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('implemented_in_app',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('ready_for_whats_and_gram',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),('in_sales_funnel',models.CharField(choices=[(_B,_C),(_D,_E),(_F,_G),(_H,_I),(_J,_K),(_L,_M),(_N,_O)],max_length=50)),(_Q,models.DateTimeField(null=_A)),(_R,models.DateTimeField(auto_now_add=_A)),(_S,models.DateTimeField(auto_now=_A)),('course',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='app.trainingcourse'))])]