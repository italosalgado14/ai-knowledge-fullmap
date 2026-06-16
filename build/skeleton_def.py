"""Software Engineering Knowledge Map — taxonomy skeleton.

Defines domains + subdomains. Topics & edges are authored per-domain by
subagents and merged by assemble.py. Run this to (re)write skeleton.json.
"""
import json, os

# key, title, color, scope, [(subkey, sublabel), ...]
DOMAINS = [
 ("prog", "Programming Languages & Paradigms", "#6366f1",
  "programming paradigms; type systems; syntax & semantics; memory & resource management; core language features; metaprogramming & reflection; runtimes & execution models; language families & idioms.",
  [("paradigms","Programming Paradigms"),
   ("type-systems","Type Systems"),
   ("language-semantics","Syntax & Semantics"),
   ("memory-model","Memory & Resource Management"),
   ("lang-features","Core Language Features"),
   ("metaprogramming","Metaprogramming & Reflection"),
   ("runtime","Runtimes & Execution Models"),
   ("lang-families","Language Families & Idioms")]),

 ("dsa", "Data Structures & Algorithms", "#14b8a6",
  "complexity & analysis; linear structures; trees & heaps; graphs; algorithm design techniques; sorting & searching; string algorithms; advanced & specialized algorithms.",
  [("complexity","Complexity & Analysis"),
   ("linear-ds","Linear Structures"),
   ("trees","Trees & Heaps"),
   ("graphs-ds","Graph Structures & Algorithms"),
   ("algo-design","Algorithm Design Techniques"),
   ("sorting-searching","Sorting & Searching"),
   ("strings","String Algorithms"),
   ("advanced-algo","Advanced & Specialized Algorithms")]),

 ("systems", "Computer Architecture & Compilers", "#ec4899",
  "digital logic & hardware; CPU architecture; memory hierarchy; assembly & machine code; compiler front end; compiler back end; linking, loading & binaries; hardware performance.",
  [("digital-logic","Digital Logic & Hardware"),
   ("cpu-arch","CPU Architecture"),
   ("memory-hierarchy","Memory Hierarchy"),
   ("assembly","Assembly & Machine Code"),
   ("compilers-frontend","Compiler Front End"),
   ("compilers-backend","Compiler Back End"),
   ("linking-loading","Linking, Loading & Binaries"),
   ("perf-arch","Hardware Performance")]),

 ("os", "Operating Systems & Concurrency", "#f59e0b",
  "processes & threads; CPU scheduling; memory management; concurrency primitives; synchronization & hazards; inter-process communication; file systems & I/O; parallel & async models.",
  [("processes","Processes & Threads"),
   ("scheduling","CPU Scheduling"),
   ("memory-mgmt","Memory Management"),
   ("concurrency","Concurrency Primitives"),
   ("sync-problems","Synchronization & Hazards"),
   ("ipc","Inter-Process Communication"),
   ("filesystems","File Systems & I/O"),
   ("parallelism","Parallel & Async Models")]),

 ("net", "Networking & Protocols", "#22c55e",
  "network models; link & physical layer; network layer & routing; transport layer; application protocols; HTTP & web transport; network security; network programming & tools.",
  [("net-models","Network Models"),
   ("link-physical","Link & Physical Layer"),
   ("ip-routing","Network Layer & Routing"),
   ("transport","Transport Layer"),
   ("app-protocols","Application Protocols"),
   ("http-deep","HTTP & Web Transport"),
   ("net-security","Network Security"),
   ("net-tools","Network Programming & Tools")]),

 ("data", "Databases & Data Management", "#a855f7",
  "relational model; SQL; transactions & concurrency; indexing & storage engines; query processing & optimization; NoSQL & alternative models; data modeling & design; data engineering & warehousing.",
  [("relational","Relational Model"),
   ("sql","SQL"),
   ("transactions","Transactions & Concurrency"),
   ("indexing-storage","Indexing & Storage Engines"),
   ("query-optimization","Query Processing & Optimization"),
   ("nosql","NoSQL & Alternative Models"),
   ("data-modeling","Data Modeling & Design"),
   ("data-pipelines","Data Engineering & Warehousing")]),

 ("distributed", "Distributed Systems", "#ef4444",
  "fundamentals (failure, time, CAP); consistency models; consensus & coordination; replication & partitioning; messaging & streaming; distributed data; fault tolerance & resilience; distributed patterns.",
  [("dist-fundamentals","Fundamentals"),
   ("consistency","Consistency Models"),
   ("consensus","Consensus & Coordination"),
   ("replication","Replication & Partitioning"),
   ("messaging","Messaging & Streaming"),
   ("dist-data","Distributed Data"),
   ("fault-tolerance","Fault Tolerance & Resilience"),
   ("dist-patterns","Distributed Patterns")]),

 ("arch", "Software Design & Architecture", "#3b82f6",
  "design principles; design patterns; architectural styles; domain-driven design; API & interface design; modularity & components; quality attributes; refactoring & evolution.",
  [("design-principles","Design Principles"),
   ("design-patterns","Design Patterns"),
   ("arch-styles","Architectural Styles"),
   ("ddd","Domain-Driven Design"),
   ("api-design","API & Interface Design"),
   ("modularity","Modularity & Components"),
   ("arch-quality","Quality Attributes"),
   ("refactoring","Refactoring & Evolution")]),

 ("web", "Web & Frontend Engineering", "#f97316",
  "web fundamentals; HTML & CSS; JavaScript & the platform; component frameworks; state & data management; rendering & delivery; performance & accessibility; modern web platform.",
  [("web-fundamentals","Web Fundamentals"),
   ("html-css","HTML & CSS"),
   ("js-frontend","JavaScript & the Platform"),
   ("frontend-frameworks","Component Frameworks"),
   ("state-data","State & Data Management"),
   ("rendering-strategies","Rendering & Delivery"),
   ("web-perf-a11y","Performance & Accessibility"),
   ("web-platform","Modern Web Platform")]),

 ("backend", "Backend & API Engineering", "#10b981",
  "server architecture; REST & HTTP APIs; RPC & GraphQL; authentication & authorization; caching & performance; async & background work; microservices & integration; backend data access.",
  [("server-arch","Server Architecture"),
   ("rest-apis","REST & HTTP APIs"),
   ("rpc-graphql","RPC & GraphQL"),
   ("auth","Authentication & Authorization"),
   ("caching-be","Caching & Performance"),
   ("async-be","Async & Background Work"),
   ("microservices","Microservices & Integration"),
   ("backend-data","Backend Data Access")]),

 ("devops", "DevOps, CI/CD & Infrastructure", "#8b5cf6",
  "CI/CD pipelines; build systems & dependency management; containers & images; container orchestration; infrastructure as code; configuration & secrets; deployment strategies; release & artifact management.",
  [("cicd","CI/CD Pipelines"),
   ("build-systems","Build Systems & Dependencies"),
   ("containers","Containers & Images"),
   ("orchestration","Container Orchestration"),
   ("iac","Infrastructure as Code"),
   ("config-mgmt","Configuration & Secrets"),
   ("deployment","Deployment Strategies"),
   ("release","Release & Artifact Management")]),

 ("cloud", "Cloud & Platform Engineering", "#06b6d4",
  "cloud service models; compute; cloud storage; cloud networking; serverless & event-driven; site reliability engineering; reliability & resilience; cost & governance.",
  [("cloud-models","Cloud Service Models"),
   ("cloud-compute","Compute"),
   ("cloud-storage","Cloud Storage"),
   ("cloud-networking","Cloud Networking"),
   ("serverless","Serverless & Event-Driven"),
   ("sre","Site Reliability Engineering"),
   ("reliability","Reliability & Resilience"),
   ("cloud-cost","Cost & Governance")]),

 ("security", "Security Engineering", "#f43f5e",
  "security fundamentals; cryptography; application security; identity & access; network & infra security; secure development; security operations; data protection & privacy.",
  [("sec-fundamentals","Security Fundamentals"),
   ("cryptography","Cryptography"),
   ("appsec","Application Security"),
   ("authn-authz","Identity & Access"),
   ("network-sec","Network & Infra Security"),
   ("secure-coding","Secure Development"),
   ("sec-ops","Security Operations"),
   ("data-protection","Data Protection & Privacy")]),

 ("quality", "Testing & Software Quality", "#eab308",
  "testing levels; test design; TDD & BDD; test doubles & isolation; test automation; static analysis & linting; performance & load testing; formal methods & verification.",
  [("testing-levels","Testing Levels"),
   ("test-design","Test Design"),
   ("tdd-bdd","TDD & BDD"),
   ("test-doubles","Test Doubles & Isolation"),
   ("test-automation","Test Automation"),
   ("static-analysis","Static Analysis & Linting"),
   ("perf-testing","Performance & Load Testing"),
   ("formal-methods","Formal Methods & Verification")]),

 ("practice", "Engineering Practice & Process", "#0ea5e9",
  "version control; code review & collaboration; development methodologies; estimation & planning; documentation & communication; code craftsmanship; debugging & troubleshooting; team & career.",
  [("version-control","Version Control"),
   ("code-review","Code Review & Collaboration"),
   ("methodologies","Development Methodologies"),
   ("estimation-planning","Estimation & Planning"),
   ("documentation","Documentation & Communication"),
   ("code-craft","Code Craftsmanship"),
   ("debugging","Debugging & Troubleshooting"),
   ("career-team","Team & Career")]),

 ("perf", "Performance & Observability", "#d946ef",
  "performance fundamentals; profiling & measurement; optimization techniques; caching; scalability; observability; monitoring & alerting; incident & reliability practice.",
  [("perf-fundamentals","Performance Fundamentals"),
   ("profiling","Profiling & Measurement"),
   ("optimization","Optimization Techniques"),
   ("caching-perf","Caching"),
   ("scalability","Scalability"),
   ("observability","Observability"),
   ("monitoring","Monitoring & Alerting"),
   ("incident","Incident & Reliability Practice")]),
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
        print(f"  {d['key']:12} {d['title']:38} {cnt} subdomains")
