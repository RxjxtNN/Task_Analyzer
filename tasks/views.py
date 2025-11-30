from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Task
from .scoring import TaskScorer
import json
from datetime import date

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            if not body:
                return JsonResponse({'error': 'Empty body'}, status=400)
                
            data = json.loads(body)
            # data can be a list or a single object
            if isinstance(data, dict):
                data = [data]
            
            # Save tasks
            for item in data:
                deps = item.get('dependencies', [])
                if isinstance(deps, str):
                    try:
                        deps = json.loads(deps)
                    except:
                        deps = []
                
                Task.objects.create(
                    title=item.get('title', 'Untitled'),
                    due_date=parse_date(item.get('due_date')),
                    importance=int(item.get('importance', 5)),
                    estimated_hours=int(item.get('estimated_hours', 1)),
                    dependencies=deps
                )
            
            # Analyze all tasks
            all_tasks = list(Task.objects.all())
            scorer = TaskScorer(all_tasks)
            results = scorer.calculate_scores()
            
            return JsonResponse(results, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)

def suggest(request):
    all_tasks = list(Task.objects.all())
    scorer = TaskScorer(all_tasks)
    results = scorer.calculate_scores()
    return JsonResponse(results[:3], safe=False)
