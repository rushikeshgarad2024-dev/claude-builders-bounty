# Next.js 15 + SQLite SaaS Engineering Guidelines

Welcome to the Next.js 15 App Router + SQLite SaaS production project. This document defines the exact architecture, coding standards, database conventions, and anti-patterns required for all AI and human developers.

---

## 1. Stack & Versions
- **Framework**: Next.js 15 (App Router, Server Components by default)
- **Runtime / Language**: Node.js 22 LTS / TypeScript 5.x (Strict mode enabled)
- **Database**: SQLite 3 via `better-sqlite3` (Local / Embedded) or Turso (`@libsql/client`) for edge deployment
- **ORM / Query Builder**: `drizzle-orm` with `drizzle-kit` for zero-overhead type-safe SQL
- **Styling**: Tailwind CSS v4 + `shadcn/ui` (Radix UI primitives) + `lucide-react`
- **Validation**: `zod` for all runtime schema, form, and API validation
- **Auth**: Iron Session / Lucia Auth / Auth.js with secure HTTP-only session cookies

---

## 2. Directory & File Organization
```
├── app/                      # Next.js 15 App Router
│   ├── (auth)/               # Route group for login, signup, reset password
│   ├── (dashboard)/          # Authenticated app shell with persistent layouts
│   │   ├── dashboard/
│   │   ├── settings/
│   │   └── billing/
│   ├── api/                  # Webhook endpoints (Stripe, GitHub) ONLY
│   ├── layout.tsx            # Global root layout with theme & session providers
│   └── page.tsx              # Public marketing landing page
├── components/               # React Components
│   ├── ui/                   # Reusable atomic primitive components (Button, Input)
│   ├── forms/                # Client form wrappers with Zod validation
│   └── navigation/           # Navbar, Sidebar, Breadcrumbs
├── lib/                      # Core business logic & utilities
│   ├── db/                   # Database client, connection pool, pragma configuration
│   │   ├── index.ts          # SQLite singleton connection with WAL mode
│   │   └── schema.ts         # Drizzle schema definitions
│   ├── actions/              # Server Actions ('use server') for all data mutations
│   ├── auth/                 # Session management, hashing, RBAC helpers
│   └── utils.ts              # cn() class merger, date formatters, currency helpers
├── migrations/               # Numbered SQL migration files (e.g. 0001_init.sql)
├── drizzle.config.ts         # Drizzle kit migration configuration
└── next.config.ts            # Next.js compiler & security headers configuration
```

---

## 3. Database & SQLite Best Practices

### Pragmas & Concurrency
Always initialize SQLite with the following mandatory pragmas in `lib/db/index.ts`:
```typescript
import Database from 'better-sqlite3';

const sqlite = new Database(process.env.DATABASE_URL || 'sqlite.db');

// Mandatory SQLite performance & integrity settings
sqlite.pragma('journal_mode = WAL');       // Write-Ahead Logging for high concurrency
sqlite.pragma('synchronous = NORMAL');     // Optimal durability without fsync bottlenecks
sqlite.pragma('foreign_keys = ON');        // Enforce relational referential integrity
sqlite.pragma('busy_timeout = 5000');      // Avoid immediate 'database is locked' errors
sqlite.pragma('cache_size = -20000');      // 20MB in-memory cache allocation
```

### Migration Rules
- Never modify applied migration files (`migrations/*.sql`).
- All schema changes must be generated via `npm run db:generate` and applied via `npm run db:migrate`.
- Include foreign key indexes explicitly on all relational references to prevent full table scans.
- Use ULIDs or UUIDv7 strings for primary keys to maintain chronological insertion ordering and index locality.

---

## 4. Component & Server Action Patterns

### Server vs Client Separation
- **Default to Server Components**: Keep page loads instant, fetch data directly from SQLite in the server component without REST/GraphQL boilerplate.
- **Client Components (`'use client'`)**: Only use when browser event listeners (`onClick`, `onChange`), React state (`useState`, `useReducer`), or browser APIs are required.

### Mutation Pattern: Server Actions with Zod
Never perform mutations via custom API routes. Use Next.js Server Actions with strict Zod validation:
```typescript
'use server';

import { z } from 'zod';
import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

const CreateProjectSchema = z.object({
  name: z.string().min(3).max(50),
  description: z.string().optional()
});

export async function createProjectAction(prevState: any, formData: FormData) {
  const parsed = CreateProjectSchema.safeParse({
    name: formData.get('name'),
    description: formData.get('description')
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors, success: false };
  }

  await db.insert(projects).values(parsed.data);
  revalidatePath('/dashboard');
  return { success: true };
}
```

---

## 5. Development & Production Commands
- `npm run dev`: Start Next.js dev server with Turbo (`next dev --turbo`)
- `npm run build`: Typecheck and produce production standalone build
- `npm run db:generate`: Generate new SQL migration from `lib/db/schema.ts`
- `npm run db:migrate`: Run pending migrations against SQLite database
- `npm run db:studio`: Launch Drizzle visual database inspector
- `npm run test`: Run Vitest unit & action tests

---

## 6. What We NEVER Do (And Why)

1. **NO Raw Unprepared SQL Queries with String Interpolation**
   - *Why*: Prevents SQL injection vulnerabilities. Always use Drizzle prepared statements or parameterized queries.
2. **NO Client-Side Data Fetching (`useEffect` + `fetch`) for Initial Page Loads**
   - *Why*: Causes waterfall network delays and UI layout shifts. Fetch directly in Server Components.
3. **NO Default Component Exports for UI Primitives**
   - *Why*: Named exports ensure refactoring safety and prevent naming drift across imports.
4. **NO Storing Sensitive Secrets in `.env` without `.env.example`**
   - *Why*: Prevents secret leakage and ensures clean onboarding for team members.
5. **NO Unindexed Foreign Keys in SQLite Tables**
   - *Why*: SQLite does not auto-create indexes on foreign key columns, causing table locks during cascading deletions.
