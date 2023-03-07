/**
 * @jest-environment jsdom
*/
const fs = require('fs');
console.log("env:", process.env.JEST_ENVIRONMENT)
const http = require("https");
const path = require("path");

const mockFn = (oldfnName, newfnName, scriptstr) => {
    let modifiedScript = scriptstr.replaceAll(oldfnName, newfnName)
    modifiedScript += ` function ${oldfnName}{ return true; }`
    return modifiedScript
}

const cleanMsg = (msg) => {
    return msg.replace(",", "; ").replace("\n", "; ")
}

describe("testing lab5", () => {

    // ------------SETUP-------------
    
    let Soup = require('jssoup').default
    const bootstrap = require('bootstrap')
    const fileP = process.env.JEST_ENVIRONMENT
    const filePath = fileP.replaceAll("\\", "\\\\")
    const submissionName = process.env.SUBMISSION_NAME
    // checking dir structure for all possible spellings of Calendar :P
    const labFiles = [{
        file: path.join('Calendar', 'resources', 'js', 'script.js'),
        altFile1: path.join('Calender', 'resources', 'js', 'script.js'),
        altFile2: path.join('Calander', 'resources', 'js', 'script.js'),
        points: 3
    }, {
        file: path.join('Calendar', 'resources', 'css', 'style.css'),
        altFile1: path.join('Calender', 'resources', 'css', 'style.css'),
        altFile2: path.join('Calander', 'resources', 'css', 'style.css'),
        points: 1
    }, {
        file: path.join('Calendar', 'index.html'),
        altFile1: path.join('Calender', 'index.html'),
        altFile2: path.join('Calander', 'index.html'),
        points: 1
    }];
    let totalPoints = {};
    let errors = "";
    const dirStructurePoints = {
        section_name: "dir structure",
        points: 0,
        comments: ""
    }
    let exitEarly = false
    let scriptContents, htmlContents;
    labFiles.forEach((fileObj) => {
        let foundFilePath;
        if (fs.existsSync(path.join(filePath, fileObj.file))) {
            dirStructurePoints['points'] += fileObj.points;
            foundFilePath = path.join(filePath, fileObj.file);
        } else if (fs.existsSync(path.join(filePath, fileObj.altFile1))) {
            dirStructurePoints['points'] += fileObj.points
            foundFilePath = path.join(filePath, fileObj.altFile1);
        } else if (fs.existsSync(path.join(filePath, fileObj.altFile2))) {
            dirStructurePoints['points'] += fileObj.points
            foundFilePath = path.join(filePath, fileObj.altFile2);
        } else {
            dirStructurePoints['comments'] += `-${fileObj.points}: file ${fileObj.file} not found in path; `
            exitEarly = true
            test("files not found", () => {
                expect(1).toBe(1);
            });
        }
        if (foundFilePath) {
            if (foundFilePath.indexOf("js") > -1) {
                scriptContents = fs.readFileSync(foundFilePath, 'ascii');
                scriptContents = scriptContents.replaceAll("const", "var")
            } else if (fileObj.file.indexOf("html") > -1) {
                htmlContents = fs.readFileSync(foundFilePath, 'ascii');
            }
        }
    });
    totalPoints['dirStructurePoints'] = dirStructurePoints;

    // ------------END - SETUP-------------
    if (!exitEarly) {

        test('<html_test>', () => {
            const section_points = {
                section_name: "html",
                points: 0,
                comments: ''
            }
            try {

                const htmlParsed = new Soup(htmlContents);
                const linkTags = htmlParsed.findAll("link");
                const validRefs = [
                    "https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css",
                    "https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js",
                    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css"
                ];
                let foundLinks = false;
                linkTags.forEach((link) => {
                    if (link.attrs.href && link.attrs.href.startsWith('https')) {
                        if (validRefs.indexOf(link.attrs.href) > -1) {
                            foundLinks = true;
                        }
                    }
                });
                if (foundLinks) {
                    section_points['points'] += 5;
                } else {
                    section_points['comments'] += '-5: the bootsrap stylesheets are not used'
                }
            } catch (err) {
                console.log(err);
                errors += cleanMsg(err.message) + "; "
            }
            totalPoints['html'] = section_points;
            expect(1).toBe(1);
        });
    
        test('<initializeContent> fn', async () => {
            eval(scriptContents);
            const sectionPoints = {
                section_name: "initializeContent",
                points: 0,
                comments: ''
            }
            try {
        
                const htmlParsed = new Soup(htmlContents);
                const bodyTag = htmlParsed.find("body")
                if (bodyTag) {
                    if (bodyTag.attrs.onload === "initializeContent()") {
                        sectionPoints['points'] += 2
                    } else {
                        sectionPoints['comments'] += '-2: onload function is not added; ';
                    }
                }
                const mainContainer = htmlParsed.find("div", { class: "container" })
                if (mainContainer) {
                    const calendar = mainContainer.find("div", {id: "calendar"})
                    if (calendar) {
                        sectionPoints['points'] += 2
                    } else {
                        sectionPoints['comments'] += "-2: container/calendar div is not found; "
                    }
                } else {
                    sectionPoints['comments'] += "-2: container/calendar div is not found; "
                }
    
                document.head.innerHTML = `
                    <link
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css"
                    rel="stylesheet"
                    integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT"
                    crossorigin="anonymous"
                    />
                    <script
                    src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js"
                    integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8"
                    crossorigin="anonymous"
                    ></script>
                    <link
                    rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css"
                    />
                `
                document.body.innerHTML = `
                    <div class="calendar" id="calendar"></div>
                    <div id="eventModal"></div>
                    <div id="event-modal"></div>
                `
                try {
                    initializeContent();
                } catch(e) {}
                const calendarEle = document.getElementById("calendar");
                const parsedSoup = new Soup(calendarEle.innerHTML)
                const mondayEle = parsedSoup.find('div', { id: "monday" })
                const tuesdayEle = parsedSoup.find('div', { id: "tuesday" })
                const wednesdayEle = parsedSoup.find('div', { id: "wednesday" })
                const thursdayEle = parsedSoup.find('div', { id: "thursday" })
                const fridayEle = parsedSoup.find('div', { id: "friday" })
                const saturdayEle = parsedSoup.find('div', { id: "saturday" })
                const sundayEle = parsedSoup.find('div', { id: "sunday" })
                let isNull = false; let count = 0;
                [mondayEle, tuesdayEle, wednesdayEle, thursdayEle, fridayEle, saturdayEle, sundayEle].forEach((ele) => {
                    if (!ele) {
                        isNull = true;
                        count += 1
                    } 
                })
                if (isNull) {
                    // console.log("cannot find all day element, found only", (7 - count))
                    sectionPoints['points'] += (7-count) * 0.5;
                    sectionPoints['comments'] += `-${(count * 0.5)}: divs for all days of week are not present; `
                } else {
                    sectionPoints['points'] += 3.5;
                }
                const icons = parsedSoup.findAll('i')
                if (icons.length === 0) {
                    sectionPoints['comments'] += "-2.5: addEvent icon is not added; "
                } else {
                    const onclickFn = icons[0]?.attrs?.onclick
                    if (onclickFn) {
                        if (onclickFn.indexOf("openEventModal") > -1) {
                            // console.log("found onclick function", onclickFn)
                            sectionPoints['points'] += 2.5
                        } else {
                            sectionPoints['comments'] += '-2.5: onclick funtion is not linked to open event modal; '
                        }
                    }
                }
            } catch (err) {
                console.log(err);
                errors +=  "err in <initializeContent> -" + cleanMsg(err.message) + "; "
            }
            totalPoints['initializeContent'] = sectionPoints;
            expect(1).toBe(1); 
        });
    
        test('Create/update events fns', () => {
            eval(scriptContents);
            const sectionPoints = {
                section_name: "Create/Update Event",
                points: 0,
                comments: ''
            }
            try {
                const parsedSoup = new Soup(htmlContents);
                const eventModality = parsedSoup.find("select", { id: "modality" })
                const eventName = parsedSoup.find("input", {id: "event_name"})
                const eventDay = parsedSoup.find("select", {id: "weekday"})
                const eventTime = parsedSoup.find("input", {id: "time"})
                const eventLocation = parsedSoup.find("input", {id: "location"})
                const fields = [eventModality, eventName, eventTime, eventDay, eventLocation]
                const indexMapping = ["eventModality", "eventName", "eventTime", "eventDay", "eventLocation"]
                fields.forEach((field, index) => {
                    if (field) {
                        sectionPoints['points'] += 1
                    } else {
                        sectionPoints['comments'] += `-1: field ${indexMapping[index]} is missing or id property is not set (check lab writeup); `
                    }
                });
                if (eventModality) {
                    if (eventModality.attrs.onchange === "updateLocationOptions(this.value)") {
                        sectionPoints['points'] += 5
                    }  else {
                        sectionPoints['comments'] += "-5: event modality onchange function is missing; "
                    }
                } else {
                    sectionPoints['comments'] += '-5: event modality div is missing and onchange function is missing; '
                }
            } catch(err) {
                errors += "err in <CreateUpdateEvent> - "  + cleanMsg(err.message) + "; ";
                console.log(err);
            }
            totalPoints['createUpdateEvents'] = sectionPoints;
            expect(1).toBe(1);
        });
    
        test('<updateDom> fn', () => {
            eval(scriptContents);
            const sectionPoints = {
                section_name: "UpdateDOM",
                points: 0,
                comments: ''
            }
            try {
                if (CALENDAR_EVENTS) {
                    if (CALENDAR_EVENTS.length > 0) {
                        sectionPoints['points'] += 2
                    } else {
                        sectionPoints['comments'] += '-2: calendar_events array does not have default events; '
                    }
                    while (CALENDAR_EVENTS.length > 0) {
                        CALENDAR_EVENTS.pop()
                    }
                    CALENDAR_EVENTS.push({
                        name: 'Dummy event 1',
                        day: 'monday',
                        time: '1:00',
                        modality: 'remote',
                        location: 'college',
                        url: 'www.google.com',
                        attendees: 'mark'
                    });
                    if (scriptContents.indexOf("updateDom") > -1) {
                        try {
                            updateDom();
                        } catch(e) {}
                    } else if (scriptContents.indexOf("updateDOM") > -1) {
                        try {
                            updateDOM();
                        } catch(e) {}
                    } else {
                        sectionPoints['comments'] += "-6: updateDom fn not found; "
                    }
                    const dummyEvent = document.getElementById("event-0");
                    if (dummyEvent) {
                        const titleChild = dummyEvent.children
                        if (titleChild && titleChild.length > 0) {
                            if (titleChild[0].innerHTML === 'Dummy event 1') {
                                sectionPoints['points'] += 6
                            } else {
                                sectionPoints['comments'] += "-6: event title is not added to event element; "
                            }
                        }
                        // add points   3
                        const clickListener = dummyEvent.getAttribute("onclick") || dummyEvent.getAttribute("onClick")
                        if (clickListener === "openEventModal({id: 0})") {
                            sectionPoints['points'] += 2
                        } else {
                            sectionPoints['comments'] += "-2: open event modal click listener is not added; "
                        }
                    } else {
                        sectionPoints['comments'] += '-8: updateDom fn does not work as expected new event was not added';
                    }
                } else {
                    sectionPoints['comments'] += "-10: CALENDAR EVENTS object is missing; "
                }
            } catch(err) {
                sectionPoints['comments'] += "-10: update dom fn is incomplete; "
                errors += "err in <Updatedom> -" + cleanMsg(err.message) + "; "
                console.log(err)
            }
            totalPoints['updateDom'] = sectionPoints;
            expect(1).toBe(1);
        });
    
        test('<openEventModal> fn', () => {
            const modifiedScript = mockFn("updateLocationOptions(value)", "updateLocationOptionsMock(value)", scriptContents);
            eval(modifiedScript);
            const sectionPoints = {
                section_name: "Open event modal",
                points: 0,
                comments: ''
            };
            try {
                if (CALENDAR_EVENTS) {
                    if (CALENDAR_EVENTS.length > 0) {
                        while (CALENDAR_EVENTS.length > 0) {
                            CALENDAR_EVENTS.pop();
                        }
                    }
                    document.body.innerHTML = `
                        <div id="submit_button"></div>
                        <div class="modal-title"></div>
                        <input id="event_name"></input>
                        <input id="weekday"></input>
                        <input id="time"></input>
                        <input id="modality"></input>
                        <input id="location"></input>
                        <input id="remote_url"></input>
                        <input id="attendees"></input>
                        <div id="modal"><form></form></div>
                    `;
                    try {
                        openEventModal({ id: 0, day: 'monday' })
                    } catch(e) {}
                    const buttonEle = document.getElementById('submit_button');
                    const modalTitle = document.querySelector(".modal-title");
                    if (buttonEle.innerHTML.toLowerCase() === 'create event' && modalTitle.innerHTML.toLowerCase() === 'create event') {
                        sectionPoints['points'] += 5;
                    } else {
                        sectionPoints['comments'] += '-5: create event button and modal title are missing; ';
                    }
                    CALENDAR_EVENTS.push({
                        name: 'Dummy event',
                        day: 'monday',
                        time: '13:00',
                        modality: 'remote',
                    });
                    try {
                        openEventModal({ id: 0, day: 'monday' })
                    } catch(e) {}
                    const buttonEle1 = document.getElementById('submit_button');
                    const modalTitle1 = document.querySelector(".modal-title");
                    if (buttonEle1.innerHTML.toLowerCase() === 'update event' && modalTitle1.innerHTML.toLowerCase() === 'update event') {
                        sectionPoints['points'] += 5;
                    } else {
                        sectionPoints['comments'] += '-5: update event button and modal title are missing; ';
                    }
                } else {
                    sectionPoints['comments'] += "-5: CALENDAR EVENTS object is missing; "
                }
            } catch (err) {
                console.log(err);
                sectionPoints['comments'] += "-10: openEventModal fn is incomplete; "
                errors += "err in <openEventModal> - " + cleanMsg(err.message) + "; "
            }
            totalPoints['openEventModal'] = sectionPoints
            expect(1).toBe(1);
        });
    
        test('<updateEventFromModal>', () => {
            eval(scriptContents);
            const sectionPoints = {
                section_name: "Update event modal",
                points: 0,
                comments: ''
            };
            try {
                if (CALENDAR_EVENTS) {
                    if (CALENDAR_EVENTS.length > 0) {
                        while (CALENDAR_EVENTS.length > 0) {
                            CALENDAR_EVENTS.pop();
                        }
                    }
                    document.body.innerHTML = `
                        <input id="event_name" value="Dummy event">
                        <input id="weekday" value="monday">
                        <input id="time" value="13:00">
                        <input id="modality" value="remote">
                        <input id="location" value="boulder">
                        <input id="remote_url" value="">
                        <input id="attendees" value="">
                    `;
                    try {
                        updateEventFromModal(0);
                    } catch (err) {}
                    if (CALENDAR_EVENTS && CALENDAR_EVENTS.length === 1) {
                        const arr = [
                            CALENDAR_EVENTS[0]['name'] === 'Dummy event',
                            CALENDAR_EVENTS[0]['day'] === 'monday',
                            CALENDAR_EVENTS[0]['time'] === '13:00',
                            CALENDAR_EVENTS[0]['modality'] === 'remote',
                            CALENDAR_EVENTS[0]['location'] === 'boulder'
                        ];
                        const fields = ['name','day','time','modality','location'];
                        arr.forEach((eq, idx) => {
                            if (eq) {
                                sectionPoints['points'] += 2
                            } else {
                                sectionPoints['comments'] += `-2: event field: ${fields[idx]} is not updated in function: updateEventFromModal; `;
                            }
                        });
                        console.log(CALENDAR_EVENTS);
                    } else {
                        sectionPoints['comments'] += `-10: updateEventFromModal fn. does not work as expected; `;
                    }
                } else {
                    sectionPoints['comments'] += "-10: CALENDAR EVENTS object is missing; "
                }
            } catch(err) {
                console.log(err);
                sectionPoints['comments'] += "-10: updateEventFromModal fn is incomplete; "
                errors += "err in <updateEventFromModal> - " + cleanMsg(err.message) + "; "
            }
            totalPoints["updateEventFromModal"] = sectionPoints;
            expect(1).toBe(1);
        });
    
        test('<updateTooltips> fn', () => {
            eval(scriptContents);
            const section_points = {
                section_name: "update_tooltips",
                points: 0,
                comments: ''
            }
            try {
                const matched_len = (scriptContents.match(/data-bs-toggle/g) || []).length;
                if (matched_len === 2) {
                    // full points
                    section_points['points'] += 20
                } else if (matched_len === 1) {
                    // 5 points
                    section_points['points'] += 10
                    section_points['comments'] += '-10: tooltips is not completely implemented; '
                } else {
                    section_points['comments'] += '-20: update_tooltips fn is not implemented; '
                }
            } catch(err) {
                console.log(err);
                sectionPoints['comments'] += "-20: updateToolTips fn is incomplete; "
                errors += "err in <updateTooltips> - " + cleanMsg(err.message) + "; "
            }
            totalPoints['updateTooltips'] = section_points;
            expect(1).toBe(1);
        });
    }

    afterAll(() => {
        const cols = ["Name","dirStructurePoints","html","initializeContent","createUpdateEvents","updateDom","openEventModal","updateEventFromModal","updateTooltips","Attendance","Total","Comments","Errors"]
        let content = '';
        let comments = '';
        let total = 0;
        cols.forEach((col) => {
            if (col === 'Name') {
                content += submissionName + ','
            } else if (['Comments', 'Errors', 'Total', 'Attendance'].indexOf(col) > -1) {
                // do nothing
            } else if (totalPoints[col]) {
                if (totalPoints[col]['comments'].length > 0) {
                    comments += totalPoints[col]['comments'] + '; '
                }
                content += totalPoints[col]['points'] + ','
                total += totalPoints[col]['points'];
            } else {
                content += 0 + ','
                comments += `grading section ${col} skipped; `
            }
        });
        content += ","
        content += total + ","
        content += comments + ",";
        content += errors;
        content += '\n'
        const folderPath = filePath.substring(0, filePath.lastIndexOf("\\"))
        fs.appendFileSync(path.join(folderPath, 'grades.csv'), content);
    });
});
