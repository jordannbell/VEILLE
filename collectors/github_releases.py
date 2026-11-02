import sys

import httpx

from common import save_items

REPOS = ["symfony/symfony", "docker/compose", "grafana/grafana"]


def fetch_releases(repo):
    url = f"https://api.github.com/repos/{repo}/releases"
    response = httpx.get(url, params={"per_page": 5}, timeout=10)
    response.raise_for_status()
    return response.json()


def to_item(repo, release):
    return {
        "source": f"github:{repo}",
        "kind": "release",
        "external_id": str(release["id"]),
        "title": f"{repo} {release['tag_name']}",
        "url": release["html_url"],
        "published_at": release["published_at"],
        "summary": (release.get("body") or "")[:500],
        "tags": [repo.split("/")[1], "release"],
    }


def main():
    items = []
    failures = 0

    for repo in REPOS:
        try:
            for release in fetch_releases(repo):
                if release["draft"]:
                    continue
                items.append(to_item(repo, release))
        except httpx.HTTPError as exc:
            failures += 1
            print(f"[N1] echec source github:{repo} : {exc}", file=sys.stderr)

    save_items(items)
    print(f"{len(items)} elements deposes, {failures} source(s) en echec")
    if failures == len(REPOS):
        sys.exit(1)


if __name__ == "__main__":
    main()
