"use client";

type Props = {
  className?: string;
  notes: string;
  setNotes: (v: string) => void;
  preferences: string;
  setPreferences: (v: string) => void;
  items: string[];
  loading: boolean;
  generating: boolean;
  canGenerate: boolean;
  onGenerate: () => void;
};

export default function WorkspacePanel(props: Props) {
  return (
    <section className={`${props.className ?? ""} rounded-lg border border-border bg-card p-4 shadow-soft`}>
      <h2 className="text-xl">Rough context intake sheet</h2>
      <p className="mt-1 text-xs text-muted-foreground">Seeded starters let judges run an instant first pass.</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {props.items.map((item) => (
          <button
            key={item}
            onClick={() => props.setNotes(item)}
            className="rounded-md border border-border bg-muted px-2 py-1 text-xs text-foreground hover:bg-accent hover:text-accent-foreground"
          >
            Use starter
          </button>
        ))}
      </div>
      <textarea
        value={props.notes}
        onChange={(e) => props.setNotes(e.target.value)}
        className="mt-3 h-56 w-full rounded-md border border-border bg-background p-3 text-sm outline-none"
      />
      <textarea
        value={props.preferences}
        onChange={(e) => props.setPreferences(e.target.value)}
        className="mt-3 h-20 w-full rounded-md border border-border bg-background p-3 text-sm outline-none"
      />
      <button
        onClick={props.onGenerate}
        disabled={!props.canGenerate || props.loading}
        className="mt-3 w-full rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground disabled:opacity-50"
      >
        {props.generating ? "Generating Brief..." : "Generate Brief"}
      </button>
    </section>
  );
}
