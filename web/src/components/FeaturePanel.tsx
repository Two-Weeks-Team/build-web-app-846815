"use client";

export default function FeaturePanel({ items }: { items: string[] }) {
  return (
    <section className="rounded-xl border border-border bg-card p-4 shadow-paper card-settle">
      <h3 className="mb-3 text-lg">Feature Stack</h3>
      <ul className="space-y-2 text-sm">
        {items.map((i, idx) => (
          <li key={`${i}-${idx}`} className="rounded-md border border-border bg-muted px-3 py-2">{i}</li>
        ))}
      </ul>
    </section>
  );
}
