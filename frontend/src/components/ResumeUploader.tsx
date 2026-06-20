"use client";

import { useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

export function ResumeUploader({
  onAnalyze,
  loading
}: {
  onAnalyze: (file?: File, resumeText?: string) => void;
  loading?: boolean;
}) {
  const [file, setFile] = useState<File | undefined>();
  const [resumeText, setResumeText] = useState("");

  return (
    <Card>
      <CardContent className="space-y-4 p-5">
        <label className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed bg-muted/40 p-6 text-center transition hover:bg-muted">
          <UploadCloud className="mb-3 h-8 w-8 text-primary" />
          <span className="text-sm font-medium">Upload resume PDF</span>
          <span className="mt-1 text-xs text-muted-foreground">PDF files up to 10MB, or paste resume text below</span>
          <input
            className="sr-only"
            type="file"
            accept="application/pdf,text/plain"
            onChange={(event) => setFile(event.target.files?.[0])}
          />
        </label>
        {file ? (
          <div className="flex items-center gap-2 rounded-md bg-secondary p-3 text-sm">
            <FileText className="h-4 w-4 text-primary" />
            <span className="truncate">{file.name}</span>
          </div>
        ) : null}
        <Textarea
          placeholder="Optional: paste your resume text here if you don't have a PDF handy."
          value={resumeText}
          onChange={(event) => setResumeText(event.target.value)}
          rows={10}
        />
        <Button className="w-full" onClick={() => onAnalyze(file, resumeText)} disabled={loading || (!file && !resumeText.trim())}>
          Analyze Resume
        </Button>
      </CardContent>
    </Card>
  );
}
