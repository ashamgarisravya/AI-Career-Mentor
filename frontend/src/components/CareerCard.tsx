import { ArrowUpRight, BriefcaseBusiness } from "lucide-react";
import type { CareerRecommendation } from "@/types/career";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export function CareerCard({ career }: { career: CareerRecommendation }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div>
            <CardTitle>{career.title}</CardTitle>
            <p className="mt-2 text-sm text-muted-foreground">{career.description}</p>
          </div>
          <BriefcaseBusiness className="h-5 w-5 text-primary" />
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span>Match score</span>
            <span className="font-semibold">{career.matchScore}%</span>
          </div>
          <Progress value={career.matchScore} />
        </div>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-md bg-muted p-3">
            <p className="text-muted-foreground">Salary</p>
            <p className="font-semibold">{career.salaryRange}</p>
          </div>
          <div className="rounded-md bg-muted p-3">
            <p className="text-muted-foreground">Growth</p>
            <p className="flex items-center gap-1 font-semibold text-primary">
              {career.growth} <ArrowUpRight className="h-3 w-3" />
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {career.skills.map((skill) => (
            <span key={skill} className="rounded-md bg-secondary px-2.5 py-1 text-xs text-secondary-foreground">
              {skill}
            </span>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
