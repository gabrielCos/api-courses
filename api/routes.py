from fastapi import APIRouter
from fastapi import HTTPException
import contextlib
from bson import ObjectId
from db import db

router = APIRouter()

@router.get('/courses')
def get_courses(sort_by: str = 'date', domain: str = None):
    
    #types of sorting and order 
    if sort_by == 'date':
        sort_field = 'date'
        sort_order = -1
    elif sort_by == 'rating':
        sort_field = 'rating.total'
        sort_order = -1
    else:  
        sort_field = 'name'
        sort_order = 1
        
    query = {}
    if domain:
        query['domain'] = domain
    
    #search for the couses in the data base
    courses = list(db.courses.find(query))
    
    #calculating and updating the total course rating 
    for course in courses:
        total = 0
        count = 0
        for chapter in course.get('chapters', []):
            #no interruptions in erros or exceptions 
            with contextlib.suppress(KeyError):
                total += chapter['rating']['total']
                count += chapter['rating']['count']
        db.courses.update_one({'_id': course['_id']}, {'$set': {'rating': {'total': total, 'count': count}}})

    
    #aplying the the order and showing the database
    courses = db.courses.find(
        query, 
        {'name': 1, 'date': 1, 'description': 1, 'domain':1,'rating':1,'_id': 0}
        ).sort(sort_field, sort_order)
    
    return list(courses)

@router.get('/courses/{course_id}')
def get_course(course_id: str):
    course = db.courses.find_one(
        {'_id' : ObjectId(course_id)}, #search for id 
        {'_id': 0, 'chapters': 0} #show the result whitout the id and chapters fields
    )
    # returns error 404 if dont find the course
    if not course:
        raise HTTPException(status_code = 404, detail='Course not found')
    try:
        course['rating'] = course['rating']['total'] # try to access the rating field
    except:
        course['rating'] = 'Not rated yet' #if does not exist, shows a message
    
    return course

@router.get('courses/{course_id}/{chapter_id}')
def get_chapter(course_id: str, chapter_id: str):
    course = db.courses.find_one(
        {'_id' : ObjectId(course_id)}, 
        {'_id': 0, } #excludes the id field of the projection
    )
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    #gets the list of chapters or a empity list
    chapters = course.get('chapters', [])
    
    try:
        # Try to access the chapter by index converted to integer
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        # if the index is not a valid integer, return this message
        raise HTTPException(status_code=404, detail="Chapter not found") from e
    
    return chapter