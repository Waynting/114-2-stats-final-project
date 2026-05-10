import sys

COSTS = {
    "search.list": 100,
    "videos.list": 1,
    "channels.list": 1,
    "playlistItems.list": 1,
    "commentThreads.list": 1,
    "comments.list": 1,
    "videoCategories.list": 1,
}


class QuotaBudgetExceeded(Exception):
    pass


class QuotaTracker:
    def __init__(self, budget=8000, verbose=True):
        self.budget = budget
        self.used = 0
        self.calls = {}
        self.verbose = verbose

    def charge(self, endpoint):
        cost = COSTS.get(endpoint, 1)
        if self.used + cost > self.budget:
            raise QuotaBudgetExceeded(
                f"Budget exceeded: used={self.used}, +{cost} for {endpoint}, budget={self.budget}"
            )
        self.used += cost
        self.calls[endpoint] = self.calls.get(endpoint, 0) + 1
        if self.verbose:
            print(f"[quota] {endpoint} +{cost} -> {self.used}/{self.budget}", file=sys.stderr)
        return self.used

    def estimate(self, plan):
        return sum(COSTS.get(ep, 1) * n for ep, n in plan.items())

    def report(self):
        lines = [f"Quota used: {self.used}/{self.budget}"]
        for ep, n in sorted(self.calls.items()):
            lines.append(f"  {ep}: {n} calls = {COSTS.get(ep, 1) * n} units")
        return "\n".join(lines)
