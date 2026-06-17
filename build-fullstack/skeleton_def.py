"""Full-Stack Developer Map — taxonomy skeleton.

Sibling to the AI/ML and Software-Engineering maps. Where the SWE map is the
abstract, tool-agnostic foundation, this map is the *focused, practical* view of
the full-stack web developer role: concept nodes as the backbone, with concrete
technologies named in each topic's description (hybrid style).

Defines domains + subdomains. Topics & edges are authored per-domain and merged
by assemble.py. Run this to (re)write skeleton.json.
"""
import json, os

# key, title, color, scope, [(subkey, sublabel), ...]
DOMAINS = [
 ("web-foundations", "How the Web Works", "#0ea5e9",
  "the substrate every web developer stands on: the internet, HTTP, DNS & hosting, how browsers run a page, baseline web security, and the data formats that flow over the wire.",
  [("internet","Internet & Client-Server"),
   ("http","HTTP & HTTPS"),
   ("dns-hosting","DNS, Domains & Hosting"),
   ("browsers","How Browsers Work"),
   ("web-security-basics","Web Security Basics"),
   ("formats","Data Formats & Wire Protocols")]),

 ("frontend-core", "Frontend Foundations — HTML, CSS & JS", "#f97316",
  "the raw materials of the browser UI: semantic HTML, CSS fundamentals & layout, modern CSS, the JavaScript language, the browser/DOM platform, TypeScript, and accessibility.",
  [("html","HTML & Semantics"),
   ("css-fundamentals","CSS Fundamentals"),
   ("css-layout","Layout & Responsive Design"),
   ("css-modern","Modern CSS & Styling"),
   ("javascript","JavaScript Language"),
   ("js-browser","JavaScript in the Browser"),
   ("typescript","TypeScript"),
   ("accessibility","Accessibility (a11y)")]),

 ("frontend-frameworks", "Frontend Frameworks & UI", "#f59e0b",
  "building real UIs at scale: the component/SPA model, React & its ecosystem, the framework landscape, state management, routing, styling approaches, forms, UI/design systems, and rendering strategies.",
  [("spa-model","SPA & Component Model"),
   ("react","React & Ecosystem"),
   ("framework-landscape","Framework Landscape"),
   ("state-management","State Management"),
   ("routing","Client-Side Routing"),
   ("styling","Styling Approaches"),
   ("forms","Forms & Validation"),
   ("ui-systems","UI Libraries & Design Systems"),
   ("rendering","Rendering Strategies & Meta-Frameworks")]),

 ("tooling", "Tooling, Build & Dev Environment", "#eab308",
  "the developer's workbench: package managers, bundlers & build systems, transpilers, linting & formatting, the editor/terminal environment, debugging tools, and monorepo tooling.",
  [("package-managers","Package Managers"),
   ("bundlers","Bundlers & Build Systems"),
   ("transpilers","Transpilers & Compilers"),
   ("linting","Linting & Formatting"),
   ("dev-environment","Editor, Shell & Environment"),
   ("debugging","Debugging Tools"),
   ("monorepo","Monorepos & Workspaces")]),

 ("backend", "Backend Languages & Frameworks", "#10b981",
  "the server side: backend languages, runtimes & app servers, web frameworks, request handling & middleware, server-side rendering/templating, validation & errors, background jobs, and file/media handling.",
  [("languages","Backend Languages"),
   ("runtimes","Runtimes & App Servers"),
   ("frameworks","Web Frameworks"),
   ("request-handling","Request Handling & Middleware"),
   ("templating","Server Rendering & Templating"),
   ("validation-errors","Validation & Error Handling"),
   ("background-jobs","Background Jobs & Scheduling"),
   ("file-handling","File & Media Handling")]),

 ("apis", "APIs & Communication", "#14b8a6",
  "how clients and services talk: REST, API design, GraphQL, RPC/gRPC, real-time channels, API documentation & contracts, and consuming/integrating third-party APIs.",
  [("rest","REST APIs"),
   ("api-design","API Design"),
   ("graphql","GraphQL"),
   ("rpc","RPC & gRPC"),
   ("realtime","Real-Time Communication"),
   ("api-docs","API Documentation & Contracts"),
   ("api-integration","Consuming & Integrating APIs")]),

 ("auth-security", "Authentication & Web Security", "#f43f5e",
  "keeping the app and its users safe: authentication, sessions & tokens, OAuth/SSO, authorization, password & transport cryptography, the OWASP vulnerability classes, and secure-by-default practices.",
  [("authentication","Authentication"),
   ("sessions-tokens","Sessions & Tokens"),
   ("oauth","OAuth, OIDC & SSO"),
   ("authorization","Authorization & Access Control"),
   ("crypto","Passwords, Crypto & TLS"),
   ("vulnerabilities","Web Vulnerabilities (OWASP)"),
   ("secure-practices","Secure-by-Default Practices")]),

 ("databases", "Databases & Data Layer", "#a855f7",
  "where state lives: relational databases, SQL, transactions & integrity, NoSQL stores, ORMs & query builders, data modeling & migrations, caching, and search/object storage.",
  [("relational","Relational Databases"),
   ("sql","SQL"),
   ("transactions","Transactions & Integrity"),
   ("nosql","NoSQL Databases"),
   ("orms","ORMs & Query Builders"),
   ("data-modeling","Data Modeling & Migrations"),
   ("caching","Caching"),
   ("search-storage","Search & Object Storage")]),

 ("testing", "Testing & Quality", "#84cc16",
  "confidence that it works: testing fundamentals, unit testing, mocking & test doubles, integration testing, end-to-end testing, frontend testing, testing practices, and code-quality tooling.",
  [("fundamentals","Testing Fundamentals"),
   ("unit","Unit Testing"),
   ("mocking","Mocking & Test Doubles"),
   ("integration","Integration Testing"),
   ("e2e","End-to-End Testing"),
   ("frontend-testing","Frontend Testing"),
   ("practices","Testing Practices"),
   ("quality-tooling","Code-Quality Tooling")]),

 ("devops", "DevOps, CI/CD & Deployment", "#8b5cf6",
  "shipping and running it: CI/CD pipelines, containers, orchestration & scaling, hosting platforms, cloud providers, serverless & edge, web servers/networking, and infrastructure & configuration.",
  [("ci-cd","CI/CD Pipelines"),
   ("containers","Containers"),
   ("orchestration","Orchestration & Scaling"),
   ("hosting","Hosting & PaaS Platforms"),
   ("cloud","Cloud Providers"),
   ("serverless","Serverless, Edge & BaaS"),
   ("web-servers","Web Servers & Networking"),
   ("infra-config","Infrastructure & Configuration")]),

 ("architecture", "Architecture & Code Quality", "#3b82f6",
  "structuring code that lasts: clean code, design principles, design patterns, project structure, application architecture, system-design basics, and refactoring & technical debt.",
  [("clean-code","Clean Code"),
   ("principles","Design Principles"),
   ("patterns","Design Patterns"),
   ("project-structure","Project Structure"),
   ("app-architecture","Application Architecture"),
   ("system-design","System Design Basics"),
   ("refactoring","Refactoring & Tech Debt")]),

 ("performance", "Performance & Observability", "#d946ef",
  "making it fast and watching it run: web performance, frontend optimization, backend performance, caching strategies, scaling & load, monitoring & metrics, logging & tracing, and error tracking.",
  [("web-vitals","Web Performance & Vitals"),
   ("frontend-perf","Frontend Optimization"),
   ("backend-perf","Backend Performance"),
   ("caching-strategies","Caching Strategies"),
   ("scaling","Scaling & Load"),
   ("monitoring","Monitoring & Metrics"),
   ("logging-tracing","Logging & Tracing"),
   ("error-tracking","Error Tracking")]),

 ("foundations", "CS Foundations for Daily Work", "#6366f1",
  "the computer-science you actually reach for: core data structures, everyday algorithms, complexity & Big-O, networking basics, concurrency & async, and problem-solving/interview patterns.",
  [("data-structures","Data Structures"),
   ("algorithms","Algorithms"),
   ("complexity","Complexity & Big-O"),
   ("networking","Networking Basics"),
   ("concurrency","Concurrency & Async"),
   ("problem-solving","Problem Solving & Patterns")]),

 ("professional", "Collaboration & Professional Skills", "#ef4444",
  "working as a developer among developers: version control, Git collaboration, agile process, documentation, communication & teamwork, career growth, and AI-assisted development.",
  [("version-control","Version Control (Git)"),
   ("git-collaboration","Git Collaboration & PRs"),
   ("agile","Agile & Process"),
   ("documentation","Documentation"),
   ("communication","Communication & Teamwork"),
   ("career","Career & Growth"),
   ("ai-assisted","AI-Assisted Development")]),
]

def build():
    domains = [{"key":k, "title":t, "color":c, "scope":s} for (k,t,c,s,subs) in DOMAINS]
    subdomains = []
    for (k,t,c,s,subs) in DOMAINS:
        for (subk, subl) in subs:
            subdomains.append({"domain":k, "key":subk, "label":subl})
    return {"domains":domains, "subdomains":subdomains}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    skel = build()
    with open(os.path.join(here,"skeleton.json"),"w") as f:
        json.dump(skel, f, indent=1)
    nd=len(skel["domains"]); ns=len(skel["subdomains"])
    print(f"wrote skeleton.json: {nd} domains, {ns} subdomains")
    for d in skel["domains"]:
        cnt=sum(1 for s in skel["subdomains"] if s["domain"]==d["key"])
        print(f"  {d['key']:20} {d['title']:42} {cnt} subdomains")
