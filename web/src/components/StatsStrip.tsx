"use client";

export default function StatsStrip({ score, mapped }: { score: number; mapped: number }) {
  return (
    <div className="grid grid-cols-2 gap-2 md:grid-cols-4">
      <div className="rounded-lg border border-border bg-card p-3"><p className="text-xs text-muted-foreground">Brief Confidence</p><p className="text-lg font-semibold">{score}%</p></div>
      <div className="rounded-lg border border-border bg-card p-3"><p className="text-xs text-muted-foreground">Mapped Phrases</p><p className="text-lg font-semibold">{mapped}</p></div>
      <div className="rounded-lg border border-border bg-card p-3"><p className="text-xs text-muted-foreground">Clarification Cards</p><p className="text-lg font-semibold">3</p></div>
      <div className="rounded-lg border border-border bg-card p-3"><p className="text-xs text-muted-foreground">Saved Snapshots</p><p className="text-lg font-semibold">Live</p></div>
    </div>
  );
}
