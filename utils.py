import requests
from tqdm import tqdm


def download_file_with_progress(url, destination_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB

        with open(destination_path, 'wb') as file, tqdm(
                desc=destination_path,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=block_size):
                bar.update(len(data))
                file.write(data)

        print(f"downloaded... {destination_path}")
    except requests.exceptions.RequestException as e:
        print(f"download err: {e}")
