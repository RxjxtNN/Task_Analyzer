document.addEventListener('DOMContentLoaded', () => {
    const singleTaskForm = document.getElementById('single-task-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const bulkJsonInput = document.getElementById('bulk-json');
    const resultsList = document.getElementById('results-list');
    const sortSelect = document.getElementById('sort-strategy');

    let currentTasks = []; // Keep a local copy for sorting

    const API_URL = '/api/tasks/analyze/';

    singleTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const dueDate = document.getElementById('due_date').value;
        const importance = document.getElementById('importance').value;
        const estHours = document.getElementById('estimated_hours').value;
        const depsStr = document.getElementById('dependencies').value;

        let dependencies = [];
        if (depsStr) {
            dependencies = depsStr.split(',').map(s => s.trim()).filter(s => s);
        }

        const task = {
            title,
            due_date: dueDate,
            importance: parseInt(importance),
            estimated_hours: parseInt(estHours),
            dependencies
        };

        await analyzeTasks([task]);
        singleTaskForm.reset();
    });

    analyzeBtn.addEventListener('click', async () => {
        try {
            const jsonStr = bulkJsonInput.value;
            if (!jsonStr) return;
            const tasks = JSON.parse(jsonStr);
            await analyzeTasks(tasks);
        } catch (e) {
            alert('Invalid JSON');
        }
    });

    async function analyzeTasks(tasks) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(tasks)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const results = await response.json();
            currentTasks = results;
            applySorting();
        } catch (error) {
            console.error('Error:', error);
            alert('Error analyzing tasks');
        }
    }

    sortSelect.addEventListener('change', () => {
        applySorting();
    });

    function applySorting() {
        const strategy = sortSelect.value;
        let sorted = [...currentTasks];

        switch (strategy) {
            case 'fastest':
                // Sort by estimated_hours (asc)
                sorted.sort((a, b) => a.estimated_hours - b.estimated_hours);
                break;
            case 'impact':
                // Sort by importance (desc)
                sorted.sort((a, b) => b.importance - a.importance);
                break;
            case 'deadline':
                // Sort by due_date (asc). Handle nulls last.
                sorted.sort((a, b) => {
                    if (!a.due_date) return 1;
                    if (!b.due_date) return -1;
                    return new Date(a.due_date) - new Date(b.due_date);
                });
                break;
            case 'smart':
            default:
                // Default: Use the server-side algorithm score
                sorted.sort((a, b) => b.score - a.score);
                break;
        }
        renderResults(sorted);
    }

    function renderResults(tasks) {
        resultsList.innerHTML = '';

        tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = 'task-card';

            // Highlight high-priority stuff (red/yellow/green)
            // If it's urgent or blocking something, mark it high.

            let priorityClass = 'low-priority';
            const isUrgent = task.reasons.some(r => r.includes('Urgency'));
            const isBlocker = task.reasons.some(r => r.includes('Blocking'));

            if (isUrgent || isBlocker || task.score > 10) {
                priorityClass = 'high-priority';
            } else if (task.score > 5) {
                priorityClass = 'medium-priority';
            }

            card.classList.add(priorityClass);

            const reasonsHtml = task.reasons.length > 0
                ? `<div class="task-reasons">Why: ${task.reasons.join(', ')}</div>`
                : '';

            card.innerHTML = `
                <div class="task-header">
                    <span class="task-title">#${task.id} ${task.title}</span>
                    <span class="task-score">Score: ${task.score}</span>
                </div>
                <div class="task-details">
                    Due: ${task.due_date || 'N/A'} | Imp: ${task.importance} | Est: ${task.estimated_hours}h
                </div>
                ${reasonsHtml}
            `;

            resultsList.appendChild(card);
        });
    }
});
