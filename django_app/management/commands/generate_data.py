_D='create_hierarchical'
_C='action'
_B='TrainingCourse'
_A='models'
from django.core.management.base import BaseCommand
from django.db.models import Q
from app.models import TrainingCourse,TrainingCourseSession,TaskStatus
import datetime,random
class Command(BaseCommand):
	help='Generate data...'
	def add_arguments(C,parser):A='create';B=parser;B.add_argument(_A,nargs=1,choices=[_B,'TrainingCourseSession'],type=str,help='Specify the models to generate data for.');B.add_argument(_C,nargs='?',choices=[A,_D],type=str,default=A,help='Optional action to perform ("create"... supported).')
	def handle(Y,*Z,**M):
		N='Conclusion';O='Votre chaîne';P='Publication';Q='1ère Vidéo';R='Chaîne Youtube - Metas';S='Prérequis: Créer votre email - In text format, medias to do...';T='Introduction';L='sessions';K='course';J='';C='in_sales_funnel';D='ready_for_whats_and_gram';E='implemented_in_app';F='course_media_validated';G='course_media_final';H='course_media_raw';I='preparation';B='status_text';A='title';U=M[_A][0];V=M[_C]
		if U.find(_B)==0:
			if V==_D:
				W=[{K:{A:'LANCER ET MONÉTISER UNE CHAÎNE YOUTUBE',B:"Dossier: <a href='https://drive.google.com/drive/folders/1lqATEDM4Xkmp5ZOjnbqbF_Nfz7gB_mya' target='_blank'>en ligne</a>",L:[{A:T,B:S,I:TaskStatus.IN_PROGRESS,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:'Stratégie',B:'In text format, medias to do...',I:TaskStatus.IN_PROGRESS,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:R,B:J,I:TaskStatus.COMPLETED,H:TaskStatus.IN_VALIDATION,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:Q,B:J,I:TaskStatus.COMPLETED,H:TaskStatus.IN_VALIDATION,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:P,B:J,I:TaskStatus.COMPLETED,H:TaskStatus.IN_VALIDATION,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:O,B:J,I:TaskStatus.COMPLETED,H:TaskStatus.IN_VALIDATION,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:N,B:J,I:TaskStatus.COMPLETED,H:TaskStatus.IN_VALIDATION,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO}]}},{K:{A:'TRAINING A PROJECT MANAGER',B:"Dossier: <a href='https://drive.google.com/drive/u/1/folders/187MK2EMs1QjRtLgDvHnAbTFe6qU4VXBU' target='_blank'>en ligne</a>",L:[{A:T,B:S,I:TaskStatus.IN_PROGRESS,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:'Réunions (en ligne), outils & techniques',B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:R,B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:Q,B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:P,B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:O,B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO},{A:N,B:J,I:TaskStatus.TODO,H:TaskStatus.TODO,G:TaskStatus.TODO,F:TaskStatus.TODO,E:TaskStatus.TODO,D:TaskStatus.TODO,C:TaskStatus.TODO}]}}]
				def X(courses_and_sessions):
					E='Fetched';F='Created'
					for G in courses_and_sessions:
						print(G);C=G[K];J=C[A];M=C.pop(L);H,B=TrainingCourse.objects.get_or_create(**C);print(f"{F if B else E} course :: {J}")
						for D in M:
							I=D[A];D[K]=H;B=False
							try:N=TrainingCourseSession.objects.get(title=I,course=H)
							except TrainingCourseSession.DoesNotExist as O:N=TrainingCourseSession.objects.create(**D);B=True
							print(f"{F if B else E} training session :: {I}")
				X(W)