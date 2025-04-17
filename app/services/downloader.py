from app.tasks.worker import process_download_task
from app.schemas.download import DownloadRequest

def start_download(request: DownloadRequest, output_path: str, final_file: str, history_id: int):
    process_download_task.delay(request.dict(), output_path, final_file, history_id)
