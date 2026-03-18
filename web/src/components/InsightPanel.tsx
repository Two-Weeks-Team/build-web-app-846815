"use client";

type Brief = { summary: string; items: string[]; score: number };
type Insights = { insights: string[]; next_actions: string[]; highlights: string[] };

type Props = {
  className?: string;
  loading: boolean;
  brief: Brief | null;
  insights: Insights | null;
  selection: string;
  setSelection: (v: string) => void;
  context: string;
  setContext: (v: string) => void;
  insighting: boolean;
  onClarify: () => void;
  onSave: () => void;
  saving: boolean;
};

export default function InsightPanel(props: Props) {
  return (
    <section className={`${props.className ?? ""} rounded-lg border border-border bg-card p-4 shadow-paper`}>
      <h2 className="text-xl">Structured brief canvas</h2>
      {!props.brief && <p className="mt-2 text-sm text-muted-foreground">Waiting for generated Product Brief, Problem Statement, Target User Profile, and Feature Stack.</p>}
      {props.brief && (
        <div className="mt-3 space-y-3">
          <article className="rounded-md border border-border bg-background p-3">
            <h3 className="text-sm text-accent">Product Brief</h3>
            <p className="text-sm">{props.brief.summary}</p>
            <p className="mt-2 text-xs text-success">Confidence score: {props.brief.score}</p>
          </article>
          <article className="rounded-md border border-border bg-background p-3">
            <h3 className="text-sm text-accent">Phrase-to-brief mapping</h3>
            <ul className="mt-2 list-disc pl-5 text-sm">
              {props.brief.items.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </article>
          <article className="rounded-md border border-border bg-background p-3">
            <h3 className="text-sm text-warning">Guided clarification rail</h3>
            <textarea value={props.selection} onChange={(e) => props.setSelection(e.target.value)} className="mt-2 h-20 w-full rounded border border-border bg-card p-2 text-sm" />
            <textarea value={props.context} onChange={(e) => props.setContext(e.target.value)} className="mt-2 h-16 w-full rounded border border-border bg-card p-2 text-sm" />
            <div className="mt-2 flex gap-2">
              <button onClick={props.onClarify} disabled={props.insighting} className="rounded bg-accent px-3 py-1 text-xs text-accent-foreground disabled:opacity-50">{props.insighting ? "Updating..." : "Run Clarification"}</button>
              <button onClick={props.onSave} disabled={props.saving} className="rounded bg-primary px-3 py-1 text-xs text-primary-foreground disabled:opacity-50">{props.saving ? "Saving..." : "Save Snapshot"}</button>
            </div>
          </article>
          {props.insights && (
            <article className="rounded-md border border-border bg-background p-3">
              <h3 className="text-sm text-accent">Resolution notes layer</h3>
              <ul className="mt-2 list-disc pl-5 text-sm">{props.insights.insights.map((i) => <li key={i}>{i}</li>)}</ul>
            </article>
          )}
        </div>
      )}
    </section>
  );
}
