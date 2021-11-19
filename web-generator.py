#!/usr/bin/env python3

import streamlit as st
import yaml

st.sidebar.title('Config Generator')

# Uploading and parsing config
inputFile = st.sidebar.file_uploader("Upload yaml config", type=['yaml', 'yml'])

# Enable option to update
if inputFile is not None and st.sidebar.button("Import from file"):
    try:
        st.session_state['data'] = yaml.safe_load(inputFile)

    except yaml.YAMLError as exc:
        if hasattr(exc, 'problem_mark'):
            if exc.context != None:
                st.error('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + ' ' + str(exc.context) +
                    '\nPlease correct data and retry.')
                st.stop()
            else:
                st.error('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + '\nPlease correct data and retry.')
                st.stop()
        else:
            st.error("Something went wrong while parsing yaml file")
            st.stop()

if st.sidebar.button("Delete data") or 'data' not in st.session_state:
    with open('template.yaml') as foo:
        st.session_state['data'] = yaml.safe_load(foo)


st.header('Add Classes')

try:
    numClasses = len(st.session_state.data['classes'])
    numClasses = st.number_input("Number of Classes", max_value=100, min_value=1, value=numClasses)
except KeyError:
    st.error("Classes section in configuration file is broken.")
    st.stop()

if st.checkbox("Show Classes", value=True):
    with st.form(key="classes"):
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

        st.form_submit_button("Save classes")

listOfNames = [i["name"] for i in st.session_state.data['classes']]
listOfNames.append('Free')
listOfNames.append('')

st.header('Add Timetable')
try:
    numCycle = len(st.session_state.data['timetable'])
    numCycle = st.number_input("Number of Days in timetable", min_value=1, max_value=100, value=numCycle)
except KeyError:
    st.error("Timetable section in configuration file is broken.")
    st.stop()

if st.checkbox("Show timetables"):
    with st.form(key="timetable"):

        error = False
        actualNumCycle = len(st.session_state.data['timetable'])

        if numCycle > actualNumCycle:
            for i in range(numCycle - actualNumCycle):
                st.session_state.data['timetable'].append(["", "", "", ""])
        if numCycle < actualNumCycle:
            for i in range(actualNumCycle - numCycle):
                st.session_state.data['timetable'].pop(len(st.session_state.data['timetable'])-1)

        for i in range(numCycle):
            st.session_state.data['timetable'][i] = st.multiselect(f"Timetable for day {i+1}", default=st.session_state.data['timetable'][i], options=listOfNames, key=i)
            if len(st.session_state.data['timetable'][i]) > 4:
                st.warning('Maximum 4 classes per day')
                error = True

        if error is not True:
            st.form_submit_button("Save classes")

st.header('Additional Configurations')
if st.checkbox("Weekends"):
    try:
        st.session_state.data['weekend'] = st.multiselect("Choose weekend", default=st.session_state.data['weekend'], options=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    except KeyError:
        st.session_state.data['weekend'] = ["Saturday", "Sunday"]
else:
    st.session_state.data['weekend'] = ["Saturday", "Sunday"]

st.sidebar.header('Generate')

st.sidebar.download_button("Download configuration file", yaml.dump(st.session_state.data), "config.yaml", "application/x-yaml")

if st.sidebar.checkbox("Preview YAML"):
    st.sidebar.write(st.session_state.data)
