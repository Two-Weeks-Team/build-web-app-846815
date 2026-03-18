"use client";

export default function Hero() {
  return (
    <section className="rounded-lg border border-border bg-card/80 p-5 shadow-paper backdrop-blur">
      <p className="text-sm text-accent">Product Planning Workbench</p>
      <h1 className="mt-2 text-3xl font-bold text-foreground">Turn rough notes into a traceable product brief</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        A drafting-table workflow: capture messy context, generate a structured brief, inspect source-to-brief mapping, resolve ambiguity, and pin reusable snapshots.
      </p>
    </section>
  );
}
