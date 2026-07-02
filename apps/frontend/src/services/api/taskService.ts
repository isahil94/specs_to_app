export interface TaskSummary {
  task_id: string;
  title: string;
  status: string;
  priority: string;
  assignee_id?: string;
  due_date?: string;
}

export interface TaskDetail extends TaskSummary {
  description?: string;
  labels?: string[];
  creator_id?: string;
  created_at?: string;
  history_summary?: string;
  comments_count?: number;
}

const API_BASE = '/api';

export async function fetchTasks(): Promise<TaskSummary[]> {
  const response = await fetch(`${API_BASE}/tasks`);
  if (!response.ok) {
    throw new Error('Unable to fetch tasks');
  }
  return response.json();
}

export async function fetchTask(taskId: string): Promise<TaskDetail> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}`);
  if (!response.ok) {
    throw new Error('Unable to fetch task');
  }
  return response.json();
}

export async function createTask(payload: Partial<TaskDetail>): Promise<TaskDetail> {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error('Unable to create task');
  }
  return response.json();
}
