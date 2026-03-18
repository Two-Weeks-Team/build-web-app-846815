import type { Metadata } from "next";
import { Merriweather, Nunito } from "next/font/google";
import "@/app/globals.css";

const display = Merriweather({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-display"
});

const body = Nunito({
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  variable: "--font-body"
});

export const metadata: Metadata = {
  title: "Build Web App — Product Planning Workbench",
  description: "Turn rough product notes into a structured, traceable brief you can refine and save in minutes."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${display.variable} ${body.variable} bg-background text-foreground`}>{children}</body>
    </html>
  );
}
