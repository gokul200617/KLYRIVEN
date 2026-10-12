"""
app/db/seed.py
--------------
Optional database seeder to populate sample published portfolio projects.

Usage:
    python -m app.db.seed
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.project import Project

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INITIAL_PROJECTS = [
    {
        "slug": "smart-evacuation-system",
        "name": "Smart Evac Command",
        "category": "Smart Systems & IoT",
        "summary": "An intelligent, multi-floor smart evacuation system for the entire building that tracks building evacuation status continuously in real time.",
        "description": "We built an entire smart evacuation system for the entire building which tracks the building evacuation status continuously. Deployed live at https://smart-evacuation-system-zf1z.onrender.com, the platform features a multi-floor realtime monitor, live IoT sensor telemetry trend monitoring, floor state distribution tracking, automated incident feeds, and emergency floor control dispatching.",
        "image_urls": [],
        "published": True,
        "display_order": 1,
    },
    {
        "slug": "meridian",
        "name": "Meridian",
        "category": "Brand Identity",
        "summary": "A comprehensive visual identity for an international architecture firm, built around precision and spatial clarity.",
        "description": "Meridian required an authoritative visual language that translated architectural discipline into digital and physical media. We developed a bespoke typographic framework, restrained geometric monogram, and responsive brand guidelines.",
        "image_urls": [],
        "published": True,
        "display_order": 2,
    },
    {
        "slug": "crestline",
        "name": "Crestline",
        "category": "E-commerce",
        "summary": "A bespoke luxury e-commerce platform with editorial product presentation and seamless checkout.",
        "description": "Constructed from the ground up to present limited-run leather goods with art gallery reverence. Integrated custom multi-currency checkout, real-time inventory synchronization, and sub-second page transitions.",
        "image_urls": [],
        "published": True,
        "display_order": 3,
    },
    {
        "slug": "solance",
        "name": "Solance",
        "category": "Digital Strategy & SEO",
        "summary": "Strategic repositioning and digital growth for a premium wellness brand entering international markets.",
        "description": "Through deep market intelligence and semantic keyword architecture, Solance transitioned from a boutique regional offering into a category-defining international wellness presence with compounding organic reach.",
        "image_urls": [],
        "published": True,
        "display_order": 4,
    },
    {
        "slug": "apex-bureau",
        "name": "Apex Bureau",
        "category": "Website Design & Development",
        "summary": "A refined digital presence for a professional services firm, combining authority with approachability.",
        "description": "Full-stack web experience featuring custom editorial layouts, dark mode transitions, and secure client portal integrations, achieving top-decile Core Web Vitals across mobile and desktop.",
        "image_urls": [],
        "published": True,
        "display_order": 5,
    },
    {
        "slug": "verdant",
        "name": "Verdant",
        "category": "Brand Identity",
        "summary": "A considered identity system for a sustainable goods brand, rooted in material honesty and craft.",
        "description": "Developed packaging design, physical collateral guidelines, and digital brand presence reflecting raw botanical purity and strict ecological verification.",
        "image_urls": [],
        "published": True,
        "display_order": 6,
    },
    {
        "slug": "omnis",
        "name": "Omnis",
        "category": "E-commerce",
        "summary": "An editorial-led online store for a lifestyle brand, where shopping feels as considered as the product.",
        "description": "Uniting editorial articles with transactional touchpoints. Developed custom headless storefront architecture and frictionless one-page checkout.",
        "image_urls": [],
        "published": True,
        "display_order": 7,
    },
]


async def seed_projects():
    async with AsyncSessionLocal() as session:
        for pdata in INITIAL_PROJECTS:
            stmt = select(Project).where(Project.slug == pdata["slug"])
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if not existing:
                now = datetime.now(timezone.utc)
                project = Project(
                    id=uuid.uuid4(),
                    slug=pdata["slug"],
                    name=pdata["name"],
                    category=pdata["category"],
                    summary=pdata["summary"],
                    description=pdata["description"],
                    image_urls=pdata["image_urls"],
                    published=pdata["published"],
                    display_order=pdata["display_order"],
                    created_at=now,
                    updated_at=now,
                )
                session.add(project)
                logger.info("Added project: %s", pdata["slug"])
            else:
                logger.info("Project already exists: %s", pdata["slug"])

        await session.commit()
        logger.info("Database seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed_projects())

