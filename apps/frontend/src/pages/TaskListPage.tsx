import { Link } from 'react-router-dom';
import { TaskCard } from '../components/TaskCard';
import './TaskListPage.css';

const tasks = [
  { id: '1', title: 'Design onboarding task flow', status: 'In Progress', priority: 'High', assignee: 'Alex', dueDate: '2026-07-10' },
  { id: '2', title: 'Review API contract for tasks', status: 'Todo', priority: 'Medium', assignee: 'Taylor', dueDate: '2026-07-14' }
];

export function TaskListPage() {
  return (
    <section className="page task-list-page" aria-labelledby="task-list-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Task management</p>
          <h1 id="task-list-heading">All tasks</h1>
        </div>
        <Link className="button primary" to="/tasks/new">
          New task
        </Link>
      </div>
      <div className="task-list-actions">
        <div className="filter-group" role="group" aria-label="Task filters">
          <label>
            Search
            <input type="search" placeholder="Search tasks" />
          </label>
          <label>
            Status
            <select defaultValue="">
              <option value="">All</option>
              <option value="Todo">Todo</option>
              <option value="In Progress">In Progress</option>
              <option value="Review">Review</option>
              <option value="Completed">Completed</option>
              <option value="Blocked">Blocked</option>
            </select>
          </label>
        </div>
      </div>
      <div className="task-list-grid">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </section>
  );
}
