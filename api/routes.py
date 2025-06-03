from fastapi import APIRouter
import contextlib
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
