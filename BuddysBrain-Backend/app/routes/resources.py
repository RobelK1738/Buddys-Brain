from fastapi import APIRouter, HTTPException, UploadFile, File, APIRouter, Form
from bson import ObjectId
from ..database import collection
from ..models import ResourceModel, ResourceOut
from ..utils.embeddings import get_embedding
from ..utils.objectid import serialize_mongo_doc
from fastapi.responses import JSONResponse
import cloudinary.uploader
from ..utils.cloudary_config import cloudinary
from ..utils.summarization.Document.main import summarize_document
from ..utils.summarization.Image.main import summarize_image
from ..utils.summarization.URL.main import summarize_article, summarize_video
import traceback
import tempfile
import os


router = APIRouter()


@router.post("/resources", response_model=ResourceOut)
async def create_resource(resource: ResourceModel):
    resource_dict = resource.dict()

    media_link = resource_dict.get("media_link")
    media_type = resource_dict.get("media_type")
    summary = None

    try:
        if media_type == "document":
            summary = summarize_article(media_link)
        elif media_type == "image":
            summary = summarize_image(media_link)
        elif media_type == "video":
            summary = summarize_video(media_link)
        elif media_type == "article":
            summary = summarize_article(media_link)
    except Exception as e:
        print("SUMMARY ERROR:", str(e))
        traceback.print_exc()
        summary = resource_dict.get("description")

    resource_dict["summary"] = summary
    resource_dict["embedding"] = get_embedding(summary)

    result = await collection.insert_one(resource_dict)
    created = await collection.find_one({"_id": result.inserted_id})
    return ResourceOut.model_validate(serialize_mongo_doc(created))

@router.post("/resources/bulk", response_model=list[ResourceOut])
async def create_bulk_resources(resources: list[ResourceModel]):
    if len(resources) > 200:
        raise HTTPException(status_code=400, detail="Maximum 100 resources allowed per request")

    resource_dicts = []
    for resource in resources:
        r_dict = resource.dict()
        r_dict["embedding"] = get_embedding(resource.summary or resource.description)
        resource_dicts.append(r_dict)

    result = await collection.insert_many(resource_dicts)
    inserted_ids = result.inserted_ids
    inserted_docs = await collection.find({"_id": {"$in": inserted_ids}}).to_list(length=500)

    return [ResourceOut.model_validate(serialize_mongo_doc(doc)) for doc in inserted_docs]

@router.get("/resources", response_model=list[ResourceOut])
async def get_all_resources():
    resources = await collection.find().to_list(500)
    return [ResourceOut.model_validate(serialize_mongo_doc(r)) for r in resources]

@router.get("/numResources", response_model=int)
async def get_all_resources():
    resources = await collection.find().to_list(500)
    return len(list([ResourceOut.model_validate(serialize_mongo_doc(r)) for r in resources]))

@router.get("/resources/{resource_id}", response_model=ResourceOut)
async def get_resource(resource_id: str):
    resource = await collection.find_one({"_id": ObjectId(resource_id)})
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceOut.model_validate(serialize_mongo_doc(resource))

@router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: str):
    result = await collection.delete_one({"_id": ObjectId(resource_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted"}
@router.post("/upload", response_model=ResourceOut)
async def upload_and_create_resource(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    course: str = Form(...)
):
    try:
        contents = await file.read()
        file_ext = file.filename.split('.')[-1].lower()

        # 🔥 Determine type
        if file_ext in ["pdf", "txt", "doc", "docx", "ppt", "pptx", "xlsx", "csv"]:
            resource_type = "raw"
            media_type = "document"
        elif file.content_type.startswith("image/"):
            resource_type = "image"
            media_type = "image"
        else:
            resource_type = "auto"
            media_type = "document"

        # ✅ Upload to Cloudinary
        result = cloudinary.uploader.upload(
            contents,
            resource_type=resource_type
        )
        media_link = result["secure_url"]

        # 🧠 Always synthesize summary from content
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            if media_type == "document":
                summary = summarize_document(tmp_path)
            elif media_type == "image":
                summary = summarize_image(tmp_path)
            else:
                summary = description  # fallback for unknown types

            os.remove(tmp_path)

        except Exception as e:
            print("SUMMARY ERROR:", str(e))
            traceback.print_exc()
            summary = description

        embedding = get_embedding(summary)

        resource_doc = {
            "title": title,
            "description": description,
            "media_type": media_type,
            "media_link": media_link,
            "course": course,
            "summary": summary,
            "embedding": embedding
        }

        inserted = await collection.insert_one(resource_doc)
        created = await collection.find_one({"_id": inserted.inserted_id})
        return ResourceOut.model_validate(serialize_mongo_doc(created))

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
