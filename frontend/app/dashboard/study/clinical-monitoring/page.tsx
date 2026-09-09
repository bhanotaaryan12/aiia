import Link from "next/link";
import DemoRecordPanel from "@/components/demo-record-panel";

export default function ClinicalMonitoringPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <Link href="/dashboard/study" className="text-sm font-medium text-teal-800 underline underline-offset-2">
        Back to study record
      </Link>
      <DemoRecordPanel recordKey="clinical_monitoring" />
    </div>
  );
}
