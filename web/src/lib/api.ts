type PlanRequest = { query: string; preferences: string };
type PlanResponse = { summary: string; items: string[]; score: number };

type InsightsRequest = { selection: string; context: string };
type InsightsResponse = { insights: string[]; next_actions: string[]; highlights: string[] };

export async function fetchItems(): Promise<{ items: string[] }> {
  const seeded = {
    items: [
      "Build Web App — a rough opportunity note about a 12-year-old app developer wanting a usable planning workflow.",
      "Campus Club Scheduler — scattered notes about events, member reminders, and role permissions.",
      "Neighborhood Swap Board — a messy concept for borrowing tools and coordinating pickups.",
      "Creator Lesson Builder — an incomplete idea about turning expertise into guided mini-courses.",
      "Pet Care Routine Planner — fragmented requirements for shared feeding, meds, and caretaker notes."
    ]
  };
  try {
    const res = await fetch("/api/items", { method: "GET" });
    if (!res.ok) return seeded;
    return (await res.json()) as { items: string[] };
  } catch {
    return seeded;
  }
}

export async function createPlan(payload: PlanRequest): Promise<PlanResponse> {
  const res = await fetch("/api/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Generation failed. Please retry.");
  return (await res.json()) as PlanResponse;
}

export async function createInsights(payload: InsightsRequest): Promise<InsightsResponse> {
  const res = await fetch("/api/insights", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Could not generate clarification cards.");
  return (await res.json()) as InsightsResponse;
}

export async function saveSnapshot(payload: { title: string; summary: string }) {
  const res = await fetch("/api/snapshots", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    return { id: crypto.randomUUID(), title: payload.title, summary: payload.summary, timestamp: new Date().toISOString() };
  }
  return (await res.json()) as { id: string; title: string; summary: string; timestamp: string };
}
