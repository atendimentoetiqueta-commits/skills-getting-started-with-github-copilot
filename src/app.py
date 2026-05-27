"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities
activities.update({
    # Sports-related
    "Soccer Team": {
        "description": "Team practices, drills, and matches against other schools",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, skill development, and intramural tournaments",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },

    # Artistic
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, play production, and stagecraft workshops",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },

    # Intellectual
    "Debate Team": {
        "description": "Structured debate practice and competitions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["elijah@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, guest lectures, and science fairs",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["sophia.science@mergington.edu", "ethan@mergington.edu"]
    }
})

# Added more activities
activities.update({
    # Sports additional
    "Tennis Team": {
        "description": "Practices, singles and doubles matches, and conditioning",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["chris@mergington.edu", "alex@mergington.edu"]
    },
    "Volleyball Team": {
        "description": "Team practices, scrimmages, and regional tournaments",
        "schedule": "Mondays and Thursdays, 4:30 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["natalie@mergington.edu", "zoe@mergington.edu"]
    },

    # Artistic additional
    "Photography Club": {
        "description": "Learn photography techniques and organize exhibitions",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "grace@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Instrumental and vocal ensemble rehearsals and performances",
        "schedule": "Tuesdays, 5:00 PM - 7:00 PM",
        "max_participants": 25,
        "participants": ["sara@mergington.edu", "jack@mergington.edu"]
    },

    # Intellectual additional
    "Math Club": {
        "description": "Problem solving sessions and math competitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["oliver.math@mergington.edu", "hannah@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions and showcases",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["mason@mergington.edu", "ava.robotics@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
