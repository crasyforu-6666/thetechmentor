import type { Metadata } from "next";
import { admin } from "@/content/site";
import Dashboard from "./Dashboard";
import "./admin.css";

export const metadata: Metadata = {
  title: admin.title,
  robots: { index: false, follow: false },
};

export default function AdminPage() {
  return <Dashboard />;
}
