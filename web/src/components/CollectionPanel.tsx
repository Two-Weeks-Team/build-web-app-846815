"use client";

type Snapshot = { id: string; title: string; timestamp: string; summary: string };

export default function CollectionPanel({ className, snapshots, error, success }: { className?: string; snapshots: Snapshot[]; error: string | null; success: string | null }) {
  return (
    <section className={`${className ?? ""} rounded-lg border border-border bg-card p-4 shadow-soft`}>
      <h2 className="text-xl">Planning Snapshot pinboard</h2>
      {error && <p className="mt-2 text-xs text-destructive">{error}</p>}
      {success && <p className="mt-2 text-xs text-success">{success}</p>}
      <div className="mt-3 space-y-2">
        {snapshots.length === 0 && <p className="text-sm text-muted-foreground">No snapshots pinned yet. Save your first generated artifact.</p>}
        {snapshots.map((s) => (
          <article key={s.id} className="rounded-md border border-border bg-background p-3">
            <h3 className="text-sm">{s.title}</h3>
            <p className="text-xs text-muted-foreground">{new Date(s.timestamp).toLocaleString()}</p>
            <p className="mt-1 text-xs">{s.summary}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
