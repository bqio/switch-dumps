import re

def remove_removed_threads(threads: list) -> list:
  for idx, thread in enumerate(threads):
    if "\u0423\u0414\u0410\u041b\u0415\u041d\u041e" in thread['title']:
      del threads[idx]
  return threads

def remove_thread_title_tags(threads: list) -> list:
  for idx, _ in enumerate(threads):
    threads[idx]['title'] = re.sub(r'\s?\[.*?\]\s?', '', threads[idx]['title'])
  return threads