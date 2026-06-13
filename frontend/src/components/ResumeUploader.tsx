"use client";

import { useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export function ResumeUploader({ onAnalyze, loading }: { onAnalyze: (file?: File) => void; loading?: boolean }) {
  const [file, setFile] = useState<File | undefined>();

  return (
    <Card>
      <CardContent className="space-y-4 p-5">
        <label className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed bg-muted/40 p-6 text-center transition hover:bg-muted">
          <UploadCloud className="mb-3 h-8 w-8 text-primary" />
          <span className="text-sm font-medium">Upload resume PDF</span>
          <span className="mt-1 text-xs text-muted-foreground">PDF files up to 10MB</span>
          <input
            className="sr-only"
            type="file"
            accept="application/pdf"
            onChange={(event) => setFile(event.target.files?.[0])}
          />
        </label>
        {file ? (
          <div className="flex items-center gap-2 rounded-md bg-secondary p-3 text-sm">
            <FileText className="h-4 w-4 text-primary" />
            <span className="truncate">{file.name}</span>
          </div>
        ) : null}
        <Button className="w-full" onClick={() => onAnalyze(file)} disabled={loading}>
          Analyze Resume
        </Button>
      </CardContent>
    </Card>
  );
}
