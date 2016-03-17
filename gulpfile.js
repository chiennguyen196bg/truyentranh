var gulp = require('gulp');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var nodemon = require('gulp-nodemon');

gulp.task('default', [], function () {
    console.log("Command:\n   myapp - run live reload server");
});
gulp.task('app', [], function () {
    browserSync({
        script: 'app.js',
        notify: false,
        server: {
            baseDir: '.'
        }
    });
    
    gulp.watch(['/src/views/*.ejs'], reload);
    gulp.watch(['/public/js/**/*.js'], reload);
    gulp.watch(['/src/routes/*.js'], reload);
    gulp.watch(['/public/css/*.css'], reload);

});
gulp.task('develop', function () {
  nodemon({ script: 'app.js'
          , ext: 'ejs js css'
          , ignore: ['ignored.js']
          , tasks: ['lint'] })
    .on('restart', function () {
      console.log('restarted!')
    })
})