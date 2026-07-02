import { useParams, Link } from 'react-router-dom';
import './TaskDetailPage.css';

export function TaskDetailPage() {
  const { taskId } = useParams();

  return (
    <section className="page task-detail-page" aria-labelledby="task-detail-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Task details</p>
          <h1 id="task-detail-heading">Review task #{taskId}</h1>
        </div>
        <Link className="button secondary" to={`/tasks/${taskId}/edit`}>
          Edit task
        </Link>
      </div>
      <article className="task-detail-card">
        <h2>Design onboarding task flow</h2>
        <p className="task-status">Status: <strong>In Progress</strong></p>
        <p className="task-priority">Priority: <strong>High</strong></p>
        <p className="task-meta">Assigned to Alex • Due 2026-07-10</p>
        <section>
          <h3>Description</h3>
          <p>Define the onboarding flow and handoff notes for the task management project.</p>
        </section>
        <section>
          <h3>Comments</h3>
          <p>No comments yet. Add a note on the task to begin collaboration.</p>
        </section>
      </article>
    </section>
  );
}
