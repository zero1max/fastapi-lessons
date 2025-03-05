from fastapi import FastAPI

app = FastAPI()

videos = {}

@app.post("/api/user/{video_id}/like")
async def like_video(video_id: int):
    if video_id not in videos:
        videos[video_id] = {"likes": 0, "views": 0}
    
    videos[video_id]["likes"] += 1
    
    return {
        "message": "Video yoqdi",
        "video_id": video_id,
        "total_likes": videos[video_id]["likes"]
    }

@app.post("/api/user/{video_id}/viewer")
async def view_video(video_id: int):
    if video_id not in videos:
        videos[video_id] = {"likes": 0, "views": 0}
    
    videos[video_id]["views"] += 1
    
    return {
        "message": "Video ko'rildi",
        "video_id": video_id,
        "total_views": videos[video_id]["views"]
    }
