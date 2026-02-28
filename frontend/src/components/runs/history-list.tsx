"use client";

import { useEffect, useState } from "react";

import { getHistory, type Provider, type RunDetail } from "../../services/runs";

export function HistoryList() {
  const [provider, setProvider] = useState<Provider | "">("");
  const [items, setItems] = useState<RunDetail[]>([]);

  useEffect(() => {
    const load = async () => {
      const response = await getHistory(provider || undefined);
      setItems(response.items);
    };
    void load();
  }, [provider]);

  return (
    <section className="rounded border bg-white p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">Run History</h3>
        <select
          value={provider}
          onChange={(event) => setProvider(event.target.value as Provider | "")}
          className="rounded border p-1 text-xs"
        >
          <option value="">All</option>
          <option value="aws">AWS</option>
          <option value="azure">Azure</option>
        </select>
      </div>
      <ul className="mt-2 space-y-2 text-xs">
        {items.length === 0 ? <li className="text-slate-500">No runs yet.</li> : null}
        {items.map((item) => (
          <li key={item.run_id} className="rounded border bg-slate-50 p-2">
            <div className="font-medium">{item.query}</div>
            <div>{item.provider_scope.toUpperCase()} · {item.provider_runs.length} provider runs</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
