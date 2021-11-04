#!/usr/bin/env python3

import streamlit as st
import yaml

st.title('Config Generator')

st.header('Add Classes')
numClasses = st.number_input("Number of Classes", 1)

classes = list()
for i in range(numClasses):
    st.subheader("Class "+str(i+1))
    className = st.text_input("Class Name (Required)", key=i)
    classRoom = st.text_input("Class Room", key=i)
    classTeacher = st.text_input("Class Teacher", key=i)
    classes.append({'name': className, 'classroom': classRoom, 'teacher': classTeacher})

listOfNames = [classes[i]["name"] for i in range(numClasses)]
listOfNames.append('Free')

st.header('Add Timetable')
numDays = st.number_input("Number of Days in Timetable", 1)

timetable = list()
for i in range(numDays):
    timetable.append(st.multiselect("Classes for day "+str(i+1), listOfNames))

st.header('Additional Configurations')
if st.checkbox("Weekends"):
    weekend = st.multiselect("Choose weekend", ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
else:
    weekend = ["Saturday", "Sunday"]

st.header('Generate')

output = {'classes': classes, 'timetable': timetable, 'weekend': weekend}
st.download_button("Download configuration file", yaml.dump(output), "config.yaml", "application/x-yaml")
