import { AlertTriangle, CheckCircle2, CircleDot } from "lucide-react";
import type { SkillGap } from "@/types/career";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

const priorityStyle = {
  High: "bg-destructive/10 text-destructive",
  Medium: "bg-accent/20 text-accent-foreground",
  Low: "bg-primary/10 text-primary"
};

export function SkillGapCard({ gap }: { gap: SkillGap }) {
  const Icon = gap.priority === "High" ? AlertTriangle : gap.priority === "Medium" ? CircleDot : CheckCircle2;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <CardTitle>{gap.skill}</CardTitle>
          <span className={cn("inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium", priorityStyle[gap.priority])}>
            <Icon className="h-3 w-3" />
            {gap.priority}
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Current {gap.currentLevel}%</span>
            <span>Target {gap.targetLevel}%</span>
          </div>
          <Progress value={gap.currentLevel} />
        </div>
        <ul className="space-y-2 text-sm">
          {gap.resources.map((resource) => (
            <li key={resource} className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-primary" />
              {resource}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
