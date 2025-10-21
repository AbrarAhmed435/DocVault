import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function PatientSummary({ summary }) {
  return (
    <div className="patient-summary">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {summary}
      </ReactMarkdown>
    </div>
  );
}
