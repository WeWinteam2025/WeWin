from django.http import JsonResponse
from django.db import connection


def healthz(request):
  try:
    with connection.cursor() as cursor:
      cursor.execute('SELECT 1;')
      row = cursor.fetchone()
    db_ok = row[0] == 1
  except Exception as exc:
    return JsonResponse({'ok': False, 'db': False, 'error': str(exc)}, status=500)

  return JsonResponse({'ok': True, 'db': db_ok})




