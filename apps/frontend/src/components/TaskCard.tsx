import { Link } from 'react-router-dom';
import './TaskCard.css';

interface TaskSummary {
  id: string;
  title: string;
  status: string;
  priority: string;
  assignee: string;
  dueDate: string;
}

interface TaskCardProps {
  task: TaskSummary;
}

export function TaskCard({ task }: TaskCardProps) {
  return (
    <article className="task-card">
      <div className="task-card-main">
        <h2>{task.title}</h2>
        <p>{task.assignee}</p>
      </div>
      <div className="task-card-meta">
        <span className="chip status">{task.status}</span>
        <span className="chip priority">{task.priority}</span>
        <span className="task-due">Due {task.dueDate}</span>
      </div>
      <Link className="text-link" to={`/tasks/${task.id}`}>
        View details
      </Link>
    </article>
  );
}
