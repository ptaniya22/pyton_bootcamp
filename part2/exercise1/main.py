import asyncio
import os
from pathlib import Path
from urllib.parse import urlparse
from requests import get
from requests.exceptions import RequestException



def check_directory(path_str):
    path = Path(path_str)

    try:
        if path.exists() and not path.is_dir():
            print("ERROR!Your path is not directory.It's file")
            return None

        path.mkdir(parents=True, exist_ok=True)

        test_file = path / "test.tmp"
        with open(test_file, "wb") as f:
            f.write(b"test")

        test_file.unlink()
        return path

    except PermissionError:
        print("Permission Error")
        return None
    except OSError:
        print("Incorrect Path")
        return None
# check_directory('test')  

def make_filename(url, index):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # protection e.g. https://site.com/image/
    # https://site.com/image/image_index.jpg
    if not filename:
        filename = f"image_{index}.jpg"

    # print(parsed_url.scheme)
    # print(parsed_url.netloc)
    # print(parsed_url.path)
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = ".jpg"
    return f"{name}_{index}{ext}"
# print(make_filename("https://example.com/images/",1))


def download_image(url, save_dir, index):

    try:
        filename = make_filename(url, index)
        file_path = save_dir / filename
        # print(f"Начало загрузки: {filename}")
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = get(url, headers=headers, timeout=(5, 10))
                
        # print(url, response.status_code, response.headers.get("Content-Type"))
        # ***200-success
        # ***404-file not found
        # ***403-access denied
        # ***500-server error
        # print("content_type: ",response.headers.get("Content-Type", ""))

        if response.status_code != 200:
            return {"url": url, "status": "Ошибка"}

        content_type = response.headers.get("Content-Type", "")        
        if "image" not in content_type.lower():
            return {"url": url, "status": "Ошибка"}

        with open(file_path, "wb") as f:
            f.write(response.content)

        # print(f"Конец загрузки: {filename}")
        # print("response.content: ",response.content)
        return {"url": url, "status": "Успех"}

    except RequestException:
        return {"url": url, "status": "Ошибка"}
    except OSError:
        return {"url": url, "status": "Ошибка"}

def print_table(results):
    if not results:
        print("Empty query. No links")
        return

    max_url_len = max(len(r["url"]) for r in results)
    max_url_len = max(max_url_len, len("Ссылка"))

    max_status_len = max(len(r["status"]) for r in results)
    max_status_len = max(max_status_len, len("Статус"))

    line = "+" + "-"*(max_url_len + 2) + "+" + "-"*(max_status_len + 2) + "+"

    print(line)
    print(f"| {'Ссылка':<{max_url_len}} | {'Статус':<{max_status_len}} |")
    print(line)

    for r in results:
        print(f"| {r['url']:<{max_url_len}} | {r['status']:<{max_status_len}} |")

    print(line) 



async def process_url(url, save_dir, index):
    return await asyncio.to_thread(download_image, url, save_dir, index)

async def main():
    while True:
        # print("Enter path")
        path_str = input().strip()
        save_dir = check_directory(path_str)
        if save_dir is not None:
            break

    tasks = []
    index = 1

    while True:
        # print("Enter link")
        url = input().strip()
        if url == "":
            break

        task = asyncio.create_task(process_url(url, save_dir, index))
        tasks.append(task)
        index += 1

    if any(not task.done() for task in tasks):
        print("Not all images have been uploaded yet. Please wait for completion...")

    results = await asyncio.gather(*tasks)
    print("Сводка об успешных и неуспешных загрузках")
    print_table(results)

    
if __name__ == "__main__":
    asyncio.run(main())

# download_image("https://sun9-83.userapi.com/c909328/u742493691/d9/-3/x_9949b483bb.jpg",Path("test"),3)
# print(download_image("https://sun9-83.userapi.com/c909328/u742493691/d9/-3/x_9949b483b.jpg",Path("test"),3))