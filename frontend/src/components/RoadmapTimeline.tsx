import { CalendarDays } from "lucide-react";
import type { RoadmapMonth } from "@/types/career";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function RoadmapTimeline({ roadmap }: { roadmap: RoadmapMonth[] }) {
  return (
    <div className="space-y-4">
      {roadmap.map((item) => (
        <Card key={item.month}>
          <CardHeader>
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-medium text-primary">{item.month}</p>
                <CardTitle>{item.title}</CardTitle>
              </div>
              <CalendarDays className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent className="grid gap-5 md:grid-cols-2">
            <div>
              <h4 className="text-sm font-semibold">Goals</h4>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {item.goals.map((goal) => (
                  <li key={goal} className="flex gap-2">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {goal}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold">Resources</h4>
              <div className="mt-3 space-y-2">
                {item.resources.map((resource) => (
                  <div key={resource.title} className="rounded-md bg-muted p-3 text-sm">
                    <div className="flex justify-between gap-3">
                      <span className="font-medium">{resource.title}</span>
                      <span className="text-xs text-muted-foreground">{resource.duration}</span>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">{resource.type}</p>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
