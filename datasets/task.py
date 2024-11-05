from accounts.models import ActivityLog, Report
from datetime import timedelta
from django.utils import timezone
from KarAmooziRoshan.celery import shared_task


def generate_report():
    start_time = timezone.now() - timedelta(days=1)
    report = Report.objects.create()
    activities = ActivityLog.objects.filter(timestamp__gte=start_time)
    for activity in activities:
        activity.report = report
        activity.save()
    return report.created_at


@shared_task
def generate_report_task():
    generate_report()
