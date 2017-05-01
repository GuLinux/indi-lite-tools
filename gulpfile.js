// requirements

var gulp = require('gulp');
var del = require('del');
var fs = require('fs');
var webpack = require('webpack-stream');

// tasks

gulp.task('transform', function () {
    var dest = './static/';
    try {
        fs.mkdirSync(dest);
    }
    catch(e) {
    }
    var src = './react/index.js';
    return gulp.src(src)
        .pipe(webpack(require('./webpack.config.js')))
        .on('error', function(e) { console.log('!!!!! ERROR on WebPack !!!!!'); console.log(e); })
        .pipe(gulp.dest(dest))
    ;
});

gulp.task('del', function () {
    return del(['./static/scripts/js']);
});

gulp.task('watch', ['del'], function() {
    try {
        gulp.start('transform');
        gulp.watch('./react/**/*.js', ['transform']);
    }
    catch(e) {
        console.log(e);
    }
});

gulp.task('default', ['del'], function() {
    gulp.start('transform');
});
