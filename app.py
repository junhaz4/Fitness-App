import random
import streamlit as st
from yt_extractor import get_info
import database as db

@st.cache(allow_output_mutation=True)
def get_workouts():
    # store the data in cache so no need to query the database every time
    # unless the user deletes the data in the database or deletes the cache
    return db.get_all_workouts()

def get_duration_text(duration_s):
    # convert duration to text such that the format is more readable
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text

st.title("Workout App")

menu_options = ("Daily Workout", "All Workouts", "Add Workout")
select = st.sidebar.selectbox("Menu", menu_options)

if select == "All Workouts":
    st.markdown("## All Workouts")
    workouts = get_workouts()
    for workout in workouts:
        url = "https://youtu.be/" + workout["video_id"]
        st.text(workout["title"])
        st.text(f"{workout['channel']} - {get_duration_text(workout['duration'])}")
        delete = st.button('Delete workout', key=workout["video_id"])
        if delete:
            db.delete_workout(workout["video_id"])
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        st.video(url)
    else:
        st.text("no workouts are available")

elif select == "Daily Workout":
    st.markdown("## Daily Workout")
    workouts = get_workouts()
    if not workouts:
        st.text("No workouts in Database!")
    else:
        workout = db.get_daily_workout()
        if not workout:
            workouts = get_workouts()
            idx = random.randint(0,len(workouts)-1)
            workout = workouts[idx]
            db.update_daily_workout(workout, insert=True)
        else:
            workout = workout[0]
        if st.button("Choose another workout"):
            workouts = get_workouts()
            n = len(workouts)
            while n > 1:
                idx = random.randint(0, len(workouts) - 1)
                workout_new = workouts[idx]
                while workout_new['video_id'] == workout['video_id']:
                    idx = random.randint(0, len(workouts) - 1)
                    workout_new = workouts[idx]
                workout = workout_new
                db.update_daily_workout(workout, insert=False)
        url = "https://youtu.be/" + workout["video_id"]
        st.text(workout['title'])
        st.text(f"{workout['channel']} - {get_duration_text(workout['duration'])}")
        st.video(url)

else:
    st.markdown("## Add Workout")
    url = st.text_input('Please enter the video url')
    if url:
        workout_data = get_info(url)
        if workout_data is None:
            st.text("Video url is invalid")
        else:
            st.text(workout_data['title'])
            st.text(workout_data['channel'])
            st.video(url)
            if st.button("Add Workout"):
                db.insert_workout(workout_data)
                st.text("workout video added")
                st.legacy_caching.clear_cache()