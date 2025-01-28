from django.core.management.base import BaseCommand
from django.db.models import Q

from app.models import TrainingCourse, TrainingCourseSession, TaskStatus


import datetime, random


class Command(BaseCommand):
    help = "Generate data..."

    def add_arguments(self, parser):
        parser.add_argument('models', nargs=1, choices=['TrainingCourse', 'TrainingCourseSession'], type=str,
                            help='Specify the models to generate data for.')
        parser.add_argument('action', nargs='?', choices=['create', 'create_hierarchical'], 
                                                          type=str, default='create',
                            help='Optional action to perform ("create"... supported).')

    def handle(self, *args, **options):
        models = options['models'][0]
        action = options['action']

        if models.find('TrainingCourse') == 0:

            if action == 'create_hierarchical':
                COURSES_AND_SESSIONS = [{
                    "course": {
                        "title": "LANCER ET MONÉTISER UNE CHAÎNE YOUTUBE",
                        "status_text": "Dossier: <a href='https://drive.google.com/drive/folders/1lqATEDM4Xkmp5ZOjnbqbF_Nfz7gB_mya' target='_blank'>en ligne</a>",
                        "sessions": [
                            {
                                "title": "Introduction",
                                "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Stratégie",
                                "status_text": "In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Chaîne Youtube - Metas",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "1ère Vidéo",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Publication",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Votre chaîne",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Conclusion",
                                "status_text": "",
                                "preparation": TaskStatus.COMPLETED,
                                "course_media_raw": TaskStatus.IN_VALIDATION,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }
                        ],
                    },
                },{
                    "course": {
                        "title": "TRAINING A PROJECT MANAGER",
                        "status_text": "Dossier: <a href='https://drive.google.com/drive/u/1/folders/187MK2EMs1QjRtLgDvHnAbTFe6qU4VXBU' target='_blank'>en ligne</a>",
                        "sessions": [
                            {
                                "title": "Introduction",
                                "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                                "preparation": TaskStatus.IN_PROGRESS,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Réunions (en ligne), outils & techniques",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Chaîne Youtube - Metas",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "1ère Vidéo",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Publication",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Votre chaîne",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }, {
                                "title": "Conclusion",
                                "status_text": "",
                                "preparation": TaskStatus.TODO,
                                "course_media_raw": TaskStatus.TODO,
                                "course_media_final": TaskStatus.TODO,
                                "course_media_validated": TaskStatus.TODO,
                                "implemented_in_app": TaskStatus.TODO,
                                "ready_for_whats_and_gram": TaskStatus.TODO,
                                "in_sales_funnel": TaskStatus.TODO,
                            }
                        ],
                    },
                }]


                # Fonction pour créer les catégories de manière récursive
                def create_courses_and_sessions(courses_and_sessions):
                    for item in courses_and_sessions:
                        print(item)
                        dcourse = item["course"]
                        ctitle = dcourse["title"]
                        # dcourse["slug"] = slugify(ctitle)
                        sessions = dcourse.pop("sessions")

                        tcourse, created = TrainingCourse.objects.get_or_create(**dcourse)
                        print(f"{'Created' if created else 'Fetched'} course :: {ctitle}")

                        # alt:
                        # ---
                        # for (title, status_text, preparation, course_media_raw,
                        #     course_media_final, course_media_validated, implemented_in_app,
                        #     ready_for_whats_and_gram, in_sales_funnel) in sessions.items():
                        for dsession in sessions:
                            stitle = dsession["title"]
                            dsession["course"] = tcourse
                            # dsession["slug"] = slugify(stitle)
                            # print(dsession)

                            created = False
                            try:
                                tsession = TrainingCourseSession.objects.get(
                                    title = stitle,
                                    course = tcourse
                                )
                            except TrainingCourseSession.DoesNotExist as err:
                                tsession = TrainingCourseSession.objects.create(**dsession)
                                created = True

                            print(f"{'Created' if created else 'Fetched'} training session :: {stitle}")


                # Création des catégories dans la base de données
                create_courses_and_sessions(COURSES_AND_SESSIONS)


