"use client";

import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

import type { CreateRunRequest, ProviderScope } from "../../services/runs";

interface QueryFormProps {
  onSubmit: (payload: CreateRunRequest) => Promise<void>;
  loading: boolean;
}

export function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const [query, setQuery] = useState("");
  const [providerScope, setProviderScope] = useState<ProviderScope>("aws");

  return (
    <form
      className="rounded border bg-white p-4"
      onSubmit={async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        await onSubmit({ query, provider_scope: providerScope });
      }}
    >
      <label className="mb-2 block text-sm font-medium">Architecture Query</label>
      <textarea
        value={query}
        onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setQuery(event.target.value)}
        className="mb-3 min-h-28 w-full rounded border p-2"
        placeholder="Describe your workload and constraints"
        required
      />

      <label className="mb-2 block text-sm font-medium">Provider Scope</label>
      <select
        value={providerScope}
        onChange={(event: ChangeEvent<HTMLSelectElement>) => setProviderScope(event.target.value as ProviderScope)}
        className="mb-4 w-full rounded border p-2"
      >
        <option value="aws">AWS</option>
        <option value="azure">Azure</option>
        <option value="both">Both</option>
      </select>

      <button
        type="submit"
        disabled={loading}
        className="rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
      >
        {loading ? "Running..." : "Generate Architecture"}
      </button>
    </form>
  );
}
