import type { WorkflowEvent } from "../../services/workflow-stream";

interface HandoffTimelineProps {
  events: WorkflowEvent[];
}

export function HandoffTimeline({ events }: HandoffTimelineProps) {
  return (
    <section className="rounded border bg-white p-4">
      <h3 className="text-sm font-semibold">Hand-off Timeline</h3>
      <ul className="mt-2 space-y-2 text-xs">
        {events.length === 0 ? <li className="text-slate-500">No events yet.</li> : null}
        {events.map((event) => (
          <li key={event.event_id} className="rounded border bg-slate-50 p-2">
            <div className="font-medium uppercase">{event.provider}</div>
            <div>{event.event_type} · {event.node.type} ({event.node.state})</div>
            <div className="text-slate-500">{new Date(event.timestamp).toLocaleTimeString()}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
