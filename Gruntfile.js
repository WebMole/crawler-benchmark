/* global module:true */

module.exports = function (grunt) {
    'use strict';

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        staticPath: 'project/static',
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            gruntfile: {
                src: 'Gruntfile.js'
            }
        },
        sass: {
            dist: {
                files: {
                    '<%= staticPath %>/css/style.css': '<%= staticPath %>/css/style.scss'
                }
            }
        },
        watch: {
            gruntfile: {
                files: '<%= jshint.gruntfile.src %>',
                tasks: ['jshint:gruntfile']
            },
            sass: {
                files: ['**/*.scss'],
                tasks: ['sass'],
                options: {
                    livereload: true
                }
            }
        }
    });

    require('load-grunt-tasks')(grunt);

    grunt.registerTask('build', ['jshint', 'sass']);
    grunt.registerTask('default', ['watch']);
};
