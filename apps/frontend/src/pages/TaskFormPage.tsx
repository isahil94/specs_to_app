import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import './TaskFormPage.css';

interface TaskFormPageProps {
  mode: 'create' | 'edit';
}

export function TaskFormPage({ mode }: TaskFormPageProps) {
  const title = useMemo(() => (mode === 'create' ? 'Create task' : 'Edit task'), [mode]);

  return (
    <section className="page task-form-page" aria-labelledby="task-form-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Task form</p>
          <h1 id="task-form-heading">{title}</h1>
        </div>
        <Link className="text-link" to="/tasks">
          Back to tasks
        </Link>
      </div>
      <form className="task-form" aria-label={title}>
        <label htmlFor="title">Title</label>
        <input id="title" name="title" type="text" required maxLength={100} placeholder="Task title" />

        <label htmlFor="description">Description</label>
        <textarea id="description" name="description" maxLength={2000} placeholder="Task description" />

        <div className="form-row">
          <label htmlFor="status">Status</label>
          <select id="status" name="status" defaultValue="Todo">
            <option value="Todo">Todo</option>
            <option value="In Progress">In Progress</option>
            <option value="Review">Review</option>
            <option value="Completed">Completed</option>
            <option value="Blocked">Blocked</option>
          </select>
        </div>

        <div className="form-row">
          <label htmlFor="priority">Priority</label>
          <select id="priority" name="priority" defaultValue="Medium">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
        </div>

        <div className="form-row">
          <label htmlFor="assignee">Assignee</label>
          <input id="assignee" name="assignee" type="text" placeholder="Assignee name" />
        </div>

        <div className="form-row">
          <label htmlFor="dueDate">Due date</label>
          <input id="dueDate" name="dueDate" type="date" />
        </div>

        <button type="submit" className="button primary">
          {mode === 'create' ? 'Create task' : 'Save changes'}
        </button>
      </form>
    </section>
  );
}
