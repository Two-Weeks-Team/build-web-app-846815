"use client";

export default function ReferenceShelf({ onUse }: { onUse: (text: string) => void }) {
  const seeds = [
    "Build Web App — a rough opportunity note about a 12-year-old app developer wanting a usable planning workflow",
    "Campus Club Scheduler — scattered notes about events, member reminders, and role permissions",
    "Neighborhood Swap Board — a messy concept for borrowing tools and coordinating pickups",
    "Creator Lesson Builder — an incomplete idea about turning expertise into guided mini-courses",
    "Pet Care Routine Planner — fragmented requirements for shared feeding, meds, and caretaker notes"
  ];

  return (
    <section className="rounded-xl border border-border bg-card p-4 shadow-paper">
      <h3 className="mb-3 text-lg">Seeded Workbench Starters</h3>
      <div className="flex flex-wrap gap-2">
        {seeds.map((s) => (
          <button key={s} onClick={() => onUse(s)} className="rounded-full border border-border bg-muted px-3 py-2 text-xs hover:border-accent">
            {s.split("—")[0].trim()}
          </button>
        ))}
      </div>
    </section>
  );
}
