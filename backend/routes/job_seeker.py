from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
from utils.db import db

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(user_id: str, resume: UploadFile = File(...)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    content = await resume.read()  
    filename = f"{user_id}_resume.pdf"
    
    with open(f"resumes/{filename}", "wb") as file:
        file.write(content)

    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"resume": filename}})
    
    return {"message": "Resume uploaded successfully", "filename": filename}


@router.get("/search_jobs")
async def search_jobs(skill: str = None, location: str = None, title: str = None):
    """
    Retrieve a list of job postings filtered by skill, location, or title.
    """
    query = {}
    if skill:
        query["skills"] = {"$regex": skill, "$options": "i"} 
        query["location"] = {"$regex": location, "$options": "i"}  
    if title:
        query["title"] = {"$regex": title, "$options": "i"} 

    jobs = list(db.jobs.find(query).limit(100))

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found matching the criteria")
    for job in jobs:
        job["_id"] = str(job["_id"])

    return {"jobs": jobs}

@router.get("/apply")    
async def apply_for_job(job_id: str , user_id:str):
    print(job_id)
    print(user_id)
    job =  db.jobs.find_one({"job_id": job_id})
    user =  db.users.find_one({"user_id": user_id})
    application = {
        "job_id": job_id, 
        "user_id": user_id,
        "status":"applied"
    }
    db.applications.insert_one(application)

    return {"message": "Application submitted successfully"}
# @router.get("/apply")    
# async def apply_for_job(job_id: str, user_id: str):
#     print(job_id, user_id)
#     user =  db.users.find_one({"_id": ObjectId(user_id)})
#     job = db.jobs.find_one({"job_id": job_id})
#     if not user or not job:
#         raise HTTPException(status_code=404, detail="User  or job not found")
    
#     application = {
#         "job_id": job_id,
#         "user_id": user_id,
#         "status": "Applied"
#     }
#     db.applications.insert_one(application)

#     return {"message": "Application submitted successfully"}

@router.get("/applications")
async def get_applications(user_id:str):
    applications = list(db.applications.find({"user_id": user_id}))
    application_list = []
    for i in applications:
        job = i["job_id"]
        if job:
            application_list.append(job)

    if len(application_list) > 0 :
        applied_jobs_list = []
        for jobs in application_list:
            applied_jobs = db.jobs.find({"job_id": jobs},{ "_id": 0 })
            applied_jobs_list.extend(applied_jobs)
        return {"applied_list" : applied_jobs_list}

 
