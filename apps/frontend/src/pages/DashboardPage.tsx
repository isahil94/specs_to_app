import { Link } from 'react-router-dom';
import { SummaryCard } from '../components/SummaryCard';
import './DashboardPage.css';

export function DashboardPage() {
  return (
    <section className="page dashboard-page" aria-labelledby="dashboard-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Welcome back</p>
          <h1 id="dashboard-heading">Your dashboard</h1>
        </div>
        <Link className="button primary" to="/tasks/new">
          Create task
        </Link>
      </div>
      <div className="dashboard-grid">
        <SummaryCard title="Open tasks" value="24" />
        <SummaryCard title="In progress" value="8" />
        <SummaryCard title="Due soon" value="5" />
        <SummaryCard title="Completed" value="32" />
      </div>
      <section className="dashboard-panel" aria-labelledby="recent-tasks-heading">
        <div className="panel-header">
          <h2 id="recent-tasks-heading">Recent tasks</h2>
          <Link className="text-link" to="/tasks">
            View all tasks
          </Link>
        </div>
        <div className="panel-body">
          <p className="panel-empty">Select a task to view details and update status.</p>
        </div>
      </section>
    </section>
  );
}
