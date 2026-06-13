"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Compass, FileText, Map, Target, UserRound } from "lucide-react";
import { cn } from "@/lib/utils";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { href: "/careers", label: "Careers", icon: Compass },
  { href: "/resume", label: "Resume", icon: FileText },
  { href: "/skill-gap", label: "Skill gaps", icon: Target },
  { href: "/roadmap", label: "Roadmap", icon: Map },
  { href: "/profile", label: "Profile", icon: UserRound }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 shrink-0 border-r bg-muted/30 md:block">
      <nav className="sticky top-16 space-y-1 p-4">
        {items.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground",
                active && "bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground"
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
