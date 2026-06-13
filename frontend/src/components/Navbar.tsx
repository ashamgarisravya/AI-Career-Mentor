"use client";

import Link from "next/link";
import { useTheme } from "next-themes";
import { BriefcaseBusiness, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
  const { theme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-30 border-b bg-background/90 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 md:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className="grid h-9 w-9 place-items-center rounded-md bg-primary text-primary-foreground">
            <BriefcaseBusiness className="h-5 w-5" />
          </span>
          AI Career Builder
        </Link>
        <nav className="hidden items-center gap-5 text-sm text-muted-foreground md:flex">
          <Link href="/dashboard" className="hover:text-foreground">Dashboard</Link>
          <Link href="/careers" className="hover:text-foreground">Careers</Link>
          <Link href="/resume" className="hover:text-foreground">Resume</Link>
          <Link href="/roadmap" className="hover:text-foreground">Roadmap</Link>
        </nav>
        <Button
          variant="outline"
          size="icon"
          aria-label="Toggle dark mode"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          <Sun className="h-4 w-4 dark:hidden" />
          <Moon className="hidden h-4 w-4 dark:block" />
        </Button>
      </div>
    </header>
  );
}
