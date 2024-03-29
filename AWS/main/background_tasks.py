import os

# remove temp files create during inference as Background task
async def cleanup(path_list):
    for path in path_list:
        try:
            os.remove(path)
        except OSError:
            pass