import './SummaryCard.css';

interface SummaryCardProps {
  title: string;
  value: string;
}

export function SummaryCard({ title, value }: SummaryCardProps) {
  return (
    <div className="summary-card">
      <p className="summary-title">{title}</p>
      <p className="summary-value">{value}</p>
    </div>
  );
}
