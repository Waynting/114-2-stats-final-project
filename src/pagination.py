import time

from googleapiclient.errors import HttpError
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential


def _is_transient(exc):
    if not isinstance(exc, HttpError):
        return False
    status = getattr(exc.resp, "status", None)
    if status in (429, 500, 502, 503, 504):
        return True
    return False


retry_on_transient = retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=32),
    reraise=True,
)


@retry_on_transient
def execute(request):
    return request.execute()


def paginate(request_builder, quota=None, endpoint=None, max_pages=None, sleep_s=0.05):
    page = 0
    page_token = None
    while True:
        if quota and endpoint:
            quota.charge(endpoint)
        request = request_builder(page_token)
        resp = execute(request)
        for item in resp.get("items", []):
            yield item
        page_token = resp.get("nextPageToken")
        page += 1
        if not page_token:
            return
        if max_pages and page >= max_pages:
            return
        if sleep_s:
            time.sleep(sleep_s)
