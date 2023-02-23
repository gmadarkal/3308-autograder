const jest = require('jest')
const projects = ["<rootDir>\\autograder\\lab5\\js-test"]
console.log(process.argv)
const filePath = process.argv[2]
const submissionName = process.argv[3]
// console.log("grading submission in folder:", filePath)
process.env.JEST_ENVIRONMENT = filePath
process.env.SUBMISSION_NAME = submissionName
jest.runCLI({
    config: "", 
    silent: true
}, 
projects)

// const fs = require('fs')
// const path = require('path')
// const filepath = "";

// const cont = fs.readFileSync(fs.readFileSync(path.join(filepath.replace(/\\/g, "\\\\"), 'Calendar\\resources\\js\\script.js'), 'ascii'));
// console.log(cont);

