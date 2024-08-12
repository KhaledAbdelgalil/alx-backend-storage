#!/usr/bin/env python3
"""
students
"""


def top_students(mongo_collection):
    """ students by score """
    return mongo_collection.aggregate([
        {
            "$studentGroup":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])