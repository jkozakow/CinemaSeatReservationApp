app = angular.module 'appcinema.app.movies', []

app.controller 'AppController', ['$scope', '$http', ($scope, $http) ->
    $scope.movies = []
    $http.get('/api/movies').then (result) ->
        angular.forEach result.data, (item) ->
            $scope.movies.push item
]
