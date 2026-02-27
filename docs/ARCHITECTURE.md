# ARCHITECTURE — NATEBJONES

## Purpose
Personal brand platform for Nathan Jones. Central hub for content, portfolio, and public-facing presence under the Resonance Energy empire.

## System Overview
```
[Content Layer] --> [Web Frontend] --> [CDN/Hosting]
[CMS/Backend]  --> [API Gateway]  --> [Analytics]
```

## Components
- **Frontend**: Static site or SPA (Next.js/Hugo) — personal brand pages, blog, portfolio
- **Content API**: Headless CMS or markdown-based content pipeline
- **Analytics**: Traffic and engagement tracking
- **SEO Layer**: Metadata, sitemaps, social cards

## Data Flow
User Request → CDN → Frontend → Content API → Response

## Integration Points
- Resonance Energy parent brand
- Social media syndication
- NCL second brain content pipeline

## Key Decisions
- Statically generated for performance and low cost
- Content managed via markdown + git workflow
- Agent-maintainable documentation structure
