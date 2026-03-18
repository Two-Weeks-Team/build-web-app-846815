"use client";

type Props = {
  loading?: boolean;
  error?: string | null;
  success?: string | null;
  empty?: boolean;
  emptyLabel?: string;
};

export default function StatePanel({ loading, error, success, empty, emptyLabel }: Props) {
  if (loading) {
    return <div className="rounded-lg border border-border bg-card p-3 text-sm text-muted-foreground">Generating your brief… tracing phrases and drafting cards.</div>;
  }
  if (error) {
    return <div className="rounded-lg border border-destructive bg-card p-3 text-sm text-destructive">{error}</div>;
  }
  if (success) {
    return <div className="rounded-lg border border-success bg-card p-3 text-sm text-success">{success}</div>;
  }
  if (empty) {
    return <div className="rounded-lg border border-border bg-card p-3 text-sm text-muted-foreground">{emptyLabel ?? "Nothing yet."}</div>;
  }
  return null;
}
