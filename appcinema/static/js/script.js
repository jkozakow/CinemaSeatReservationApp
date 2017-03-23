(function() {
  var app;

  app = angular.module('appcinema.app.movies', []);

  app.controller('AppController', [
    '$scope', '$http', function($scope, $http) {
      $scope.movies = [];
      return $http.get('/api/movies').then(function(result) {
        return angular.forEach(result.data, function(item) {
          return $scope.movies.push(item);
        });
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('appcinema.api', ['ngResource']);

  app.factory('Movie', [
    '$resource', function($resource) {
      return $resource('/api/movies/:id', {
        id: '@id'
      });
    }
  ]);

}).call(this);
