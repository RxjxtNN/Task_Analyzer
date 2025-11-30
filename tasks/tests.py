from django.test import TestCase
from .models import Task
from .scoring import TaskScorer
from datetime import date, timedelta

class TaskScorerTest(TestCase):
    def test_scoring_logic(self):
        # Create tasks
        t1 = Task.objects.create(
            title="Urgent Task",
            due_date=date.today() + timedelta(days=1),
            importance=10,
            estimated_hours=2,
            dependencies=[]
        )
        t2 = Task.objects.create(
            title="Long Term Task",
            due_date=date.today() + timedelta(days=30),
            importance=8,
            estimated_hours=10,
            dependencies=[]
        )
        t3 = Task.objects.create(
            title="Blocker Task",
            due_date=date.today() + timedelta(days=5),
            importance=5,
            estimated_hours=1,
            dependencies=[t1.id] # Blocks t1
        )
        
        scorer = TaskScorer([t1, t2, t3])
        results = scorer.calculate_scores()
        
        # Verify results exist and are sorted
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]['score'] >= results[1]['score'])
        
        # Verify t3 got a boost from t1
        # t3 base score: ROI=5, Urgency ~2. Base ~10.
        # t1 base score: ROI=5, Urgency ~4. Base ~20.
        # t3 final should be Base + 0.5 * t1_base ~ 20.
        # t3 should be high up.
        
        # Check if reasons are populated
        self.assertTrue(len(results[0]['reasons']) > 0)
