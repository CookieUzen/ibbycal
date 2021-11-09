#!/usr/bin/env python3

import streamlit as st
import yaml

st.title('Config Generator')

# Uploading and parsing config
inputFile = st.file_uploader("Upload yaml config", type=['yaml', 'yml'])

# Enable option to update
if inputFile is not None and st.button("Update"):
    st.session_state['data'] = yaml.safe_load(inputFile)
elif st.button("Delete") or 'data' not in st.session_state:
    with open('template.yaml') as foo:
        st.session_state['data'] = yaml.safe_load(foo)

st.header('Add Classes')

numClasses = len(st.session_state.data['classes'])
numClasses = st.number_input("Number of Classes", max_value=100, min_value=1, value=numClasses)

if numClasses > len(st.session_state.data['classes']):
    for i in range(numClasses - len(st.session_state.data['classes'])):
        st.session_state.data['classes'].append({'name': '', 'classroom': '', 'teacher': ''})
elif numClasses < len(st.session_state.data['classes']):
    for i in range(numClasses - len(st.session_state.data['classes'])):
        st.session_state.data['classes'].pop(len(st.session_state.data['classes']-i-1))

for i in range(numClasses):
    st.subheader("Class "+str(i+1))

    st.session_state.data['classes'][i]['name'] = st.text_input("Class Name (Required)", st.session_state.data['classes'][i]['name'], key=i)
    st.session_state.data['classes'][i]['classroom'] = st.text_input("Class Room", st.session_state.data['classes'][i]['classroom'], key=i)
    st.session_state.data['classes'][i]['teacher'] = st.text_input("Class Teacher", st.session_state.data['classes'][i]['teacher'], key=i)

listOfNames = [i["name"] for i in st.session_state.data['classes']]
listOfNames.append('Free')
listOfNames.append('')

st.header('Add Timetable')
numCycle = len(st.session_state.data['timetable'])
numCycle = st.number_input("Number of Days in timetable", min_value=1, max_value=100, value=numCycle)

actualNumCycle = len(st.session_state.data['timetable'])

if numCycle > actualNumCycle:
    for i in range(numCycle - actualNumCycle):
        st.session_state.data['timetable'].append(("", "", "", ""))
if numCycle < actualNumCycle:
    for i in range(actualNumCycle - numCycle):
        st.session_state.data['timetable'].pop(len(st.session_state.data['timetable'])-1)

for i in range(numCycle):
    st.write("timetable for day "+str(i+1))
    for j in range(4):
        st.session_state.data['timetable'][i][j] = st.selectbox("Class "+str(j+1), index=listOfNames.index(st.session_state.data['timetable'][i][j]), options=listOfNames)

st.header('Additional Configurations')
if st.checkbox("Weekends"):
    st.session_state.data['weekend'] = st.multiselect("Choose weekend", default=st.session_state.data['weekend'], options=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
else:
    st.session_state.data['weekend'] = ["Saturday", "Sunday"]

st.header('Generate')

if st.checkbox("Preview YAML"):
    st.write(st.session_state.data)

st.download_button("Download configuration file", yaml.dump(st.session_state.data), "config.yaml", "application/x-yaml")
