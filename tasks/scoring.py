import math
from datetime import date

class TaskScorer:
    def __init__(self, tasks):
        # tasks is a list of Task objects
        self.tasks = tasks

    def calculate_scores(self):
        # Pass 1: Base Score
        # Map ID to task and score data
        scores = {}
        
        for task in self.tasks:
            # ROI: Importance / Estimated Hours
            if task.estimated_hours <= 0:
                roi = task.importance * 10 # Avoid div by zero, treat as very efficient
            else:
                roi = task.importance / task.estimated_hours
            
            # Urgency: 1 + (4 / ln(days_until_due + 2))
            if isinstance(task.due_date, str):
                # Should be date object from model, but handle string just in case
                from django.utils.dateparse import parse_date
                d = parse_date(task.due_date)
            else:
                d = task.due_date
                
            if d:
                days_until_due = (d - date.today()).days
            else:
                days_until_due = 10 # Default if missing
                
            if days_until_due < 0:
                urgency_multiplier = 5.0
            else:
                try:
                    # ln(days + 2)
                    denom = math.log(days_until_due + 2)
                    if denom == 0:
                        urgency_multiplier = 5.0
                    else:
                        urgency_multiplier = 1 + (4 / denom)
                except ValueError:
                    urgency_multiplier = 5.0
            
            base_score = roi * urgency_multiplier
            scores[task.id] = {'task': task, 'score': base_score, 'reasons': []}
            
            if urgency_multiplier >= 3:
                scores[task.id]['reasons'].append("High Urgency")
            if roi > 2:
                scores[task.id]['reasons'].append("High ROI")

        # Pass 2: Dependency Inheritance
        # If Task A blocks Task B, Task A inherits 50% of B's score.
        # task.dependencies contains IDs of tasks that depend on this task (Blocked tasks)
        
        final_results = []
        for task in self.tasks:
            score_data = scores[task.id]
            current_score = score_data['score']
            
            blocked_task_ids = task.dependencies # List of IDs
            if not isinstance(blocked_task_ids, list):
                blocked_task_ids = []
                
            for blocked_id in blocked_task_ids:
                # Ensure blocked_id is int
                try:
                    blocked_id = int(blocked_id)
                except:
                    continue
                    
                if blocked_id in scores:
                    blocked_score = scores[blocked_id]['score']
                    inheritance = blocked_score * 0.5
                    current_score += inheritance
                    score_data['reasons'].append(f"Blocking Critical Task {blocked_id}")
            
            final_results.append({
                'id': task.id,
                'title': task.title,
                'score': round(current_score, 2),
                'reasons': score_data['reasons'],
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'importance': task.importance,
                'estimated_hours': task.estimated_hours
            })
            
        return sorted(final_results, key=lambda x: x['score'], reverse=True)
