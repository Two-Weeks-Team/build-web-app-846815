"use client";

import { useEffect, useMemo, useState } from "react";
import Hero from "@/components/Hero";
import WorkspacePanel from "@/components/WorkspacePanel";
import InsightPanel from "@/components/InsightPanel";
import CollectionPanel from "@/components/CollectionPanel";
import { createInsights, createPlan, fetchItems, saveSnapshot } from "@/lib/api";

export default function Page() {
  const [notes, setNotes] = useState("");
  const [preferences, setPreferences] = useState("MVP focus; team size: 2; timeline: 6 weeks");
  const [selection, setSelection] = useState("Target user is unclear between student builders and indie founders.");
  const [context, setContext] = useState("Need to decide who the first release serves best.");
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [insighting, setInsighting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [items, setItems] = useState<string[]>([]);
  const [brief, setBrief] = useState<{ summary: string; items: string[]; score: number } | null>(null);
  const [insights, setInsights] = useState<{ insights: string[]; next_actions: string[]; highlights: string[] } | null>(null);
  const [snapshots, setSnapshots] = useState<Array<{ id: string; title: string; timestamp: string; summary: string }>>([]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchItems();
        setItems(data.items);
        setNotes(data.items[0] || "");
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load starter notes.");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  const canGenerate = useMemo(() => notes.trim().length > 20 && !generating, [notes, generating]);

  const onGenerate = async () => {
    setGenerating(true);
    setError(null);
    setSuccess(null);
    try {
      const result = await createPlan({ query: notes, preferences });
      setBrief(result);
      setSuccess("Structured brief generated with source mapping.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not generate brief.");
    } finally {
      setGenerating(false);
    }
  };

  const onClarify = async () => {
    setInsighting(true);
    setError(null);
    setSuccess(null);
    try {
      const result = await createInsights({ selection, context });
      setInsights(result);
      setSuccess("Clarification updates ready. Review the guided cards.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load clarification insights.");
    } finally {
      setInsighting(false);
    }
  };

  const onSave = async () => {
    if (!brief) return;
    setSaving(true);
    setError(null);
    try {
      const saved = await saveSnapshot({ title: "Planning Snapshot", summary: brief.summary });
      setSnapshots((prev) => [saved, ...prev]);
      setSuccess("Snapshot pinned to your working board.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save snapshot.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="min-h-screen bg-background p-4 md:p-6">
      <Hero />
      <div className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-12">
        <WorkspacePanel
          className="xl:col-span-4"
          notes={notes}
          setNotes={setNotes}
          preferences={preferences}
          setPreferences={setPreferences}
          items={items}
          loading={loading}
          generating={generating}
          canGenerate={canGenerate}
          onGenerate={onGenerate}
        />
        <InsightPanel
          className="xl:col-span-5"
          loading={generating}
          brief={brief}
          insights={insights}
          selection={selection}
          setSelection={setSelection}
          context={context}
          setContext={setContext}
          insighting={insighting}
          onClarify={onClarify}
          onSave={onSave}
          saving={saving}
        />
        <CollectionPanel className="xl:col-span-3" snapshots={snapshots} error={error} success={success} />
      </div>
    </main>
  );
}
