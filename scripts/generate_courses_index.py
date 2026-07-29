#!/usr/bin/env python3
"""Scan TeachingApp/<category>/*-lesson-*.html, copy them into webapp/lessons/,
and emit webapp/courses.json. Mirrors the category/title parsing rules that
HTMLScannerService.parseCourseMetadata used in the iOS app, so course IDs and
titles stay stable across the native -> PWA migration.
"""
import json
import os
import re
import shutil
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_ROOT = os.path.join(REPO_ROOT, "TeachingApp")
WEBAPP_ROOT = os.path.join(REPO_ROOT, "webapp")
LESSONS_OUT = os.path.join(WEBAPP_ROOT, "lessons")
COURSES_JSON = os.path.join(WEBAPP_ROOT, "courses.json")

LESSON_PATTERN = re.compile(r"^(?P<category>[a-zA-Z0-9]+)-lesson-(?P<number>\d+)\.html$")


def parse_course_metadata(filename):
    match = LESSON_PATTERN.match(filename)
    if not match:
        return None
    category_raw = match.group("category")
    number = match.group("number")
    category = category_raw.replace("-", " ").title()
    title = f"{category} Lesson {number}"
    return category, title, int(number)


def main():
    if not os.path.isdir(SOURCE_ROOT):
        print(f"Source root not found: {SOURCE_ROOT}", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(LESSONS_OUT):
        shutil.rmtree(LESSONS_OUT)
    os.makedirs(LESSONS_OUT, exist_ok=True)

    courses = []
    for entry in sorted(os.listdir(SOURCE_ROOT)):
        subdir = os.path.join(SOURCE_ROOT, entry)
        if not os.path.isdir(subdir):
            continue
        for filename in sorted(os.listdir(subdir)):
            if not filename.endswith(".html"):
                continue
            metadata = parse_course_metadata(filename)
            if metadata is None:
                continue
            category, title, number = metadata
            category_slug = category.lower().replace(" ", "-")

            dest_dir = os.path.join(LESSONS_OUT, category_slug)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(os.path.join(subdir, filename), os.path.join(dest_dir, filename))

            course_id = filename.replace(".html", "")
            courses.append({
                "id": course_id,
                "title": title,
                "category": category,
                "categorySlug": category_slug,
                "fileName": filename,
                "path": f"lessons/{category_slug}/{filename}",
                "number": number,
                "generatedDate": None,
            })

    courses.sort(key=lambda c: (c["category"], c["number"]))

    with open(COURSES_JSON, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(courses)} courses to {COURSES_JSON}")


if __name__ == "__main__":
    main()
